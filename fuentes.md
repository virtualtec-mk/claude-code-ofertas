# Fuentes activas

Tabla maestra de fuentes de descubrimiento. El orquestador `buscar-ofertas` usa `radar_editorial` como fuente principal y deja los scrapers directos como reserva manual/diagnostica.

Si anades una fuente nueva, edita aqui y crea/actualiza el subagente correspondiente. Si una fuente cae, marcala como `inactiva: true` antes de borrar nada para que el historial siga siendo legible.

---

## Fuentes en MVP

| slug | tipo | URL base | anunciantes cubiertos | subagente | inactiva |
|---|---|---|---|---|---|
| `radar_editorial` | API JSON autenticada | `/api/editorial/offers/` en Railway | amazon, aliexpress | `radar-catalog-client` | false |
| `chollometro` | web (Playwright) | `https://www.chollometro.com/search/ofertas?merchant-id={ID}` | amazon (173), aliexpress (165) | `aggregator-scraper` | true |
| `telegram-hispachollos` | bridge web Telegram (WebFetch) | `https://t.me/s/hispachollos` | amazon, aliexpress | `telegram-scraper` | true |
| `telegram-chollazos` | bridge web Telegram (WebFetch) | `https://t.me/s/chollazos` | amazon, aliexpress | `telegram-scraper` | true |

---

## Notas por fuente

### radar_editorial
- Fuente principal. Centraliza ingesta, normalizacion, score, calidad de fuentes y diagnosticos.
- Requiere configurar `RADAR_BASE_URL` y `RADAR_AGENT_API_TOKEN` para el subagente `radar-catalog-client`.
- Si una consulta devuelve cero resultados o campos incompletos, se registra como mejora del radar. No se compensa con scraping local automatico.

### chollometro
- Reserva manual/diagnostica. No se invoca en el flujo normal de `/buscar-ofertas`.
- Mantiene el conocimiento validado el 19/05/2026 para investigar cambios de maquetacion o cobertura.

### telegram-hispachollos / telegram-chollazos
- Reserva manual/diagnostica. No se invocan en el flujo normal de `/buscar-ofertas`.
- Siguen documentados porque pueden servir para auditar si el radar esta perdiendo cobertura de canales semilla.

---

## Fuentes descartadas

- **Compradiccion**: candidata si el radar incorpora nuevas semillas, pero no se activa desde este repo.
