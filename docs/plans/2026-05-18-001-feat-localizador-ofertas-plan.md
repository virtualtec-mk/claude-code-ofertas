---
title: Localizador de ofertas (estilo claude-code-text-agents)
type: feat
status: completed
date: 2026-05-18
origin: docs/brainstorms/2026-05-18-localizador-ofertas-requirements.md
---

# Localizador de ofertas (estilo claude-code-text-agents)

## Enhancement Summary

**Profundizado el:** 2026-05-18 con investigación de Chollometro (anti-bot, redirects), extracción de patrones de text-agents (frontmatter, errores tipados, naming, modelo), y revisión de simplicidad (YAGNI).

**Cambios clave respecto a la versión inicial:**
1. **Recorte agresivo del MVP**. Fuera: `config.json`, `fuentes.md` como tabla maestra con 1 sola fuente, skill `crear-watchlist`, subagente `editorial-filter`, dedupe/cooldown, motivos de rechazo como catálogo cerrado, doble pausa interactiva por candidata.
2. **Filtrado editorial dentro del orquestador**, no como subagente. Es razonamiento puro sobre archivos ya cargados; no toca tools restringidas.
3. **Paso 0 de scout en vivo** sobre Chollometro antes de implementar el scraper. Cloudflare bloquea WebFetch (HTTP 403 confirmado); hay que ir con Playwright headed, aceptar el banner de cookies y validar URLs y selectores reales.
4. **Mecánica de redirect**: el botón "Ir a la oferta" en Chollometro pasa por un redirect de afiliación. La URL canónica de Amazon/AliExpress se resuelve siguiendo `location.href` tras `browser_click` o leyendo `browser_network_requests`. No basta con extraer `href`.
5. **Convenciones text-agents alineadas**: naming de archivos `DD-MM-YYYY-{slug}.md`; subagentes declaran `model: claude-sonnet-4-6`; `browser_wait_for` con timeout 10 s explícito; carpeta `knowledge/notas-degradacion.md` para registrar dominios y patrones problemáticos.
6. **Schemas de inbox e historial recortados** a campos que se usan en MVP; el resto se añade si y cuando exista un consumidor real.
7. **Permisos limitados a `.es`**: `amazon.es` y `es.aliexpress.com` solamente (los redactores escriben para medios españoles).

## Overview

Construir un proyecto local operable desde Claude Code que descubre ofertas de Amazon España y AliExpress España en Chollometro, las filtra usando el guideline editorial del proyecto hermano `claude-code-text-agents`, deja que el redactor valide candidata a candidata y entrega las aprobadas como fichas listas en una carpeta inbox que el flujo de redacción existente puede consumir sin re-scrapear.

Replica el patrón de text-agents: skills como orquestadores (`disable-model-invocation: true`), subagentes en `.claude/agents/` con tools restringidos por capa, errores tipados con respuesta prescrita, frontmatter YAML en outputs, pausas interactivas obligatorias, todo en archivos locales sin DB ni panel.

## Problem Statement / Motivation

Los redactores ya redactan con text-agents pero el cuello de botella se ha movido **antes** del comando de redacción. Hoy buscan a mano en Chollometro y otros agregadores, descartan duplicados y sopesan si el descuento es real. Este proyecto cubre esa fase sin tocar el sistema de redacción y reutilizando sus guidelines como única fuente de verdad editorial.

Las decisiones de producto están cerradas en el documento origen (ver origin: `docs/brainstorms/2026-05-18-localizador-ofertas-requirements.md`).

## Proposed Solution

### Arquitectura

Dos subagentes en cadena, coordinados por una sola skill. El filtrado editorial vive en el orquestador (es razonamiento puro sobre archivos ya leídos, no necesita tools restringidos).

