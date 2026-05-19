# Localizador de ofertas

Proyecto hermano de `claude-code-text-agents`. **Encuentra ofertas, las filtra contra el guideline del medio y deja la ficha lista para redactar.**

Operable desde Claude Code con un solo comando: `/buscar-ofertas`.

---

## Para qué sirve

El cuello de botella en el flujo editorial ya no está en redactar (eso lo cubre el otro proyecto), sino en **encontrar** ofertas que merezcan un artículo. Hoy buscas a mano en Chollometro, descartas duplicados y sopesas si el descuento es real. Este proyecto hace ese trabajo por ti:

1. Tú dices: medio + anunciante + (opcional) watchlist o descripción libre.
2. El sistema scrapea Chollometro filtrando por el anunciante elegido.
3. Aplica el guideline editorial del medio y reduce la lista a las que tienen sentido editorial.
4. Te pasa una por una: validar / rechazar / saltar.
5. Las validadas se enriquecen (precio histórico, reseñas, especificaciones) y aterrizan en la inbox del proyecto de redacción.

La próxima vez que ejecutes `/crear-articulo` en `claude-code-text-agents`, las fichas estarán ahí, sin re-scrapear.

---

## Cómo usarlo

```
/buscar-ofertas
```

Sin argumentos. La skill te pregunta interactivamente medio, anunciante y watchlist. Opcionalmente:

```
/buscar-ofertas mundodeportivo amazon
/buscar-ofertas mundodeportivo amazon auriculares-anc-md
```

### Flujo típico

1. **Pre-vuelo**: te muestra medios disponibles (leídos del proyecto hermano) y watchlists.
2. **Afinado conversacional**: puedes decir "hoy solo Sony y Bose" sin tocar el archivo de watchlist.
3. **Scraping**: 15-25 candidatas brutas de Chollometro.
4. **Filtrado editorial inline**: cada candidata con una línea de justificación contra el guideline.
5. **Pausa por candidata**: validar / rechazar (con nota libre opcional) / saltar.
6. **Enriquecimiento**: por cada validada, ficha completa con precio anterior, nivel de confianza del descuento, reseñas.
7. **Handoff**: ficha en `../claude-code-text-agents/inbox/`.
8. **Cierre**: historial de la sesión + línea en changelog.

---

## Estructura

- `.claude/skills/buscar-ofertas/SKILL.md` — orquestador.
- `.claude/agents/aggregator-scraper.md` — scraping de Chollometro.
- `.claude/agents/offer-enricher.md` — enriquecimiento de Amazon/AliExpress.
- `watchlists/` — listas temáticas editables a mano.
- `historial/` — una sesión por archivo.
- `knowledge/notas-degradacion.md` — log de dominios/patrones problemáticos.
- `changelog/` — bitácora de cambios al proyecto.

---

## Requisitos

- **Claude Code** instalado.
- **Plugin Playwright MCP** activo (ya requerido por el proyecto hermano).
- **`claude-code-text-agents` clonado en `../claude-code-text-agents/`** con guidelines.

Detalles en [`docs/instalacion.txt`](docs/instalacion.txt).

---

## Qué NO hace este proyecto

- No redacta artículos (lo hace el hermano).
- No mantiene base de datos ni panel web. Todo es markdown local.
- No deduplica contra el historial en MVP (volumen bajo no lo justifica).
- No reintenta scraping automáticamente cuando Cloudflare bloquea.
