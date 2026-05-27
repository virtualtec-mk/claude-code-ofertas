# claude-code-ofertas

Repo unificado de **descubrimiento + redacción** de artículos de oferta para Amazon España y AliExpress España. Operable desde Claude Code con cuatro comandos:

- `/buscar-ofertas` — descubrir, filtrar, validar y enriquecer ofertas → ficha en `inbox/`.
- `/crear-articulo` — redactar el artículo desde una URL o desde el inbox.
- `/crear-guideline` — crear o actualizar una guideline editorial por medio.
- `/importar-gpt` — importar un GPT personalizado al formato guideline.

Antes existía como dos repos separados (`claude-code-ofertas` + `claude-code-writer`). Se fusionaron el 27/05/2026 para usarlos en la misma sesión y simplificar el handoff. Ver [`docs/plans/2026-05-27-merge-ofertas-writer.md`](docs/plans/2026-05-27-merge-ofertas-writer.md).

---

## Flujo end-to-end

1. **Descubrir.** `/buscar-ofertas {medio} {amazon|aliexpress} [watchlist]`. El sistema consulta `radar_editorial`, filtra contra la guideline del medio y te presenta candidatas una a una. Validas con V/R/S/Q.
2. **Enriquecer.** Cada validada se enriquece automáticamente (precio actual, precio anterior, confianza del descuento, reseñas, specs) y aterriza en `inbox/DD-MM-YYYY-{slug}.md`.
3. **Redactar.** `/crear-articulo {medio} {filtro}` busca en `inbox/`, o `/crear-articulo {URL} {medio}` va directo a una URL. El writer aplica guideline + persona-redactora y deja el draft en `drafts/{medio}/`.
4. **Publicar.** Copias el draft al CMS de tu medio.

---

## Cómo usarlo

```
/buscar-ofertas larazon aliexpress xiaomi
/crear-articulo larazon xiaomi
/crear-articulo https://www.amazon.es/dp/B0XYZ123 larazon
/crear-guideline nuevomedio
```

Detalles de cada skill en `.claude/skills/*/SKILL.md`.

### Auto-pull

Al iniciar la sesión, el hook `SessionStart` hace `git pull --ff-only` y avisa si hay cambios. Si no tienes conexión o hay conflictos locales, te lo dice y continúa sin bloquear.

---

## Estructura mínima

```
.claude/skills/       ← buscar-ofertas, crear-articulo, crear-guideline, importar-gpt
.claude/agents/       ← 9 subagentes (4 de descubrimiento + 5 de redacción)
.claude/hooks/        ← session-start-pull.sh
guidelines/           ← voz editorial por medio
watchlists/           ← listas temáticas
inbox/                ← handoff descubrimiento → redacción
drafts/{medio}/       ← output del writer
historial/            ← sesiones de /buscar-ofertas
knowledge/            ← manifiesto, frases vetadas, personas, ejemplos publicados
docs/                 ← brainstorms, plans, qa, instalación
```

Visión completa en [`CLAUDE.md`](CLAUDE.md).

---

## Requisitos

- **Claude Code** instalado.
- **Plugin Playwright MCP** activo.
- **Variables de entorno de `radar_editorial`** en `.env`:
  ```
  RADAR_BASE_URL=https://...
  RADAR_AGENT_API_TOKEN=...
  ```
  Copia `.env.example` → `.env` y rellena. El `.env` está en `.gitignore`.

Guía paso a paso: [`docs/instalacion.txt`](docs/instalacion.txt) y [`docs/configuracion-local-radar.txt`](docs/configuracion-local-radar.txt).

---

## Qué NO hace

- No mantiene base de datos ni panel web. Todo es markdown local.
- No deduplica contra el historial en MVP.
- No reintenta scraping automáticamente cuando Cloudflare bloquea.
- No publica en el CMS del medio (el draft sale en `drafts/`).

---

## Historial

Cambios diarios en `changelog/changelog-YYYY-MM-DD.txt`. Sesiones de `/buscar-ofertas` en `historial/YYYY-MM-DD-sesion-{n}.md`.
