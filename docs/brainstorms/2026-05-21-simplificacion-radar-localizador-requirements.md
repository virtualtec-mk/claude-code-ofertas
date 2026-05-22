---
date: 2026-05-21
topic: simplificacion-radar-localizador
origen: docs/2026-05-20-mejoras-radar-y-localizador.md (UAT end-to-end /buscar-ofertas)
afecta_a:
  - radar_editorial (cambios principales)
  - claude-code-localizador-ofertas (cambios complementarios)
---

# Simplificación del radar y el localizador de ofertas

## Problem Frame

El UAT del 20/05/2026 demostró que **0 de 12 ofertas entregadas por el radar eran enriquecibles**. Causa raíz: el radar persiste shortlinks de afiliación (`chz.to/...`, `michollo.app/...`) que rotan a otros productos pasados pocos días. Con una edad media de catálogo de 12 días, casi todos los enlaces ya apuntan a productos no relacionados.

El documento de origen propone 7 mejoras. Este brainstorm las cribra con criterio YAGNI y añade un techo de frescura para reducir superficie de problema antes de añadir lógica.

**Quién se ve afectado:** el redactor (operador del localizador) pierde tiempo abriendo ofertas inservibles. El sistema entero queda inoperante hasta resolverlo.

## Requirements

- **R1. TTL duro de 10 días en el radar.** Toda oferta cuyo `first_seen_at` supere 10 días debe desaparecer del catálogo activo (DELETE en BD, no soft-delete). La API pública solo sirve ofertas dentro de la ventana.
- **R2. Resolución de shortlink → ASIN canónico en ingesta del radar.** Al capturar un chollo, el adapter sigue el redirect del shortlink, extrae el identificador de producto (ASIN para Amazon, item ID para AliExpress) y persiste la URL canónica limpia como `product_url`. El shortlink original se conserva aparte (`affiliate_url`), nunca se expone en la API pública. Si el redirect no resuelve a `amazon.es` o `es.aliexpress.com`/`aliexpress.com`, la oferta no se publica.
- **R3. Búsqueda multi-keyword + filtros estructurados en `/api/editorial/offers/`.** El parámetro `q=` debe tokenizar y construir consulta con operador OR por defecto, ordenando por relevancia. La API debe aceptar además filtros estructurados: `price_max`, `price_min`, `discount_min`, `store`. Mantener `sort=score` como override.
- **R4. Validación de coherencia título radar/Amazon en el enricher del localizador.** El orquestador pasa `titulo_radar` al `offer-enricher`. El enricher rechaza con error claro (`StoreMismatchError` o similar) si los tokens significativos del título extraído de la tienda no encajan con los del título recibido del radar. Red de seguridad para los casos en que R2 falle puntualmente.

## Success Criteria

- Tras aplicar R1+R2, ≥80% de las candidatas servidas por el radar son enriquecibles en una pasada del localizador (vs. 0% en el UAT).
- Una watchlist con varias keywords (p.ej. `móvil OR smartphone OR teléfono`) devuelve resultados relevantes en una única consulta del localizador.
- Una consulta tipo `store=amazon&q=zapatillas hombre&price_max=50` devuelve solo ofertas que cumplen los tres criterios.
- El catálogo activo no contiene ofertas con `first_seen_at` > 10 días en ningún momento.

## Scope Boundaries

- **El panel del radar se deja tal cual.** No se simplifica la UI ni se eliminan las secciones de redacción/selección de ofertas que ya no se usan. Decisión consciente: aplazado a una fase posterior.
- **No se mantiene histórico de ofertas expiradas.** Borrado duro. Si en el futuro se necesita histórico, se añadirá entonces (YAGNI).
- **No se añade dedupe por ASIN** (#4 del doc original). Con R2 + R1, el ruido por duplicados es manejable; añadir constraint `unique` y lógica de merge es complejidad opcional. Reconsiderar solo si el operador reporta exceso de duplicados en uso real.
- **No se rellena el campo `category`** (#5 del doc original). Impacto bajo confirmado por el propio doc. Se deja vacío o se elimina del schema si estorba.
- **No se añade resolución de shortlink en el localizador** (#A del doc original). Redundante si R2 está en su sitio.
- **No se implementa búsqueda semántica con embeddings.** Para catálogo ≤200 ofertas y queries categóricas tipo watchlist, full-text + filtros estructurados es estrictamente suficiente y evita infra recurrente (modelo de embeddings, pgvector). Reconsiderar solo si el catálogo crece a miles de ofertas o aparece la necesidad de buscar por intención abstracta.
- **No se implementa revalidación periódica abriendo cada URL** (#2 del doc original, en su forma compleja). El TTL duro de R1 cubre el caso al 95% sin coste de mantenimiento.

## Key Decisions

- **TTL 10 días con borrado duro en lugar de revalidación activa.** Razón: simplifica el job de mantenimiento de "abrir cada URL, comparar título, marcar dead" a un simple `DELETE WHERE first_seen_at < NOW() - INTERVAL '10 days'`. Aceptamos perder ofertas válidas que duren más de 10 días a cambio de eliminar una capa entera de complejidad.
- **Resolución de shortlinks en el radar, no en el localizador.** Razón: el problema raíz es que los enlaces rotan; resolverlos en consulta no ayuda si el shortlink original ya rotó tiempo atrás. Resolver en ingesta los captura cuando aún apuntan al producto correcto.
- **Full-text Postgres en lugar de búsqueda semántica.** Razón: las queries reales del operador son categóricas (keyword + filtros), no de intención. La semántica añadiría coste e infra sin valor proporcional para este tamaño de catálogo.
- **Defensa en profundidad mínima vía R4.** Razón: R2 puede fallar puntualmente (redirects raros, dominios nuevos). R4 es una validación barata en el localizador que evita falsos positivos sin duplicar lógica.

## Dependencies / Assumptions

- R4 depende parcialmente de R2: si el radar sigue entregando shortlinks, R4 aún funciona pero el enricher cargará la URL equivocada antes de detectar el mismatch. Coste tolerable.
- R1 requiere asegurar que la ingesta corre con frecuencia suficiente (≤24 h) para que el catálogo activo no se vacíe entre runs.
- R3 asume que el modelo `Offer` ya tiene los campos `current_price`, `discount_percentage` y `store` indexados o indexables sin migración compleja.

## Outstanding Questions

### Resolve Before Planning

_(ninguna)_

### Deferred to Planning

- [Afecta R1][Técnico] ¿El TTL se aplica vía constraint + job programado, o solo en la query que sirve la API (filter en runtime)? Decisión menor con impacto en limpieza de BD.
- [Afecta R2][Necesita investigación] AliExpress: ¿el redirect del shortlink resuelve siempre a `item/<ID>.html`, o hay variantes (`.../store/...`, mobile URLs) que haya que normalizar?
- [Afecta R3][Técnico] Configuración del diccionario de stemming en español para `SearchVector` y manejo de queries con tokens muy comunes (stopwords).
- [Afecta R4][Técnico] Definición precisa del "tokens significativos no encajan" — ¿match por intersección mínima de N tokens, similitud Jaccard, otro? Mejor decidirlo en planning con casos reales.
- [Afecta cross-repo][Operativa] Convención compartida entre radar/localizador/writer para renames y cambios de contrato (la nota operativa del doc original). Definir si vive como README en uno de los repos o canal fijado.

## Next Steps

→ `/ce:plan` para estructurar el plan de implementación (probablemente dos planes paralelos: uno en `radar_editorial` para R1+R2+R3 y otro en este repo para R4).