```
buscar-ofertas (skill orquestadora)
  ├─ Paso 1: medio + anunciante + (watchlist | descripción libre)  [interactivo]
  ├─ Paso 2: aggregator-scraper
  │     in:  https://www.chollometro.com/<ruta-tienda>   (URL hardcoded en el agent en MVP)
  │     out: lista mínima (título, precio, %dto, url tienda resuelta, fuente)
  ├─ Paso 3: filtro editorial inline en el orquestador
  │     lee: GUIDELINE-{medio}.md del proyecto hermano + watchlist (si aplica) + afinado
  │     reduce y ordena las candidatas con una línea de justificación por cada una
  ├─ Paso 4: presentación al redactor — una pausa por candidata
  │     opciones: validar (lanza enriquecimiento) | rechazar (nota libre opcional) | saltar
  ├─ Paso 5: por cada validada → offer-enricher
  │     in:  URL final de la tienda
  │     out: ficha enriquecida (mismo schema que product-researcher de text-agents)
  └─ Paso 6: escribe ficha en ../claude-code-text-agents/inbox/  +  línea en historial
```

### Estructura de directorios

```
claude-code-localizador-ofertas/
├── .claude/
│   ├── settings.json
│   ├── agents/
│   │   ├── aggregator-scraper.md
│   │   └── offer-enricher.md
│   └── skills/
│       └── buscar-ofertas/SKILL.md
├── watchlists/                       ← markdown editables a mano; sin skill propia
│   └── WATCHLIST-{slug}.md
├── historial/
│   └── YYYY-MM-DD-sesion-{n}.md
├── knowledge/
│   └── notas-degradacion.md          ← log libre de dominios/patrones problemáticos
├── docs/
│   ├── brainstorms/
│   ├── plans/
│   └── instalacion.txt
├── changelog/
│   └── changelog-YYYY-MM-DD.txt
├── CLAUDE.md
└── README.md
```

Reglas implícitas:
- La ruta al proyecto hermano se asume `../claude-code-text-agents/` y se documenta en `CLAUDE.md`. Si en el futuro el clon vive en otra ruta, se edita ahí. Sin `config.json`.
- Hay una sola fuente de descubrimiento en MVP: Chollometro. La URL base vive directamente en `aggregator-scraper.md`. Si entra una segunda fuente, se promueve a `fuentes.md`.
- Las watchlists se crean editando un .md de ejemplo. El orquestador puede ofrecer "¿guardo esta búsqueda afinada como watchlist?" al final de una sesión, pero no hay skill dedicada.

### Reutilización cross-proyecto

- `GUIDELINE-{medio}.md` se leen de `../claude-code-text-agents/guidelines/`. Cero duplicación.
- `medios.md` se lee también de allí (lista canónica de slugs).
- La inbox se escribe en `../claude-code-text-agents/inbox/`.
- El cambio en `/crear-articulo` de text-agents para consumir la inbox **queda fuera de este plan**; se entrega como PR-companion al otro repo.

## Technical Considerations

### Subagentes — frontmatter y tools

Mismo formato exacto que text-agents (`model: claude-sonnet-4-6` por defecto):

| Subagente | Tools permitidos | Excluido |
|---|---|---|
| `aggregator-scraper` | `mcp__plugin_playwright_playwright__browser_navigate`, `browser_snapshot`, `browser_wait_for`, `browser_click`, `browser_evaluate`, `browser_network_requests`, `browser_close` | Read, Write, todo lo editorial |
| `offer-enricher` | mismas Playwright tools que arriba (sin `browser_click`/`network_requests` si no son necesarios) + nada de Write | Read de guidelines (no los necesita) |

El orquestador (skill) sí usa Read sobre guidelines/watchlists e instruye los subagentes con texto.

### Realidad de Chollometro

