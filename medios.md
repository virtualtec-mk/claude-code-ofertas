# Tabla maestra de medios

Este archivo es la fuente de verdad sobre todos los medios configurados en el sistema.

**Se actualiza automáticamente** en dos momentos:
- Al crear o modificar un guideline con `/crear-guideline`.
- Al publicar un artículo (columna "Última publicación").

Si detectas que la tabla está desincronizada con los archivos de `/guidelines/`, usa `/crear-guideline` sobre el medio afectado para recalibrar, o edita la fila manualmente.

**Importante sobre los slugs:** El slug de cada medio (columna "Medio") debe coincidir exactamente con el nombre del archivo `GUIDELINE-{medio}.md` en la carpeta `/guidelines/`. Los slugs se confirman con el redactor o champion editorial antes de crear el guideline por primera vez. Una vez fijados, no cambiarlos sin actualizar también los drafts y los ejemplos publicados de ese medio.

---

## Medios registrados

| Medio | Tipo | Tono | Longitud | Disclaimer afiliación | Última publicación | Estado guideline |
|---|---|---|---|---|---|---|
| `mundodeportivo` | deportes | cercano-experto / enérgico | 450-500 (1 prod.) / 600-800 (3-10 prod.) | Lo gestiona el CMS | — | ✅ activa |
| `larazon` | generalista / consumo y estilo de vida | cercano-directo / autoridad tranquila | 400-600 (oferta simple) / 1.500-2.000 (análisis) | Texto propio (ver guideline) | 19/05/2026 | ✅ activa |
| `abc` | generalista / Favorito (consumo, tecnología, motor, hogar) | conversacional con chispa / experto + amigo de chollos | 500-700 (oferta única) / 800-1.200 (recopilatorio) / 600-900 (longtail-marca) | Lo gestiona el CMS | 19/05/2026 | ✅ activa (v1.1, calibrada con 18 ejemplos publicados) |

---

## Referencia de columnas

| Columna | Descripción | Valores posibles |
|---|---|---|
| **Medio** | Slug exacto del medio (igual que el nombre del archivo GUIDELINE) | ej. `xataka`, `marca`, `meristation` |
| **Tipo** | Categoría editorial del medio | `tecnología`, `lifestyle`, `gaming`, `motor`, `hogar`, `generalista` |
| **Tono** | Registro de escritura predominante | `divulgativo`, `informal`, `técnico`, `aspiracional`, `directo` |
| **Longitud** | Extensión objetivo del artículo | ej. `300-500 palabras`, `500-800 palabras` |
| **Disclaimer afiliación** | Texto o referencia al aviso legal que usa ese medio | ej. `"Este artículo contiene enlaces de afiliación"` o `ver guideline` |
| **Última publicación** | Fecha del último artículo generado para ese medio | Formato DD/MM/YYYY |
| **Estado guideline** | Si la guideline está lista para producción | `activa`, `borrador`, `pendiente-revisión` |
