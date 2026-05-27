# claude-code-ofertas — Instrucciones para Claude

Repo unificado que **descubre, valida, enriquece y redacta** artículos de oferta para Amazon España y AliExpress España. Combina dos flujos antes separados:

- **`/buscar-ofertas`** — descubrimiento desde `radar_editorial`, filtrado contra la guideline del medio, validación humana y enriquecimiento → ficha en `inbox/`.
- **`/crear-articulo`** — toma una URL de producto o lee `inbox/`, orquesta los subagentes redactores (product-researcher, angle-picker, headline-generator, writer, editor-in-chief) → draft en `drafts/{medio}/`.
- **`/crear-guideline`** — crea o actualiza una guideline editorial por medio.
- **`/importar-gpt`** — importa instrucciones de un GPT personalizado al formato guideline.

Todo vive en la misma sesión de Claude Code. Las rutas son internas (`inbox/`, `guidelines/`, `drafts/`), no relativas a un proyecto hermano.

---

## Estructura de carpetas

```
claude-code-ofertas/
├── .claude/
│   ├── settings.json
│   ├── hooks/
│   │   └── session-start-pull.sh    ← auto-pull desde GitHub al arrancar
│   ├── agents/
│   │   ├── aggregator-scraper.md    (scraping Chollometro — manual/diagnóstico)
│   │   ├── telegram-scraper.md      (scraping Telegram — manual/diagnóstico)
│   │   ├── radar-catalog-client.md  (consulta radar_editorial)
│   │   ├── offer-enricher.md        (enriquecimiento de tienda)
│   │   ├── product-researcher.md    (investigación producto para redacción)
│   │   ├── angle-picker.md          (decisión de ángulo + persona-redactora)
│   │   ├── headline-generator.md    (titular)
│   │   ├── writer.md                (redacción del draft)
│   │   └── editor-in-chief.md       (validación final del draft)
│   └── skills/
│       ├── buscar-ofertas/SKILL.md
│       ├── crear-articulo/SKILL.md
│       ├── crear-guideline/SKILL.md
│       └── importar-gpt/SKILL.md
├── fuentes.md                       ← fuentes de descubrimiento activas
├── medios.md                        ← slugs canónicos por medio
├── guidelines/                      ← voz editorial por medio
│   └── GUIDELINE-{medio}.md
├── watchlists/                      ← listas temáticas para /buscar-ofertas
├── inbox/                           ← handoff: fichas validadas en buscar → consumidas en crear
├── drafts/{medio}/                  ← output del writer
├── historial/                       ← sesiones de /buscar-ofertas
├── changelog/
├── knowledge/
│   ├── manifiesto-editorial.md
│   ├── frases-vetadas.md
│   ├── headline-recipes.md
│   ├── naming-productos.md
│   ├── politicas-afiliacion.md
│   ├── posicion-precio-por-angulo.md
│   ├── notas-degradacion.md
│   ├── ejemplos-publicados/
│   └── personas-redactoras/
├── docs/
│   ├── brainstorms/
│   ├── plans/
│   ├── qa/
│   ├── instalacion.txt
│   ├── configuracion-local-radar.txt
│   └── integracion-radar-editorial.txt
├── pruebas/
├── tasks/
├── .env.example
├── .env                             (gitignored)
├── CLAUDE.md
└── README.md
```

---

## Convenciones comunes

- **Fechas:** `DD/MM/YYYY` en frontmatter y texto al redactor. `YYYY-MM-DD` solo en nombres de archivo donde la ordenación lex importa.
- **Números:** estilo español, punto para miles y coma para decimales (`1.299,00 €`).
- **Idioma:** todo el texto al redactor en español con ortografía y acentos correctos.
- **Naming de archivos:**
  - Fichas en `inbox/`: `DD-MM-YYYY-{slug-titulo}.md`.
  - Watchlists: `WATCHLIST-{slug-kebab}.md`.
  - Historial: `YYYY-MM-DD-sesion-{n}.md`.
  - Changelog: `changelog-YYYY-MM-DD.txt`.
- **Slugs:** kebab-case sin acentos, máx 60 caracteres.

---

## Dominio: descubrimiento (`/buscar-ofertas`)

### Política de fuentes

- **Fuente principal MVP:** `radar_editorial` (vía subagente `radar-catalog-client`).
- **Fuentes de respaldo manual/diagnóstico:** Chollometro (`aggregator-scraper`) y canales Telegram hispachollos + chollazos (`telegram-scraper`). NO se invocan automáticamente desde el orquestador.
- **Tiendas finales aceptadas:** `amazon.es` (`amazon-es`), `es.aliexpress.com` (`aliexpress-es`), `aliexpress.com` (`aliexpress-global`). Resto se descarta.
- **Cloudflare delante de Chollometro** → Playwright MCP, no WebFetch directo.

### Regla de capas

