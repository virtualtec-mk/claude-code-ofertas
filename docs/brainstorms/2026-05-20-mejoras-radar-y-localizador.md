---
fecha: 20/05/2026
autor: Javier + Claude
tipo: brainstorm
origen: UAT end-to-end de /buscar-ofertas con radar_editorial como fuente principal
estado: borrador para discutir con el equipo
afecta_a:
  - radar_editorial (cambios principales)
  - claude-code-ofertas (cambios complementarios)
---

# Mejoras a radar_editorial y al localizador de ofertas

## Resumen ejecutivo

Hemos probado el flujo completo `/buscar-ofertas` end-to-end por primera vez contra el radar real. El radar respondió, devolvió candidatas, pero **ninguna de las 12 ofertas era enriquecible**: al abrir la primera Amazon mostraba pañales, la segunda una cafetera. El problema es estructural y nace en la ingesta del radar, no en el localizador.

Este documento propone las mejoras necesarias en cada capa, ordenadas por impacto.

---

## Qué hemos descubierto

El localizador le pide al radar "dame freidoras de Amazon", el radar devuelve 12 ofertas, y al intentar abrir la primera Amazon nos muestra un paquete de pañales. La segunda, una cafetera. Ninguna de las 12 era utilizable.

No es un fallo puntual. Es estructural: **el radar guarda los links de afiliación originales (`chz.to/...`, `michollo.app/...`) en vez del producto real de Amazon.** Esos links son rotatorios — cuando la oferta del día cambia, el link sigue activo pero apunta a otro producto. Como las ofertas del catálogo tienen una media de 12 días, casi todos los links ya han rotado a productos sin relación con el chollo original.

### Datos concretos del UAT

- Query: `store=amazon&q=freidora&limit=12&sort=score`.
- Resultados: 12 candidatas (de 21 disponibles tras filtros).
- Distribución de `product_url`:
  - amazon.es directo: **0/12**
  - chz.to (shortlink): 6/12
  - michollo (shortlink): 2/12
  - vacío: 4/12
- Calidad general del catálogo: 199/200 ofertas marcadas `stale`, 200/200 sin categoría, 177/200 sin `product_url`.
- Verificación en Amazon de las 2 primeras candidatas:
  - Bosch Serie 4 XL freidora → ASIN `B0FLX1D8G5` → muestra pañales Dodot.
  - Ninja MAX PRO freidora → ASIN `B0FX5FXFRX` → muestra cafetera Krups.

---

## Las 5 mejoras que harían que esto funcione

### 1. Que el radar guarde la URL real de Amazon, no el link de afiliación

**Lo más importante.** Hoy, cuando el radar captura un chollo, almacena el shortlink. Debería seguir el redirect en ese mismo momento, extraer el código ASIN del producto en Amazon, y guardar la URL definitiva del producto. El shortlink se mantiene aparte para tracking de comisiones, pero la URL "buena" es la canónica de Amazon.

**Por qué importa:** sin esto, cualquier oferta que tenga más de un par de días es inservible. Es la diferencia entre que el localizador funcione o no funcione.

**Dónde toca:** `apps/ingestion/services/adapters.py` en `radar_editorial`. Cada adapter (Hispachollos, Chollazos, Chollometro, Michollo) debe hacer un `requests.head(shortlink, allow_redirects=True)`, extraer ASIN con regex `r"/dp/([A-Z0-9]{10})"`, y guardar:

- `product_url`: `https://www.amazon.es/dp/{ASIN}` limpio, sin parámetros de afiliación.
- `affiliate_url` (campo nuevo): el shortlink original, útil internamente, nunca expuesto en la API pública.

Si el redirect no resuelve a un host `amazon.es` o `es.aliexpress.com`, marcar la oferta como incompleta y no publicarla.

---

### 2. Revisar ofertas viejas periódicamente y despublicar las muertas

El catálogo tiene **199 de 200 ofertas marcadas como "stale"**, lo que sugiere que la ingesta no corre desde hace tiempo. Y aunque se arregle el punto 1, las ofertas válidas hoy dejan de serlo en pocos días: el precio sube, se agota stock, Amazon cambia el ASIN.

Hace falta un proceso automático que cada cierto tiempo abra cada oferta, compruebe que el producto sigue siendo el mismo y el precio sigue siendo oferta, y la despublique si no.

**Por qué importa:** evita que el redactor pierda tiempo abriendo ofertas que ya no existen.

**Dónde toca:** un job programado en Railway (o un management command + cron) que itere ofertas con `status='pending'` o `last_seen_at` > N días, reabra cada `product_url`, compare el título extraído con el `title` ingestado, y marque `status='dead'` si divergen demasiado.

---

### 3. Que el buscador del radar sepa buscar de verdad