- **Cloudflare delante.** `WebFetch` directo devuelve 403. Hay que ir con Playwright en modo headed (lo gestiona el plugin); Playwright headless puro suele caer.
- **Banner de cookies/consentimiento** al primer acceso de la sesión. Aceptarlo antes de scrapear; documentar en `aggregator-scraper.md` el orden: navigate → wait_for banner → click aceptar → snapshot.
- **Paginación clásica** con `?page=N`, no infinite scroll. MVP: solo página 1 (20-30 items).
- **Selectores por accessibility tree** (rol + nombre accesible), nunca por CSS. Cada item suele exponerse como `article` o `listitem` con heading del título.
- **Redirect de afiliación** en el botón "Ir a la oferta". Para obtener la URL canónica de Amazon/AliExpress, el agente debe: `browser_click` sobre el botón, esperar la navegación con `browser_wait_for`, leer `location.href` con `browser_evaluate("() => location.href")` o usar `browser_network_requests` para capturar la cadena de redirects y quedarse con el primer URL en `amazon.es` o `es.aliexpress.com`. Después `browser_navigate` de vuelta a la lista.
- **Throttling**: separar 1-2 s entre acciones para no levantar rate-limit.
- **Rutas exactas (a validar en scout)**: el patrón histórico de la red Pepper es `/grupo/<tienda>`. **No confirmado en vivo**: el Paso 0 del plan lo valida antes de hardcodearlo en el agent.

### Paso 0 — Scout en vivo (antes de implementar el scraper)

Una pasada interactiva con Playwright MCP **manual** (desde una sesión cualquiera, no como parte del producto) para confirmar:

1. URL real de "todas las ofertas de Amazon España" en Chollometro hoy.
2. URL real para AliExpress.
3. Selector accesible estable para: cada item, título, precio, % descuento, botón a tienda.
4. Mecánica exacta del redirect (¿abre nueva pestaña? ¿navega en la misma? ¿`browser_network_requests` lo captura?).
5. Texto literal del banner de cookies (para el `browser_click` por nombre accesible).
6. Si la ruta `/grupo/<tienda>` ya no existe, hallar la actual.

Salida del scout: una nota de 15-20 líneas en `knowledge/notas-degradacion.md` con las URLs y el orden exacto de pasos. Esa nota se traduce a las instrucciones del subagente.

### Permisos (`settings.json`)

```json
{
  "permissions": {
    "allow": [
      "WebFetch(domain:chollometro.com)",
      "WebFetch(domain:amazon.es)",
      "WebFetch(domain:es.aliexpress.com)",
      "Read(**)",
      "Read(../claude-code-text-agents/guidelines/**)",
      "Read(../claude-code-text-agents/medios.md)",
      "Write(watchlists/**)",
      "Write(historial/**)",
      "Write(knowledge/**)",
      "Write(changelog/**)",
      "Write(../claude-code-text-agents/inbox/**)",
      "Edit(watchlists/**)"
    ],
    "deny": [
      "Bash(*)",
      "Write(../claude-code-text-agents/guidelines/**)",
      "Write(../claude-code-text-agents/drafts/**)"
    ]
  }
}
```

### Schema de watchlist (markdown editable a mano)

```yaml
---
name: auriculares-anc-md
medio_sugerido: mundodeportivo
anunciante: amazon
keywords: [auriculares, ANC, cancelación]
marcas: [Sony, Bose, Sennheiser, Apple, JBL]
precio_min: 30
precio_max: 100
---

# Auriculares ANC para Mundo Deportivo

[Notas libres del editor]
```

No hay esquema de validación. Si un campo falta, el orquestador lo ignora.

### Frontmatter de la inbox (handoff a text-agents)

`../claude-code-text-agents/inbox/DD-MM-YYYY-{slug-producto}.md` (mismo formato de fecha que los drafts del proyecto hermano):

```yaml
---
medio: mundodeportivo
anunciante: amazon
url_producto: https://www.amazon.es/dp/B0XXXXXXXX
titulo: "Sony WH-1000XM5"
precio_actual: 279,00
descuento_pct: 30
vendedor: Amazon
fecha_validacion: 18/05/2026
nota_redactor: "Mínimo histórico verificable."
---

# Ficha enriquecida

[output completo del offer-enricher con el MISMO schema que produce
product-researcher de text-agents — precio actual y anterior, nivel de
confianza del descuento, descripción corta, especificaciones, reseñas]
```

Schema mínimo. ASIN, EAN, moneda, url_canonical, etc. se añaden si y cuando un consumidor real los necesite.

### Formato del historial (una línea por validación/rechazo)

`historial/2026-05-18-sesion-1.md`:

