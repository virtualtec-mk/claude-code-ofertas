"""
guidelines-check.py
Verifica la consistencia del proyecto: medios, guidelines, drafts y ejemplos publicados.
Ejecutar desde cualquier directorio: python docs/guidelines-check.py
"""

import os
import re
import sys

# Forzar UTF-8 en la salida para que los caracteres especiales no rompan en Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")


# ---------------------------------------------------------------------------
# Localizar raíz del proyecto (buscando CLAUDE.md hacia arriba desde este script)
# ---------------------------------------------------------------------------

def find_project_root():
    current = os.path.dirname(os.path.abspath(__file__))
    for _ in range(6):  # máximo 6 niveles hacia arriba
        if os.path.isfile(os.path.join(current, "CLAUDE.md")):
            return current
        parent = os.path.dirname(current)
        if parent == current:
            break
        current = parent
    return None


ROOT = find_project_root()
if ROOT is None:
    print("[ERROR] No se encontró CLAUDE.md. Ejecuta este script desde dentro del proyecto.")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Rutas relevantes
# ---------------------------------------------------------------------------

GUIDELINES_DIR = os.path.join(ROOT, "guidelines")
DRAFTS_DIR = os.path.join(ROOT, "drafts")
EJEMPLOS_DIR = os.path.join(ROOT, "knowledge", "ejemplos-publicados")
FRASES_VETADAS_FILE = os.path.join(ROOT, "knowledge", "frases-vetadas.md")
MEDIOS_FILE = os.path.join(ROOT, "medios.md")


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def existing_dir(path):
    return os.path.isdir(path)


def guideline_files():
    """Devuelve {slug: filepath} para cada GUIDELINE-*.md en guidelines/."""
    result = {}
    if not existing_dir(GUIDELINES_DIR):
        return result
    for name in os.listdir(GUIDELINES_DIR):
        m = re.match(r"^GUIDELINE-(.+)\.md$", name, re.IGNORECASE)
        if m:
            result[m.group(1)] = os.path.join(GUIDELINES_DIR, name)
    return result


def draft_medios():
    """Devuelve el conjunto de slugs de medios con al menos una subcarpeta en drafts/."""
    result = set()
    if not existing_dir(DRAFTS_DIR):
        return result
    for name in os.listdir(DRAFTS_DIR):
        if os.path.isdir(os.path.join(DRAFTS_DIR, name)):
            result.add(name)
    return result


def ejemplos_medios():
    """Devuelve el conjunto de slugs con carpeta en knowledge/ejemplos-publicados/."""
    result = set()
    if not existing_dir(EJEMPLOS_DIR):
        return result
    for name in os.listdir(EJEMPLOS_DIR):
        if os.path.isdir(os.path.join(EJEMPLOS_DIR, name)):
            result.add(name)
    return result


def medios_en_tabla():
    """
    Devuelve el conjunto de slugs de medios registrados en medios.md.
    Solo lee la tabla bajo el encabezado '## Medios registrados', ignorando
    la tabla de referencia de columnas y otras secciones.
    """
    result = set()
    if not os.path.isfile(MEDIOS_FILE):
        return result

    with open(MEDIOS_FILE, encoding="utf-8") as f:
        lines = f.readlines()

    # Localizar el bloque "## Medios registrados"
    in_section = False
    for line in lines:
        # Entrar en la sección correcta
        if re.match(r"^##\s+Medios registrados", line.strip(), re.IGNORECASE):
            in_section = True
            continue
        # Salir al encontrar otro encabezado de nivel 2
        if in_section and re.match(r"^##\s+", line):
            break
        if not in_section:
            continue
        if not line.startswith("|"):
            continue

        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells:
            continue
        slug = cells[0]

        # Descartar encabezado de columna, separadores y placeholder
        if slug in ("Medio", "", "*(añadir filas con /crear-guideline)*"):
            continue
        if re.match(r"^[-:]+$", slug):  # línea separadora de tabla
            continue

        result.add(slug)

    return result


def frases_vetadas_globales():
    """
    Devuelve la lista de frases literales del archivo frases-vetadas.md.
    Extrae ítems de lista (líneas que empiezan con '- "' o "- '").
    """
    frases = []
    if not os.path.isfile(FRASES_VETADAS_FILE):
        return frases
    with open(FRASES_VETADAS_FILE, encoding="utf-8") as f:
        for line in f:
            # Captura: - "frase" o - 'frase' o - frase sin comillas
            m = re.match(r'^-\s+"(.+?)"', line) or re.match(r"^-\s+'(.+?)'", line)
            if m:
                frases.append(m.group(1).lower())
            elif re.match(r"^-\s+\S", line):
                # Sin comillas: tomar el texto después del guion
                raw = re.sub(r"^-\s+", "", line).strip().lower()
                if raw and not raw.startswith("("):  # ignorar notas entre paréntesis
                    frases.append(raw)
    return frases


