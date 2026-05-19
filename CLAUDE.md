# claude-code-localizador-ofertas — Instrucciones para Claude

Proyecto local operable desde Claude Code que **descubre** ofertas de Amazon España y AliExpress España en Chollometro, las **filtra** con el guideline editorial del medio destino y entrega las validadas como fichas listas en la inbox del proyecto hermano `claude-code-text-agents`.

Este repo se ocupa solo del **descubrimiento + filtrado + enriquecimiento**. La redacción la hace el otro proyecto a partir de la inbox.

---

## Convención de carpetas

```
claude-code-localizador-ofertas/
├── .claude/
│   ├── settings.json          ← permisos restrictivos
│   ├── agents/                ← subagentes con tools restringidos
│   │   ├── aggregator-scraper.md
│   │   ├── telegram-scraper.md
│   │   └── offer-enricher.md
│   └── skills/
│       └── buscar-ofertas/SKILL.md   ← orquestador único
├── fuentes.md                 ← tabla maestra de agregadores activos
├── watchlists/                ← markdown editables a mano (sin skill propia)
│   └── WATCHLIST-{slug}.md
├── historial/                 ← una sesión = un archivo
│   └── YYYY-MM-DD-sesion-{n}.md
├── knowledge/
│   └── notas-degradacion.md   ← log libre de dominios/patrones problemáticos
├── docs/
│   ├── brainstorms/
│   ├── plans/
│   └── instalacion.txt
├── changelog/
│   └── changelog-YYYY-MM-DD.txt
├── CLAUDE.md  (este archivo)
└── README.md
```

---

## Proyecto hermano: ubicación y reutilización

El proyecto hermano vive en **`../claude-code-text-agents/`**. Todas las rutas relativas a él se calculan desde la raíz de este repo. Si en el futuro el clon vive en otro sitio, edita aquí y en `.claude/settings.json`.

Se **leen** de allí (cero duplicación):
- `../claude-code-text-agents/guidelines/GUIDELINE-{medio}.md` — voz editorial por medio.
- `../claude-code-text-agents/medios.md` — slugs canónicos.

Se **escribe** allí:
- `../claude-code-text-agents/inbox/DD-MM-YYYY-{slug-producto}.md` — ficha validada con frontmatter compatible con `product-researcher` del otro repo.

Se **deniega** explícitamente cualquier escritura en `guidelines/**` o `drafts/**` del hermano.

Si la carpeta `../claude-code-text-agents/` no existe, lanza error claro (no traceback) y para el flujo.

---

## Política de scraping

- **Fuentes activas en MVP: Chollometro + Telegram (hispachollos, chollazos).** Tabla maestra en `fuentes.md`. Si añades una nueva, edita ese archivo Y crea el subagente correspondiente.
- **Tiendas finales aceptadas** (todo lo demás se descarta):
  - `amazon.es` → `tienda = amazon-es`.
  - `es.aliexpress.com` → `tienda = aliexpress-es`.
  - `aliexpress.com` (global, sin `es.`) → `tienda = aliexpress-global`. Se acepta como equivalente funcional porque el producto es el mismo `item/<ID>.html` y AliExpress geolocaliza al usuario español. Es el dominio al que aterrizan los redirects desde Telegram/`s.click.aliexpress.com`.
  - Descartadas: `amazon.com`, `amazon.co.uk`, `miravia.es`, `banggood.com`, etc.
- **Dedupe entre fuentes**: el orquestador deduplica por `url_canonica` tras unificar las listas de los scrapers (la misma ficha de Amazon puede aparecer en Chollometro y en uno o los dos canales de Telegram). Gana la candidata con más datos (precio anterior, % descuento) — si empatan, prevalece Chollometro.
- **Cloudflare delante de Chollometro.** WebFetch directo devuelve 403. Hay que ir con Playwright MCP (modo headed, lo gestiona el plugin).
- **Banner de cookies** en el primer acceso de la sesión: aceptarlo antes de scrapear.
- **`browser_wait_for` con timeout máximo 10 segundos.** Sin reintentos automáticos.
- **Throttling**: separar 1-2 s entre acciones para no levantar rate-limit.
- **Redirect de afiliación**: el botón "Ir a la oferta" pasa por un redirect. La URL canónica de tienda se resuelve siguiendo la navegación (`browser_evaluate("() => location.href")` o `browser_network_requests`), no extrayendo el `href` directo.
- **Selectores por accessibility tree** (rol + nombre accesible), nunca por CSS.
- **Sin Bash.** El sistema lo deniega globalmente.

Cualquier dominio o selector que demuestre ser inestable se registra en `knowledge/notas-degradacion.md`.

---

## Regla de capas entre subagentes

Patrón espejo del proyecto hermano: el orquestador (skill) **es el único** que lee guidelines, watchlists y orquesta pausas interactivas. Los subagentes son brazos con tools restringidos.

| Capa | Quién | Tools |
|---|---|---|
| Orquestación + filtrado editorial + dedupe | `buscar-ofertas` (skill) | Read, Write, sin Playwright ni WebFetch |
| Scraping de Chollometro | `aggregator-scraper` | Playwright (navigate, snapshot, wait_for, click, evaluate, network_requests, close) |
| Scraping de canales Telegram | `telegram-scraper` | WebFetch (sobre `t.me`, `chz.to` y dominios de tienda) |
| Enriquecimiento de tienda | `offer-enricher` | Playwright (navigate, snapshot, wait_for, take_screenshot, close) |

Los subagentes **no se llaman entre sí**. Solo el orquestador los invoca.

El filtrado editorial vive en el orquestador (es razonamiento puro sobre archivos ya leídos; separarlo como subagente añadiría handoff sin ganancia).

---

## Errores tipados

Mismo patrón que text-agents (prefijo ⚠️, mensaje literal al redactor, espera input):

- **`AggregatorBlockedError`** — Chollometro devuelve captcha o `browser_wait_for` agota timeout. El scraper devuelve la lista parcial (si la hay) con `degraded: true`. El orquestador avisa: *"He podido recuperar N candidatas antes del bloqueo. ¿Continúo con esas o aborto?"*. **Sin reintentos automáticos.**
- **`StoreBlockedError`** — al enriquecer, Amazon/AliExpress bloquea. Misma mecánica que `URLBlockedError` del hermano: el redactor pega la ficha manualmente; la inbox lleva `fuente: manual`.
- **`GuidelineMissingError`** — si el medio elegido no tiene guideline en text-agents. Mensaje literal: *"El medio '{medio}' no tiene guideline en text-agents. Crea primero la guideline allí con `/crear-guideline` y vuelve a lanzar."* **Detiene el flujo.**

---

## Convenciones de naming

- **Drafts en la inbox del hermano:** `DD-MM-YYYY-{slug-titulo}.md`. Slug en kebab-case sin acentos, máx 60 caracteres. Coincide con el patrón de `drafts/` del hermano.
- **Watchlists:** `WATCHLIST-{slug-kebab}.md` en `watchlists/`.
- **Historial:** `YYYY-MM-DD-sesion-{n}.md` en `historial/` (numérico para ordenación lexicográfica).
- **Changelog:** `changelog-YYYY-MM-DD.txt` en `changelog/`.

**Fechas:**
- `DD/MM/YYYY` en frontmatter visible al humano y en texto al redactor.
- `YYYY-MM-DD` solo en nombres de archivo donde la ordenación lex importa.

**Números:** estilo español, punto para miles y coma para decimales (`1.299,00 €`).

---

## Idioma

Todo el texto al redactor en **español** con ortografía y acentos correctos. Mensajes de error literales como aparecen en este documento.