```yaml
---
fecha: 18/05/2026
medio: mundodeportivo
anunciante: amazon
watchlist: auriculares-anc-md
afinado: "solo Sony y Bose"
---

## Validadas
- https://www.amazon.es/dp/B0XX — Sony WH-1000XM4 — 199,00€

## Rechazadas
- https://www.amazon.es/dp/B0YY — descuento dudoso

## Saltadas
- https://www.amazon.es/dp/B0ZZ
```

Texto libre del redactor en la nota de rechazo. Sin catálogo cerrado en MVP.

### Errores tipados

Replicar el patrón exacto de text-agents (prefijo ⚠️, mensaje literal, espera input):

- **`AggregatorBlockedError`** — Chollometro devuelve captcha o el `browser_wait_for` agota timeout. El scraper devuelve la lista parcial (si la hay) con `degraded: true`. El orquestador avisa: "He podido recuperar N candidatas antes del bloqueo. ¿Continúo con esas o aborto?". Sin reintentos automáticos.
- **`StoreBlockedError`** — al enriquecer, Amazon/AliExpress bloquea. Mensaje y fallback manual igual que `URLBlockedError` de text-agents: el redactor pega la ficha; la inbox lleva `fuente: manual`.
- **`GuidelineMissingError`** — si el medio elegido no tiene guideline en text-agents. Mensaje exacto: "El medio '{medio}' no tiene guideline en text-agents. Crea primero la guideline allí con `/crear-guideline` y vuelve a lanzar." Detiene el flujo.

### Convenciones de naming

- Drafts de la inbox: `DD-MM-YYYY-{slug-titulo}.md` con slug en kebab-case sin acentos, máx 60 caracteres. Coincide con el patrón de `drafts/` en text-agents.
- Watchlists: `WATCHLIST-{slug-kebab}.md`.
- Historial: `YYYY-MM-DD-sesion-{n}.md` (numérico para ordenación).
- Fechas: `DD/MM/YYYY` en frontmatter visible al humano; `YYYY-MM-DD` solo en nombres de archivo donde la ordenación lex importa.

## System-Wide Impact

- **Interaction graph**: el orquestador llama scraper una vez y enricher una vez por candidata validada. Subagentes no se llaman entre sí. La inbox dispara sin acoplamiento el flujo de text-agents la siguiente vez que se ejecute `/crear-articulo`.
- **Error propagation**: errores tipados se traducen a mensajes ⚠️ al redactor con opción explícita de continuar/abortar. Excepciones no recuperables (Playwright MCP no instalado) producen mensaje claro, no traza técnica.
- **State lifecycle**: cada ficha validada se escribe a la inbox **inmediatamente** después de enriquecer con éxito. El historial se escribe al cierre normal de la sesión; si se interrumpe antes, queda perdido (aceptable: es métrica, no datos críticos).
- **Integration scenarios a verificar**:
  1. Sesión completa Amazon + mundodeportivo + watchlist → ≥1 ficha en inbox + historial coherente.
  2. Cookies de Chollometro caducadas/ausentes → scraper acepta el banner y continúa.
  3. Bloqueo en Chollometro a mitad de scraping → `AggregatorBlockedError` con lista parcial; redactor decide continuar.
  4. Bloqueo en Amazon al enriquecer una candidata → `StoreBlockedError`, redactor pega manualmente.
  5. Filtro editorial deja 0 candidatas → orquestador presenta las próximas 5 sin filtro marcadas como "fuera del foco editorial" y avisa.

## Acceptance Criteria

### Funcionalidad

- [ ] `/buscar-ofertas` lanzable como skill; pide medio + anunciante interactivamente si no se pasan como argumentos.
- [ ] Lista medios disponibles leyendo `../claude-code-text-agents/guidelines/GUIDELINE-*.md`.
- [ ] `GuidelineMissingError` si el medio no existe allí.
- [ ] Permite elegir watchlist existente o "ninguna / describir libre".
- [ ] Afinado conversacional aplicable sobre una watchlist en runtime ("solo Sony hoy") sin modificar el archivo.
- [ ] `aggregator-scraper` scrapea Chollometro filtrado por anunciante, acepta el banner de cookies, resuelve el redirect de afiliación a la URL final de la tienda, y devuelve 15-25 candidatas estructuradas.
- [ ] Orquestador aplica filtrado editorial inline usando guideline + watchlist + afinado, con una línea de justificación por candidata.
- [ ] Por candidata: pausa interactiva con validar / rechazar (nota libre opcional) / saltar.
- [ ] `offer-enricher` produce ficha en formato compatible con `product-researcher` de text-agents (mismos campos).
- [ ] Ficha validada escrita en la inbox del proyecto hermano antes de pasar a la siguiente candidata.
- [ ] Cierre de sesión: `historial/YYYY-MM-DD-sesion-N.md` + línea en `changelog/`.