def frases_duplicadas_en_guideline(filepath, frases_globales):
    """
    Dado un archivo de guideline, busca si alguna frase global aparece literalmente
    en la sección de frases adicionales del medio.
    Heurística: busca después de un encabezado que contenga 'adicional' o 'vetad'.
    """
    if not frases_globales:
        return []
    duplicadas = []
    try:
        with open(filepath, encoding="utf-8") as f:
            content = f.read().lower()
    except Exception:
        return []

    # Intentar aislar solo la sección de frases adicionales
    # Si no existe esa sección, analizar el documento completo (mejor falso positivo que silencio)
    seccion_match = re.search(
        r"(adicional(?:es)?[^\n]*vetad[^\n]*|vetad[^\n]*adicional[^\n]*|frases\s+adicionales[^\n]*)\n(.*)",
        content,
        re.DOTALL | re.IGNORECASE,
    )
    if seccion_match:
        zona = seccion_match.group(2)
        # Recortar en el siguiente encabezado markdown
        zona = re.split(r"\n#{1,4}\s", zona)[0]
    else:
        zona = content  # analizar todo el documento

    for frase in frases_globales:
        if frase in zona:
            duplicadas.append(frase)
    return duplicadas


# ---------------------------------------------------------------------------
# Checks
# ---------------------------------------------------------------------------

def run_checks():
    issues = []
    oks = []

    guidelines = guideline_files()       # {slug: path}
    drafts = draft_medios()              # {slug, ...}
    ejemplos = ejemplos_medios()         # {slug, ...}
    tabla = medios_en_tabla()            # {slug, ...}
    frases_globales = frases_vetadas_globales()

    # -----------------------------------------------------------------------
    # 1. Medios en drafts/ sin guideline
    # -----------------------------------------------------------------------
    sin_guideline = drafts - set(guidelines.keys())
    if sin_guideline:
        for medio in sorted(sin_guideline):
            issues.append(
                f"[WARN] '{medio}' tiene drafts sin guideline "
                f"→ crea guidelines/GUIDELINE-{medio}.md"
            )
    else:
        if drafts:
            oks.append(f"[OK] Todos los medios con drafts ({len(drafts)}) tienen guideline")

    # -----------------------------------------------------------------------
    # 2. Guidelines sin carpeta de ejemplos publicados
    # -----------------------------------------------------------------------
    sin_ejemplos = set(guidelines.keys()) - ejemplos
    if sin_ejemplos:
        for medio in sorted(sin_ejemplos):
            issues.append(
                f"[WARN] Guideline '{medio}' no tiene ejemplos publicados "
                f"→ añade archivos en knowledge/ejemplos-publicados/{medio}/"
            )
    else:
        if guidelines:
            oks.append(f"[OK] Todas las guidelines ({len(guidelines)}) tienen ejemplos publicados")

    # -----------------------------------------------------------------------
    # 3. Frases vetadas globales duplicadas en sección adicional de guidelines
    # -----------------------------------------------------------------------
    for slug, path in sorted(guidelines.items()):
        duplicadas = frases_duplicadas_en_guideline(path, frases_globales)
        if duplicadas:
            preview = ", ".join(f'"{f}"' for f in duplicadas[:3])
            sufijo = f" (y {len(duplicadas)-3} más)" if len(duplicadas) > 3 else ""
            issues.append(
                f"[WARN] GUIDELINE-{slug}.md repite frases globales en su sección adicional: "
                f"{preview}{sufijo} → usa un puntero a frases-vetadas.md en vez de duplicarlas"
            )

    if not any("repite frases globales" in i for i in issues) and guidelines:
        oks.append("[OK] Ninguna guideline duplica frases de la lista global")

    # -----------------------------------------------------------------------
    # 4. Tabla medios.md vs archivos reales en guidelines/
    # -----------------------------------------------------------------------
    en_tabla_sin_archivo = tabla - set(guidelines.keys())
    en_archivo_sin_tabla = set(guidelines.keys()) - tabla

    if en_tabla_sin_archivo:
        for medio in sorted(en_tabla_sin_archivo):
            issues.append(
                f"[WARN] '{medio}' aparece en medios.md pero no tiene archivo GUIDELINE "
                f"→ crea guidelines/GUIDELINE-{medio}.md o corrige el slug en medios.md"
            )
    if en_archivo_sin_tabla:
        for medio in sorted(en_archivo_sin_tabla):
            issues.append(
                f"[WARN] GUIDELINE-{medio}.md existe pero '{medio}' no está en la tabla de medios.md "
                f"→ añade la fila en medios.md o elimina el archivo huérfano"
            )

    if not en_tabla_sin_archivo and not en_archivo_sin_tabla:
        if tabla or guidelines:
            oks.append(
                f"[OK] {len(guidelines)} guideline(s) consistente(s) con medios.md"
            )

    # -----------------------------------------------------------------------
    # Caso base: proyecto vacío
    # -----------------------------------------------------------------------
    if not guidelines and not drafts and not tabla:
        oks.append("[OK] Proyecto sin medios configurados aún — todo consistente")

    return oks, issues


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print()
    print("guidelines-check — Verificación de consistencia del proyecto")
    print("=" * 60)
    print(f"Raíz del proyecto: {ROOT}")
    print()

    oks, issues = run_checks()

    for line in oks:
        print(line)
    for line in issues:
        print(line)

    if not issues:
        print()
        print("Sin advertencias. El proyecto está en orden.")
    else:
        print()
        print(f"{len(issues)} advertencia(s) encontrada(s).")
        print("[INFO] Ejecuta /crear-guideline para crear guidelines faltantes")

    print()


if __name__ == "__main__":
    main()
