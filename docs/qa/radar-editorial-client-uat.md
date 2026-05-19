# UAT - Cliente radar editorial

Fecha: 19/05/2026

- [ ] Con token valido, una respuesta JSON con dos ofertas se transforma en candidatas YAML con `fuente: radar_editorial`.
- [ ] Una oferta sin `product_url` queda marcada en `campos_incompletos` y no se inventa URL.
- [ ] Un 401/403 del radar se comunica como `RadarConfigError`.
- [ ] Una respuesta vacia con `diagnostics` se transmite al orquestador sin activar scrapers locales.
- [ ] Cada candidata conserva `radar_offer_id`, `url_origen` y `fuente_original`.