### Calidad

- [ ] Subagentes con tools restringidos exactamente al subset declarado en su frontmatter.
- [ ] `Bash(*)` denegado en `settings.json`.
- [ ] `model: claude-sonnet-4-6` declarado en cada subagente.
- [ ] `browser_wait_for` con timeout máximo 10 segundos.
- [ ] El proyecto funciona aunque la ruta a text-agents no exista (error claro, no traceback).
- [ ] Todo el texto al redactor en español con ortografía correcta.

### Documentación

- [ ] `README.md` orientado al redactor, mismo estilo que el de text-agents.
- [ ] `CLAUDE.md` con: convención de carpetas, política de scraping, regla de capas entre subagentes, ubicación esperada de text-agents, errores tipados.
- [ ] `docs/instalacion.txt`: Playwright MCP, ubicación de text-agents, primera watchlist de ejemplo, orden recomendado de pasos.
- [ ] PR-companion a text-agents documentado en `docs/`.

## Implementation Phases

### Fase 0 — Scout en vivo de Chollometro (sin escribir código)

Sesión interactiva manual: abrir Chollometro con Playwright headed, validar URLs por tienda, confirmar selectores accesibles, mecánica del redirect, texto del banner. Salida: nota corta en `knowledge/notas-degradacion.md`. Sin esto, la fase 1 implementa a ciegas.

### Fase 1 — End-to-end mínimo con descubrimiento

Archivos:
- `CLAUDE.md`, `README.md`, `docs/instalacion.txt`
- `.claude/settings.json`
- `.claude/agents/aggregator-scraper.md` (URL hardcoded de Chollometro, validada en fase 0)
- `.claude/skills/buscar-ofertas/SKILL.md` (pasos 1, 2, 4, 6 — sin filtro inline, sin enricher; las "validadas" se anotan solo en historial)
- `knowledge/notas-degradacion.md`

Salida: el redactor ve una lista cruda filtrada por anunciante y la decisión queda en el historial. Sin handoff a inbox todavía.

### Fase 2 — Filtro editorial + enriquecimiento + handoff

Archivos:
- `.claude/agents/offer-enricher.md`
- `buscar-ofertas/SKILL.md` (añadir paso 3 inline + paso 5)

Coordinar con text-agents:
- Crear `../claude-code-text-agents/inbox/` con `.gitkeep`.
- Ampliar `settings.json` de text-agents para `Read(inbox/**)`.

Salida: ficha validada termina en la inbox lista para que `/crear-articulo` la consuma.

### Fase 3 — Watchlists y afinado

- Plantillas seed en `watchlists/` para `mundodeportivo` y `larazon`.
- Modificación del orquestador: paso 1 muestra watchlists y permite afinado conversacional; paso 3 lo aplica.

### Fase 4 — PR-companion a text-agents

- Modificación de `/crear-articulo` de text-agents para listar items en `inbox/` al inicio y saltar `product-researcher` cuando el redactor elige uno (la ficha ya está). Documentación en ambos proyectos. **Fuera del scope de este repo**; se entrega como cambio al otro.

(Fase 5 — dedupe, cooldown, motivos cerrados, métricas — diferida hasta que el uso real demuestre la necesidad.)

## Alternative Approaches Considered

