---
fecha: 20/05/2026
sesion: UAT-radar-1
medio: larazon
anunciante: amazon
watchlist: pequeno-electrodomestico-larazon
query_radar: "freidora"
total_radar: 21
candidata_problematica:
  radar_offer_id: (titulo "Bosch - Freidora de aire Serie 4 XL 6,1L")
  source: hispachollos
  url_origen: https://t.me/hispachollos/...
  product_url_radar: https://chz.to/c3ba3
  product_url_resuelto: https://www.amazon.es/dp/B0FLX1D8G5
  asin: B0FLX1D8G5
  producto_real_en_amazon: "Pañales Dodot, 49,99 €"
tipo_diagnostico: shortlink_apunta_a_producto_distinto
---

## Resumen

El radar tenia una candidata bien titulada (Bosch Serie 4 XL freidora) pero
el product_url (shortlink chz.to/c3ba3) tras seguir redirects aterriza en
un ASIN de Amazon que actualmente es Pañales Dodot. La oferta original era
real (probablemente publicada en hispachollos hace varios dias) pero el
shortlink se ha invalidado o repurposado.

## Recomendaciones para radar_editorial

1. Considerar guardar el ASIN extraido de la primera resolucion como campo
   estable (`amazon_asin`) ademas del shortlink, para detectar drift.
2. Marcar `stale=true` mas agresivamente cuando `last_seen_at` supere los
   N dias (en este catalogo, 199/200 ofertas ya estan stale).
3. Revalidar shortlinks periodicamente comparando el titulo extraido del
   producto final contra el `title` registrado por el adaptador semilla.

---

## Patron sistemico detectado tras 2 candidatas

Tras enriquecer 2 candidatas del Top-12 (Bosch + Ninja), ambas resolvieron
a productos distintos:

- Bosch Serie 4 XL freidora → ASIN B0FLX1D8G5 → Pañales Dodot 49,99 €
- Ninja MAX PRO freidora    → ASIN B0FX5FXFRX → Cafetera Krups EA9109OM

Distribucion de product_url en el Top-12 entero:

  - amazon.es directo: 0/12
  - chz.to (shortlink):  6/12
  - michollo (shortlink): 2/12
  - vacio: 4/12

Conclusion: el radar esta devolviendo redirectores de afiliacion rotatorios
(chz.to de Hispatablet, a.michollo.app/.to de Michollo) en vez de URLs
canonicas amazon.es/dp/{ASIN}. Cuando la ingesta es antigua (199/200
ofertas marcadas stale), esos shortlinks ya han rotado al chollo del dia
siguiente y apuntan a productos distintos.

## Recomendacion accionable para radar_editorial

En `apps/ingestion/services/adapters.py`, los adapters de Hispachollos,
Chollazos, Chollometro y Michollo deben:

1. Al capturar una candidata, hacer un GET con redirect-follow sobre el
   shortlink de afiliacion para obtener la URL final de Amazon.
2. Extraer el ASIN (patron `/dp/[A-Z0-9]{10}`) y normalizar a
   `https://www.amazon.es/dp/{ASIN}` (sin parametros de afiliacion).
3. Guardar:
   - `product_url`: la URL canonica `https://www.amazon.es/dp/{ASIN}`.
   - `affiliate_url` (nuevo campo opcional): el shortlink original, util
     para tracking interno pero NUNCA expuesto via API.
4. Si el redirect no devuelve un host amazon.es, marcar la candidata como
   `incomplete_fields: ['product_url_unresolved']` y NO publicarla en
   `/api/editorial/offers/`.

Sin esta fix, el UAT muestra que el catalogo del radar es inutil para el
flujo /buscar-ofertas: cero candidatas son enriquecibles.