| Capa | Quién | Tools |
|---|---|---|
| Orquestación + filtrado editorial + pausas | `buscar-ofertas` (skill) | Read, Write |
| Consulta radar | `radar-catalog-client` | WebFetch |
| Scraping Chollometro (manual) | `aggregator-scraper` | Playwright |
| Scraping Telegram (manual) | `telegram-scraper` | WebFetch |
| Enriquecimiento de tienda | `offer-enricher` | Playwright |

Los subagentes no se llaman entre sí. Solo el orquestador los invoca.

### Errores tipados

- **`AggregatorBlockedError`** — Chollometro bloqueado. Sin reintentos automáticos. El orquestador avisa con candidatas parciales.
- **`StoreBlockedError`** — Amazon/AliExpress bloquea al enriquecer. La ficha se marca `fuente: manual`.
- **`StoreMismatchError`** — el título de tienda no encaja con `titulo_radar` (Paso 3.5 del enricher). Pausa interactiva: Saltar / Rechazar / Forzar.
- **`RadarConfigError`** / **`RadarUnavailableError`** — radar caído o sin token. Detiene el flujo.
- **`GuidelineMissingError`** — no existe `guidelines/GUIDELINE-{medio}.md`. Mensaje literal: *"El medio '{medio}' no tiene guideline. Crea primero la guideline con `/crear-guideline` y vuelve a lanzar."*

---

## Dominio: redacción (`/crear-articulo`)

### Subagentes en secuencia

1. **`product-researcher`** — extrae ficha de la URL (precio, reseñas, specs).
2. **`angle-picker`** — propone ángulo + persona-redactora (pausa interactiva A con el redactor humano).
3. **`headline-generator`** — propone 3 titulares (pausa B).
4. **`writer`** — escribe el draft completo siguiendo guideline + persona.
5. **`editor-in-chief`** — valida el draft contra guideline, frases vetadas y test de bloguero.

### Inputs admitidos

- **`/crear-articulo <url1> [url2 ...] [medio]`** — modo URL directo (prioritario si hay URLs).
- **`/crear-articulo [medio] [filtro-inbox]`** — si no hay URLs, se busca en `inbox/`.
  - Sin filtro → menú completo del inbox.
  - Con filtro (texto) → fuzzy match en nombres de archivo.
  - Si match único → continúa automáticamente con `url_producto` del frontmatter.
  - Si múltiples → menú filtrado.

### Pausas interactivas obligatorias

El skill `/crear-articulo` **NO admite auto mode** en las pausas A (ángulo + persona) y B (titular). Son decisiones humanas. Ver bloque "PROHIBIDO el auto mode" del SKILL.

---

## Política de auto-pull

Hook `SessionStart` ejecuta `.claude/hooks/session-start-pull.sh` al arrancar Claude Code en este repo. Hace `git pull --ff-only` y muestra:

- "✓ Sistema al día" si nada cambió.
- "✓ Sistema actualizado con N commits nuevos" si hubo pull.
- Advertencia si falló (no bloquea la sesión; el redactor decide).

Trabajamos siempre con la última versión de GitHub. El PASO 0 manual de git pull dentro de `crear-articulo` queda como fallback.

---

## Política de scraping (heredada del localizador)

- `browser_wait_for` con timeout máximo 10 segundos. Sin reintentos automáticos.
- Throttling: 1-2 s entre acciones.
- Selectores por accessibility tree (rol + nombre accesible), nunca por CSS.
- Aceptar banner de cookies en el primer acceso de la sesión.
- Redirect de afiliación: resolver URL canónica siguiendo navegación, no extrayendo `href` directo.
- Cualquier dominio o selector inestable se registra en `knowledge/notas-degradacion.md`.

---

## Política editorial (heredada del writer)

- Lectura obligatoria previa a redactar: `knowledge/manifiesto-editorial.md`.
- Voz del medio en `guidelines/GUIDELINE-{medio}.md`. Personas-redactoras en `knowledge/personas-redactoras/`.
- Frases vetadas globales en `knowledge/frases-vetadas.md`. El editor-in-chief aplica el test de "frase intercambiable" en todos los medios.
- Posición del precio según ángulo: `knowledge/posicion-precio-por-angulo.md`.
- Naming marca + modelo: `knowledge/naming-productos.md`.
- Headline recipes: `knowledge/headline-recipes.md`.
- Disclaimer y compliance de afiliación: `knowledge/politicas-afiliacion.md`.

---

## Reglas generales

- **Modo de planificación predeterminado** para tareas no triviales (más de 3 pasos o decisiones de arquitectura). Planes en `docs/plans/YYYY-MM-DD-{nombre}.md`.
- **Subagentes para tareas paralelas o que ensucian la ventana de contexto.**
- **Simplicidad primero.** Cambios mínimos, impacto acotado.
- **Sin pereza.** Causas raíz, no parches.
- **Orden de carpetas.** Si generas un plan o script temporal, revísalo al final y bórralo si ya no sirve.
- **Documenta lo que cambies** en `changelog/changelog-YYYY-MM-DD.txt`.