Hoy si pides `q=freidora robot aspirador cafetera`, el radar busca el texto literal completo y no encuentra nada. Tiene que buscar como Google: cada palabra cuenta, los resultados son los que contienen *alguna* de ellas, y se ordenan por relevancia. Postgres lo trae de serie con `SearchVector` y `SearchQuery`.

**Por qué importa:** ahora el operador tiene que adivinar la palabra exacta que más resultados va a devolver. Con búsqueda de verdad, una watchlist con varias keywords funciona en una sola consulta del localizador.

**Dónde toca:** la vista que sirve `/api/editorial/offers/`. Tokenizar el `q`, construir `SearchQuery` con operador `OR` por defecto, y ordenar por `SearchRank`. Mantener `sort=score` como override.

---

### 4. Eliminar duplicados en el radar

El mismo producto aparece 3-4 veces en los resultados porque chollazos, hispachollos, chollometro y michollo publicaron todos la misma oferta. El radar no las junta.

Si se arregla el punto 1 y se tiene el ASIN canónico, la deduplicación es trivial: una oferta = un ASIN, se queda la versión con más datos (precio anterior y descuento poblados) o la de mejor score.

**Por qué importa:** de 12 candidatas devueltas hoy, realmente había 5-6 productos distintos. El operador ve ruido y pierde tiempo.

**Dónde toca:** o un constraint `unique(amazon_asin)` en el modelo `Offer` con merge en ingesta, o un paso de dedup justo antes de servir el JSON.

---

### 5. Rellenar la categoría de las ofertas

Las 200 ofertas del catálogo tienen el campo `category` vacío. O el adapter de ingesta lo rellena con una heurística simple (palabras del título → categoría), o se elimina del schema porque no aporta nada.

**Por qué importa:** menor que los otros, pero el filtrado editorial mejora mucho si el operador puede pedir "dame solo cocina" o "dame solo audio" sin mirar título por título.

**Dónde toca:** un helper en `apps/ingestion/services/categorization.py` con un dict simple `{regex_titulo: categoria}` aplicado al guardar.

---

## Mejoras en el localizador (este lado)

Mientras el radar se arregla, hay dos cosas que se pueden hacer aquí para que el sistema sea más robusto **cuando el radar empiece a entregar bien**:

### A. Resolver el shortlink antes de pasarlo al enriquecedor

Hoy si llega un `chz.to/...`, el enriquecedor abre lo que sea que apunte ese link, aunque sea otro producto. Si se añade un paso intermedio de "sigue el redirect y mira si el producto resultante coincide con el título del chollo", evitamos los falsos positivos en el local incluso cuando el radar siga entregando shortlinks.

**Dónde toca:** `.claude/skills/buscar-ofertas/SKILL.md`, entre Paso 4 (validación) y Paso 5 (enricher), añadir un sub-paso 4.5.

### B. Que el enriquecedor avise si el título Amazon no encaja con el del chollo

Lo que hizo bien el enriquecedor hoy fue decir "esto que cargué no es la Bosch que me pediste". Eso fue por cómo redacté el prompt sobre la marcha, no porque la spec lo exigiera. Convertirlo en regla formal evita depender de la suerte.

**Dónde toca:** `.claude/agents/offer-enricher.md`. El orquestador le pasa también `titulo_radar`, y el enricher rechaza con error claro si los tokens significativos del título extraído no encajan con los del título recibido.

---

## Nota operativa para el equipo

El localizador, el radar y el writer son tres piezas separadas que se acoplan por convenciones (rutas, formato de fichas, nombres de campos). Cada vez que se cambia un nombre en un sitio, los otros dos lo notan. Hoy hemos descubierto eso por las malas: el repo hermano se renombró de `claude-code-text-agents` a `claude-code-writer` y media docena de archivos seguían apuntando al nombre viejo.

**Recomendación:** que cualquier rename o cambio de contrato entre los tres proyectos se documente en una nota corta compartida (un README en alguno de los repos, o un canal de Slack fijado), porque el siguiente que entre al código no va a saber por qué hay rutas mezcladas.

---

## Prioridad sugerida

| # | Mejora | Capa | Impacto | Esfuerzo |
|---|---|---|---|---|
| 1 | Resolver shortlinks en ingesta + guardar ASIN canónico | radar | Bloqueador | Medio |
| 2 | Revalidación periódica de ofertas | radar | Alto | Medio |
| 3 | Búsqueda multi-keyword en `q=` | radar | Alto | Bajo |
| 4 | Dedupe por ASIN canónico | radar | Medio | Bajo (depende de 1) |
| 5 | Rellenar categoría | radar | Bajo | Bajo |
| A | Resolver shortlink antes del enricher | localizador | Medio | Bajo |
| B | Coherencia título radar/Amazon | localizador | Medio | Bajo |

Si se ataca **solo el #1**, el localizador pasa de 0% candidatas enriquecibles a probablemente >80%. Es la mejora con mejor ratio impacto/esfuerzo.
