# Fuentes activas

Tabla maestra de agregadores de los que descubrimos ofertas. El orquestador `buscar-ofertas` lee este archivo para saber qué scrapers están vivos y a qué subagente delegar.

Si añades una fuente nueva, edita aquí Y crea/actualiza el subagente correspondiente. Si una fuente cae, márcala como `inactiva: true` antes de borrar nada — así el historial sigue siendo legible.

---

## Fuentes en MVP

| slug | tipo | URL base | anunciantes cubiertos | subagente | inactiva |
|---|---|---|---|---|---|
| `chollometro` | web (Playwright) | `https://www.chollometro.com/search/ofertas?merchant-id={ID}` | amazon (173), aliexpress (165) | `aggregator-scraper` | false |
| `telegram-hispachollos` | bridge web Telegram (WebFetch) | `https://t.me/s/hispachollos` | amazon, aliexpress (mezclados) | `telegram-scraper` | false |
| `telegram-chollazos` | bridge web Telegram (WebFetch) | `https://t.me/s/chollazos` | amazon, aliexpress (mezclados) | `telegram-scraper` | false |

---

## Notas por fuente

### chollometro
- Único filtro nativo por anunciante: parámetro `merchant-id` (Amazon=173, AliExpress=165).
- Selectores y mecánica del redirect: ver `knowledge/notas-degradacion.md` (scout 19/05/2026).
- Volumen por carga: 20-30 items por página.

### telegram-hispachollos / telegram-chollazos
- No hay filtro nativo por anunciante en el bridge. El subagente clasifica post a post resolviendo el shortener.
- Todos los enlaces salen con shortener **`chz.to/<slug>`**. La cadena tiene hasta 3 saltos y WebFetch NO sigue cross-host automáticamente — el subagente encadena llamadas:
  - Amazon: `chz.to` → `amzn.to` → `amazon.es/dp/<ASIN>`.
  - AliExpress: `chz.to` → `s.click.aliexpress.com` → `aliexpress.com/item/<ID>.html` (dominio GLOBAL, no `es.`; se acepta como `aliexpress-global` por equivalencia funcional para el redactor español).
- Volumen por carga: 15-20 posts recientes. Coste: ~45 WebFetches por canal.
- Precio visible en el texto del post (formato variable: "Precio oferta: 9,41€", "SOLO 119€", etc.). Lo parsea el subagente.

---

## Fuentes descartadas

- **Compradicción**: candidata si Chollometro endurece anti-bot o cambia el patrón de URLs. No activada.
- **Telegram @chollazoses, @ofertasinformaticas, etc.**: solapamiento alto con las dos ya activas; no se añaden hasta que el uso real demuestre que aportan cobertura única.