- **`editorial-filter` como subagente separado.** Rechazado tras review de simplicidad: es razonamiento sobre archivos ya leídos por el orquestador. Separarlo añade un agent y un handoff sin ganancia.
- **`config.json` con la ruta a text-agents.** Rechazado: una constante en `CLAUDE.md` basta. text-agents no tiene config.json; introducirlo aquí es asimetría.
- **`fuentes.md` como tabla maestra desde el día 1.** Rechazado: con una sola fuente activa, la URL vive en el agent. Se promueve a tabla cuando entre la segunda fuente.
- **Skill `crear-watchlist`.** Rechazado: una watchlist es un .md con frontmatter; el redactor copia un ejemplo y edita. Si surge fricción real, se añade luego.
- **Dedupe contra historial + drafts en MVP.** Diferido: con volumen bajo y 1-2 redactores, es resolver un problema que aún no existe.
- **Catálogo cerrado de motivos de rechazo.** Diferido: en MVP el redactor escribe texto libre opcional. Estructurar cuando exista un consumidor del dato.
- **Llamar a `product-researcher` de text-agents en lugar de tener `offer-enricher`.** Rechazado: introduce dependencia cross-proyecto en runtime. Mantener un agente espejo con el mismo schema es más barato.

## Success Metrics

- Tiempo del redactor desde "empiezo a buscar" hasta "≥2 fichas en inbox" < 10 minutos en sesiones reales.
- 0 fichas validadas que requieran re-scrapear al pasar por text-agents.
- 0 falsos positivos por medio en piloto (filtro editorial es cero ruido).
- ≤1 captcha disruptivo por sesión.

## Dependencies & Risks

**Dependencias:**
- Playwright MCP instalado y operativo (ya prerrequisito de text-agents).
- `claude-code-text-agents` en `../claude-code-text-agents/`.
- Coordinación con el otro proyecto para crear `inbox/` y modificar `/crear-articulo` (fase 4).

**Riesgos:**
- **Chollometro endurece anti-bot.** Mitigación: scout en fase 0 documenta el estado; si en algún momento Playwright headed deja de pasar Cloudflare, se promociona `fuentes.md` y se añade Compradicción como alternativa (confirmada activa en 2026).
- **Cambio en la mecánica del redirect.** Mitigación: `browser_network_requests` es más robusto que parsear `href` y aguanta cambios de la página.
- **Rutas relativas en Windows.** El redactor debe abrir Claude Code desde la raíz del localizador. Documentado explícitamente en `docs/instalacion.txt`.
- **Filtro inline en el orquestador se vuelve grande con muchos medios.** Si llega ese punto, extraer a subagente; hoy es prematuro.

## Sources & References

### Origen
- **Documento origen:** [docs/brainstorms/2026-05-18-localizador-ofertas-requirements.md](../brainstorms/2026-05-18-localizador-ofertas-requirements.md). Decisiones heredadas: fuente = solo agregadores; búsqueda en dos fases; medio dirige filtrado desde el inicio; handoff vía inbox; todo local sin DB ni panel.

### Referencias internas (proyecto hermano)
- `claude-code-text-agents/CLAUDE.md` — convenciones, política de scraping, regla de capas.
- `claude-code-text-agents/.claude/skills/crear-articulo/SKILL.md` — patrón de orquestador.
- `claude-code-text-agents/.claude/agents/product-researcher.md` — patrón de subagente con Playwright y `URLBlockedError`. Schema espejeado en `offer-enricher`.
- `claude-code-text-agents/.claude/settings.json` — patrón de permisos restrictivos.
- `claude-code-text-agents/medios.md` — slugs de medios disponibles.
- `claude-code-text-agents/knowledge/notas-degradacion.md` (si existe) — patrón a replicar para registrar dominios problemáticos.

### Referencias externas
- Estructura de Chollometro / red Pepper en 2026 — calibrar en fase 0.
- Cloudflare anti-bot: requiere Playwright headed + cookies + throttling humano.

### Trabajos relacionados
- `Proyecto analizador de ofertas/00_ideas_brainstorm.md` — ideas editoriales reutilizadas (watchlists, score editorial, motivos estructurados).
- `Proyecto analizador de ofertas/01_modelo_datos_minimo.md` — entidades Product/Offer adaptadas como markdown estructurado (versión recortada).
