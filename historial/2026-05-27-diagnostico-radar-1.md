---
fecha: 27/05/2026
tipo: diagnostico-radar
medio: larazon
anunciante: aliexpress
watchlist: (descripcion libre)
query_libre: "móviles POCO"
afinado: ""
fuente_descubrimiento: radar_editorial
resultado: RadarUnavailableError
total_candidatas: 0
---

# Diagnóstico radar_editorial — 27/05/2026

## Contexto de la sesión

- Skill: `/buscar-ofertas`
- Args invocados: `larazon  móviles POCO`
- Medio resuelto: `larazon` (guideline existente)
- Anunciante resuelto interactivamente: `aliexpress`
- Watchlist: ninguna seleccionada. Se usa descripción libre `móviles POCO` (smartphones marca Xiaomi POCO, cualquier modelo en oferta).
- Afinado: ninguno

## Síntoma

`radar-catalog-client` devolvió `RadarUnavailableError`. Tras verificación manual con `curl` y `RADAR_AGENT_API_TOKEN` válido contra `RADAR_BASE_URL = https://web-production-6fbc3.up.railway.app/`:

| Ruta probada | HTTP |
|---|---|
| `/health/` | **200** `{"status": "ok"}` |
| `/healthz` | 404 |
| `/api/health` | 404 |
| `/api/` | 404 |
| `/api/offers/` | 404 |
| `/offers/` | 404 |
| `/editorial/offers/` | 404 |
| `/api/editorial/offers/` | 404 |
| `/docs` | 404 |
| `/openapi.json` | 404 |

El servicio responde (health 200), pero ninguna ruta de catálogo conocida está expuesta. El subagente `radar-catalog-client` apunta por defecto a `/api/editorial/offers/` (definición vigente en `.claude/agents/radar-catalog-client.md`).

## Hipótesis

1. La aplicación desplegada en este `RADAR_BASE_URL` no es la build esperada del radar editorial (puede ser un servicio distinto compartiendo dominio Railway).
2. La ruta del catálogo cambió en una release reciente del radar y `radar-catalog-client` quedó desactualizado.
3. El despliegue solo tiene healthcheck y aún no expone el API.

## Acción recomendada (fuera del scope de este repo)

- Verificar en `radar_editorial` cuál es la ruta canónica vigente del catálogo y si requiere autenticación distinta a `Bearer`.
- Actualizar `RADAR_BASE_URL` en `.env` o el path del endpoint en `.claude/agents/radar-catalog-client.md` para que vuelvan a converger.
- Hasta entonces, `/buscar-ofertas` no puede operar contra `radar_editorial`.

## Resultado para esta sesión

- `CANDIDATAS_BRUTAS = 0`
- No se invoca `aggregator-scraper` ni `telegram-scraper` (regla del orquestador: no hay fallback automático a scrapers).
- No se escribe nada en `inbox/`.
- No se genera nueva watchlist.
