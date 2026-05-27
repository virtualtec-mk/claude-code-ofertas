# Tabla maestra de medios

Este archivo es la fuente de verdad sobre todos los medios configurados en el sistema.

**Se actualiza automáticamente** en dos momentos:
- Al crear o modificar un guideline con `/crear-guideline`.
- Al publicar un artículo (columna "Última publicación").

Si detectas que la tabla está desincronizada con los archivos de `/guidelines/`, usa `/crear-guideline` sobre el medio afectado para recalibrar, o edita la fila manualmente.

**Importante sobre los slugs:** El slug de cada medio (columna "Medio") debe coincidir exactamente con el nombre del archivo `GUIDELINE-{medio}.md` en la carpeta `/guidelines/`. Los slugs se confirman con el redactor o champion editorial antes de crear el guideline por primera vez. Una vez fijados, no cambiarlos sin actualizar también los drafts y los ejemplos publicados de ese medio.

---

## Medios registrados

| Medio | Tipo | Tono | Longitud | Formatos multi admitidos | Disclaimer afiliación | Última publicación | Estado guideline |
|---|---|---|---|---|---|---|---|
| `mundodeportivo` | deportes | cercano-experto / enérgico | 450-500 (mono) / 600-800 (multi 3-10 prod.) | comparativa · recopilatorio · top-n · por-presupuesto · por-uso | Lo gestiona el CMS | — | ✅ activa (v2.4) |
| `larazon` | generalista / consumo y estilo de vida | cercano-directo / autoridad tranquila | 600-900 (mono) / 1.000-2.200 (multi) / 1.500-2.000 (análisis) | comparativa · recopilatorio · top-n · por-presupuesto · por-uso | Texto propio (ver guideline) | 19/05/2026 | ✅ activa (v2.7) |
| `abc` | generalista / Favorito (consumo, tecnología, motor, hogar) | conversacional con chispa / experto + amigo de chollos | 500-700 (oferta única) / 800-1.200 (recopilatorio) / 600-900 (longtail-marca) | comparativa · recopilatorio · top-n · por-presupuesto · por-uso · longtail-marca | Lo gestiona el CMS | 19/05/2026 | ✅ activa (v1.2) |

---

## Referencia de columnas

| Columna | Descripción | Valores posibles |
|---|---|---|
| **Medio** | Slug exacto del medio (igual que el nombre del archivo GUIDELINE) | ej. `xataka`, `marca`, `meristation` |
| **Tipo** | Categoría editorial del medio | `tecnología`, `lifestyle`, `gaming`, `motor`, `hogar`, `generalista` |
| **Tono** | Registro de escritura predominante | `divulgativo`, `informal`, `técnico`, `aspiracional`, `directo` |
| **Longitud** | Extensión objetivo del artículo | ej. `300-500 palabras`, `500-800 palabras` |
| **Formatos multi admitidos** | Slugs de `FORMATO_GUIA` que la guideline del medio acepta para guías multi-producto | ej. `comparativa · recopilatorio · top-n`. Subconjunto de: `comparativa`, `recopilatorio`, `top-n`, `por-presupuesto`, `por-uso`, `longtail-marca` |
| **Disclaimer afiliación** | Texto o referencia al aviso legal que usa ese medio | ej. `"Este artículo contiene enlaces de afiliación"` o `ver guideline` |
| **Última publicación** | Fecha del último artículo generado para ese medio | Formato DD/MM/YYYY |
| **Estado guideline** | Si la guideline está lista para producción | `activa`, `borrador`, `pendiente-revisión` |
