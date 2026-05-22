---
title: Simplificación radar + localizador (R4 local + contrato cross-repo)
type: feat
status: completed
date: 2026-05-21
origin: docs/brainstorms/2026-05-21-simplificacion-radar-localizador-requirements.md
---

# Simplificación radar + localizador (R4 local + contrato cross-repo)

## Overview

El UAT del 20/05/2026 reveló que el flujo `/buscar-ofertas` produce 0% de ofertas enriquecibles por culpa de shortlinks de afiliación que rotan en el catálogo del radar. El [requirements doc del 21/05/2026](../brainstorms/2026-05-21-simplificacion-radar-localizador-requirements.md) acotó las mejoras del documento original a 4 requirements: **R1 (TTL 10 días con borrado duro)**, **R2 (resolver ASIN canónico en ingesta del radar)**, **R3 (búsqueda full-text + filtros estructurados)** y **R4 (validación de coherencia título radar/tienda en el enricher local)**.

Este plan cubre **R4 en detalle** porque es la única requirement implementable en este repo (`claude-code-localizador-ofertas`). R1/R2/R3 viven en `radar_editorial` y se ejecutarán con un plan paralelo en aquel repo; aquí se documenta solo el **contrato cross-repo** que ese plan debe satisfacer.

## Problem Statement / Motivation

Hoy el `offer-enricher` abre cualquier URL que le pase el orquestador y devuelve la ficha del producto que encuentre — aunque sea el equivocado. En el UAT, el redactor solo evitó el desastre porque, mientras revisaba, le pidió al enricher de forma ad hoc *"comprueba si esto es la Bosch que te pedí"* y el enricher detectó el mismatch. Esa salvaguarda fue ortográfica, no estructural. R4 la convierte en regla del agente.

R4 es la **red de seguridad** que protege al operador cuando R2 falle puntualmente (redirects raros, dominios nuevos, latencia transitoria en ingesta), y es útil **incluso antes de que R2 esté hecho**, porque detecta el caso degenerado del UAT (shortlink rotado a un producto sin relación).

## Proposed Solution

Modificar `offer-enricher` para que:

1. Reciba `titulo_radar` como **input adicional obligatorio** (hoy solo recibe la URL).
2. Tras navegar y extraer el título de la página de la tienda, ejecute un **paso de coherencia** entre `titulo_radar` y `titulo_tienda` usando un algoritmo de matching por **tokens de identidad**.
3. Si no hay match, devuelva `StoreMismatchError` con el detalle (sin escribir nada a inbox).

Modificar la skill `buscar-ofertas` para que:

1. Pase `titulo_radar` al enricher al invocarlo.
2. Capture `StoreMismatchError`, lo presente al redactor en una pausa interactiva, y permita **saltar (recomendado)**, **rechazar con motivo** o **forzar** (override consciente del operador).
3. Registre los mismatches en el historial y el changelog como diagnóstico para mejorar la ingesta del radar.

El matching es lógica pura (sobre cadenas), no requiere Playwright adicional ni red. Coste de ejecución: despreciable.

## Technical Approach

### Algoritmo de matching por tokens de identidad

Diseño en dos niveles:

**Nivel 1 — Fast path estructural (cuando R2 esté hecho):**
- Si el orquestador puede pasar `asin_esperado` y la URL canónica de la tienda contiene ese identificador, **match automático**. Se omite el nivel 2.
- Si la tienda es AliExpress, equivalente con el `item_id` extraído de `item/<ID>.html`.

**Nivel 2 — Matching por tokens (siempre activo como fallback):**

1. **Normalización** de ambos títulos:
   - Lowercase, sin acentos (NFKD → ASCII), colapso de espacios.
   - Elimina puntuación salvo guiones internos a alfanuméricos (`wh-1000xm5` se conserva como un solo token).
   - Tokeniza por espacios.
2. **Filtrado de stopwords** en español + ruido genérico de marketplaces: `de, la, el, con, para, y, en, a, las, los, un, una, por, sin, oferta, chollo, descuento, gratis, envio, nuevo, original, premium, version, pack`.
3. **Identificación de tokens de identidad** (los que importan para decidir si es el mismo producto). Un token es de identidad si cumple cualquiera de:
   - Aparece en mayúscula inicial en el título original (probable marca o nombre propio).
   - Contiene al menos un dígito (probables modelos: `xm5`, `4xl`, `pro7`).
   - Tiene 4+ caracteres y no es stopword ni adjetivo común.
4. **Decisión:**
   - `match` si la intersección de tokens de identidad entre radar y tienda tiene al menos **2 elementos**, O al menos 1 elemento de los cuales contiene dígitos (modelo coincide).
   - `mismatch` en cualquier otro caso.

**Tabla de casos de prueba (a documentar en el agent.md):**

| # | titulo_radar | titulo_tienda | Esperado | Razón |
|---|---|---|---|---|
| 1 | `Bosch Serie 4 XL freidora` | `Pañales Dodot Talla 5 Maxi` | mismatch | 0 tokens identidad comunes |
| 2 | `Ninja MAX PRO freidora aire` | `Cafetera Krups Essential` | mismatch | 0 tokens identidad comunes |
| 3 | `Sony WH-1000XM5 auriculares` | `Sony WH-1000XM5 Auriculares Inalámbricos Bluetooth Cancelación Ruido` | match | `sony`, `wh-1000xm5` coinciden |
| 4 | `Xiaomi Robot Vacuum X10+` | `Xiaomi Robot Aspirador X10+ Mopa` | match | `xiaomi`, `x10` coinciden |
| 5 | `Auriculares JBL Tune 510BT` | `JBL Tune 510BT Cascos Bluetooth Plegables` | match | `jbl`, `510bt` coinciden |
| 6 | `iPhone 15 Pro 256GB Titanio Natural` | `Apple iPhone 15 Pro 256 GB Natural` | match | `iphone`, `15`, `pro`, `256` coinciden |
| 7 | `Lego Star Wars Halcón Milenario` | `Lego Marvel Hulkbuster` | mismatch | solo `lego` en común (1 token sin dígito) |

El caso 7 ilustra por qué el umbral es **≥2 tokens** o **≥1 con dígito**: marcas grandes con muchos productos exigen confirmación adicional.

### Cambios concretos por archivo

#### `.claude/agents/offer-enricher.md`

- **Frontmatter:** sin cambios en `tools` (los mismos de Playwright).
- **Sección "Tu rol en el flujo":** añadir que recibe `titulo_radar` y opcionalmente `asin_esperado` (para fast-path cuando R2 esté disponible).
- **Nueva sección entre el Paso 3 (extraer datos) y Paso 4 (calcular descuento): "Paso 3.5 — Validación de coherencia título radar/tienda"**. Describe el algoritmo de dos niveles arriba y enuncia los casos de la tabla.
- **Nueva sección de manejo de errores: "StoreMismatchError"**, paralela a `StoreBlockedError`. Define el mensaje literal que se devuelve al orquestador:
  ```
  ⚠️ StoreMismatchError: la URL [URL] cargó "[titulo_tienda]" pero el chollo decía "[titulo_radar]".

  Tokens identidad radar: {tokens_radar}
  Tokens identidad tienda: {tokens_tienda}
  Intersección significativa: {interseccion}

  Decisión: mismatch. No se ha enriquecido. El orquestador decidirá si saltar, rechazar o forzar.
  ```
- **Regla nueva en "Reglas de comportamiento":** "Antes de devolver la ficha, ejecuta SIEMPRE el Paso 3.5. Si detectas mismatch, no construyas la ficha — devuelve `StoreMismatchError`."
- **Cierre del navegador:** asegurar `browser_close` también en la rama de `StoreMismatchError` (consistente con el manejo actual de `StoreBlockedError`).

#### `.claude/skills/buscar-ofertas/SKILL.md`

- **PASO 5 — Enriquecer candidata validada:** cambiar el contrato de invocación del enricher. Hoy se le pasa solo la `product_url`. Se le añade:
  - `titulo_radar: <titulo de la candidata>` (siempre).
  - `asin_esperado: <ASIN si el radar lo expone limpio en product_url>` (opcional, solo si R2 está disponible aguas arriba).
- **Tras invocar al enricher**, comprobar la respuesta:
  - Si es ficha → continuar como hoy (escribir a inbox).
  - Si es `StoreBlockedError` → seguir el flujo manual ya existente.
  - **Nuevo:** si es `StoreMismatchError` → no escribir a inbox. Pausar al redactor con:
    ```
    ⚠️ Mismatch detectado en {titulo_radar}
        URL pidió: {titulo_radar}
        URL cargó: {titulo_tienda}

    ¿Qué hago?
      S) Saltar - registrar como diagnóstico y continuar (recomendado)
      R) Rechazar - con motivo opcional
      F) Forzar - confío en la URL, enriquecer igualmente
    ```
  - `S` → añade a `SALTADAS` con motivo `store_mismatch` y el detalle de la intersección de tokens.
  - `R` → añade a `RECHAZADAS` con motivo redactado por el operador.
  - `F` → llama de nuevo al enricher con un flag `force_match=true` (o un alias claro). Esta vez el enricher construye la ficha sin ejecutar el Paso 3.5. La inbox lleva `coherencia_titulo: forzada` en el frontmatter.
- **PASO 6 — Cierre de sesión:** el historial recoge cada `store_mismatch` con `titulo_radar`, `titulo_tienda`, `tokens_intersect` y `radar_offer_id`. Esto cierra el bucle con el radar: cada mismatch es un caso a corregir aguas arriba.

#### Frontmatter de las fichas en inbox

Añadir a `PASO 5` los campos:
```yaml
coherencia_titulo: ok | forzada
titulo_radar: "{titulo crudo del radar}"
titulo_tienda: "{titulo extraído de la tienda}"
```

Esto deja constancia en cada draft de la inbox de si el match fue automático o forzado, para que el redactor del proyecto hermano lo tenga visible.

### Tests / verificación

Este repo no tiene suite Python. La verificación se hace con la **tabla de 7 casos** del agent.md más:

1. **Smoke test manual:** ejecutar `/buscar-ofertas` apuntado al catálogo actual del radar (todavía con shortlinks rotados). Esperado: el enricher debe rechazar la mayoría como `StoreMismatchError`. Confirma que la red de seguridad funciona antes de que R2 esté hecho.
2. **Smoke test positivo:** una vez R2 esté en producción, ejecutar de nuevo `/buscar-ofertas`. Esperado: la inmensa mayoría debería pasar el matching y producir fichas en inbox.

## System-Wide Impact

- **Interaction graph:** `buscar-ofertas` (skill) → `offer-enricher` (subagente con Playwright). El cambio toca solo el contrato entre estas dos piezas; `radar-catalog-client`, `aggregator-scraper` y `telegram-scraper` no se ven afectados.
- **Error propagation:** se introduce un nuevo error tipado (`StoreMismatchError`) paralelo a `StoreBlockedError`. La skill captura ambos en el mismo bloque de manejo del Paso 5. La pausa interactiva añadida no interrumpe el flujo del bucle de candidatas — al elegir `S/R/F` se vuelve al loop normal.
- **State lifecycle risks:** ninguno. R4 es lógica pura sobre datos transitorios. No persiste estado nuevo en BD (no hay BD local). El historial y changelog ya recogen rechazos/saltos; solo se añade el motivo `store_mismatch`.
- **API surface parity:** el `aggregator-scraper` y `telegram-scraper` no llaman al enricher hoy (CLAUDE.md lo prohíbe explícitamente — solo el orquestador llama a subagentes). Por tanto el cambio de contrato del enricher solo afecta a la skill.
- **Integration test scenarios:**
  1. Catálogo con shortlinks rotados → todos los enriches devuelven mismatch → no se escribe nada a inbox.
  2. Catálogo limpio post-R2 → matching pasa para >80% de candidatas.
  3. Producto legítimo con título reescrito en Amazon (caso #4 borderline) → matching pasa por coincidencia de modelo.
  4. Producto con marca muy común y título engañoso (caso #7) → matching detecta correctamente como mismatch.
  5. Operador fuerza match con `F` → ficha escrita con `coherencia_titulo: forzada`.

## Acceptance Criteria

### Funcionales

- [ ] El enricher acepta `titulo_radar` como input obligatorio y opcionalmente `asin_esperado`.
- [ ] El enricher ejecuta el Paso 3.5 (matching) en toda invocación y rechaza con `StoreMismatchError` si no hay match.
- [ ] El algoritmo de matching pasa los 7 casos de la tabla del agent.md.
- [ ] La skill `buscar-ofertas` pasa `titulo_radar` al enricher en cada llamada.
- [ ] La skill captura `StoreMismatchError` y ofrece al redactor las opciones `S/R/F` con los detalles del mismatch.
- [ ] La opción `F` (forzar) escribe la ficha en inbox con `coherencia_titulo: forzada`.
- [ ] El historial y el changelog recogen `store_mismatch` como motivo separado, con los tokens involucrados.

### No funcionales

- [ ] El matching es lógica pura, sin I/O adicional. El paso 3.5 no añade más de ~50 ms al tiempo del enricher.
- [ ] Los mensajes de error al redactor están en español con ortografía y acentos correctos.
- [ ] El navegador se cierra con `browser_close` también en la rama de `StoreMismatchError`.

## Success Metrics

- Antes de R2 (con catálogo de shortlinks rotados): R4 detecta y rechaza ≥90% de los mismatches reales. Cero fichas erróneas en inbox.
- Tras R2 (con catálogo limpio): la tasa de `StoreMismatchError` baja por debajo del 5%. Los pocos que queden son diagnóstico válido del radar (rotaciones extremadamente recientes, productos descatalogados).

## Dependencies & Risks

**Dependencias:**
- Independiente de R1/R2/R3. R4 puede implementarse y desplegarse hoy mismo.
- Si R2 se implementa después, el fast-path estructural (Nivel 1) se activa pasando `asin_esperado`. Hasta entonces, el matching opera solo con tokens.

**Riesgos:**
- **Falsos negativos** (productos válidos rechazados): mitigado por la opción `F` (forzar) del operador.
- **Falsos positivos** (mismatches que pasan como match): la tabla de casos cubre el borde (caso #7). Si aparecen patrones nuevos, se añaden a la tabla y se ajusta el umbral.
- **Acentos en títulos:** la normalización NFKD → ASCII evita problemas con `cancelación`/`cancelacion`. Cubierto.

## Implementation Phases

### Fase 1 — Documentación del matcher en `offer-enricher.md`

- Añadir sección "Paso 3.5 — Validación de coherencia título radar/tienda" con el algoritmo de dos niveles.
- Añadir la tabla de 7 casos de prueba con la columna `match | mismatch` esperada.
- Añadir sección "Manejo de errores: StoreMismatchError" con el mensaje literal.
- Actualizar reglas de comportamiento.

### Fase 2 — Actualización del contrato en `SKILL.md`

- En PASO 5, añadir `titulo_radar` (y opcionalmente `asin_esperado`) al payload de invocación al enricher.
- Añadir el manejo de `StoreMismatchError` con las opciones `S/R/F`.
- Añadir los campos `coherencia_titulo`, `titulo_radar` y `titulo_tienda` al frontmatter de inbox.
- En PASO 6, añadir el motivo `store_mismatch` con detalle de tokens al historial y al changelog.

### Fase 3 — Verificación manual

- Ejecutar `/buscar-ofertas` contra el catálogo actual. Confirmar que el enricher detecta los mismatches del UAT y la skill ofrece la pausa interactiva esperada.
- Documentar los resultados como entrada en `historial/2026-05-21-sesion-1.md` (o el siguiente número disponible).

### Fase 4 — Documentación operativa

- Añadir línea en `changelog/changelog-2026-05-21.txt` describiendo el cambio.
- Actualizar `CLAUDE.md` si fuera necesario para reflejar el nuevo error tipado (`StoreMismatchError`).

## Alternativas consideradas

1. **Resolver el shortlink en un paso 4.5 de la skill antes de llamar al enricher** (mejora #A del documento original). Descartada en el brainstorm (ver origin) porque duplicaría trabajo: el enricher ya navega y ya tiene el snapshot. Mejor que el matching viva donde están los datos.
2. **Tests automatizados con pytest contra el matcher**. Descartada porque este repo no tiene runtime Python — son skills/agentes Claude. La tabla de casos en el agent.md cumple la misma función.
3. **Similaridad por Jaccard o coseno TF-IDF**. Descartada por complejidad. Los títulos son cortos (5-15 tokens). El matching por intersección de tokens de identidad es más predecible y debuggable, y los casos del UAT son lo bastante extremos como para no necesitar más fineza.

## Contrato cross-repo (qué necesita exponer `radar_editorial`)

R1/R2/R3 son trabajo del repo hermano `radar_editorial` y requieren su propio `/ce:plan` allí. Este plan documenta el **contrato mínimo** que ese plan debe satisfacer para no romper este repo:

### R1 — TTL 10 días con borrado duro
- La API `/api/editorial/offers/` **nunca** debe servir ofertas con `first_seen_at` anterior a 10 días naturales.
- Si se implementa como borrado físico (`DELETE`), perfecto. Si se implementa como filtro de runtime sin borrar, también es aceptable mientras la API se mantenga limpia.
- Sin retención ni histórico (decisión cerrada en brainstorm).

### R2 — Resolver shortlinks en ingesta
- Cada item devuelto por `/api/editorial/offers/` debe llevar `product_url` apuntando a la URL canónica de la tienda:
  - Amazon: `https://www.amazon.es/dp/{ASIN}` sin parámetros de afiliación.
  - AliExpress: `https://es.aliexpress.com/item/{ID}.html` (o `aliexpress.com/...` como equivalente funcional según CLAUDE.md de este repo).
- Si una oferta entra al radar con un shortlink que no resuelve a uno de esos hosts, **no se publica** en la API.
- **Campo opcional pero deseable:** `asin` (para Amazon) e `item_id` (para AliExpress) expuestos directamente como campos, no solo embebidos en la URL. Esto habilita el fast-path estructural del Nivel 1 del matcher de R4.
- El shortlink original se mantiene internamente como `affiliate_url` y **no se expone** en la API.

### R3 — Búsqueda full-text + filtros estructurados
- `q=` debe tokenizar y construir consulta con operador OR por defecto, ordenando por relevancia (`SearchRank` de Postgres con diccionario español).
- La API debe aceptar adicionalmente: `price_max`, `price_min`, `discount_min`, `store`.
- `sort=score` se mantiene como override del ranking por relevancia.

### Esqueleto sintético para el plan paralelo de `radar_editorial`

Cuando se ejecute `/ce:plan` en el otro repo, parte de esta base:

```
Fase 1 — R2 (resolver shortlinks en ingesta de adapters)
  - apps/ingestion/services/adapters.py: para cada adapter (chollazos, hispachollos, chollometro, michollo),
    seguir el redirect del shortlink con requests.head(..., allow_redirects=True), extraer ASIN/item_id,
    poblar product_url canónica + campo asin/item_id, y guardar el shortlink en affiliate_url.
  - Si el redirect no resuelve a hosts permitidos, no publicar.
  - Backfill: recorrer ofertas pendientes con product_url=null para resolverlas o despublicarlas.

Fase 2 — R1 (TTL 10 días)
  - Filtro en la vista que sirve /api/editorial/offers/ (excluye first_seen_at < NOW - 10 días).
  - Job programado en Railway: DELETE FROM offers WHERE first_seen_at < NOW() - INTERVAL '10 days'.
    Cadencia: diaria.

Fase 3 — R3 (full-text + filtros)
  - SearchVector sobre title + brand con dictionary español.
  - Vista: tokenizar q, construir SearchQuery con operador OR, ordenar por SearchRank.
  - Añadir filtros: price_max, price_min, discount_min, store.
  - Mantener sort=score como override.

Fase 4 — Verificación end-to-end con el localizador
  - Ejecutar /buscar-ofertas desde claude-code-localizador-ofertas contra el catálogo limpio.
  - Confirmar tasa de StoreMismatchError <5%.
```

## Outstanding Questions

### Resolve before implementation

_(ninguna)_

### Deferred during execution

- **[Afecta R4][Operativa]** La opción `F` (forzar) escribe a inbox con `coherencia_titulo: forzada`. ¿Conviene además registrar el forzado en un log separado para auditarlo? Decisión menor; se puede dejar para iteración 2 si en uso real aparece la necesidad.
- **[Afecta R4][Investigación]** Detectar si AliExpress devuelve títulos con tokens muy variables entre el chollo original y el listing actual (re-titulación frecuente por SEO). Si la tasa de falsos negativos en AliExpress es alta, podría hacer falta umbral distinto por tienda.
- **[Cross-repo][Operativa]** La nota operativa del doc original sobre versionado de contratos entre los tres repos sigue pendiente. Candidato a un README compartido o un canal fijado. No bloquea esta implementación.

## Sources & References

### Origin
- **Origin document:** [docs/brainstorms/2026-05-21-simplificacion-radar-localizador-requirements.md](../brainstorms/2026-05-21-simplificacion-radar-localizador-requirements.md). Decisiones clave carried forward:
  - TTL 10 días con borrado duro (sin histórico).
  - Resolución de ASIN en radar (no en localizador).
  - Full-text Postgres en lugar de búsqueda semántica.
  - R4 como red de seguridad en el enricher local.

### Internal references
- [.claude/agents/offer-enricher.md](../../.claude/agents/offer-enricher.md) — agente que se modifica.
- [.claude/skills/buscar-ofertas/SKILL.md](../../.claude/skills/buscar-ofertas/SKILL.md) — orquestador que se modifica.
- [.claude/agents/radar-catalog-client.md](../../.claude/agents/radar-catalog-client.md) — cliente del radar, sin cambios pero contexto del contrato.
- [fuentes.md](../../fuentes.md) — tabla maestra de fuentes activas.
- [CLAUDE.md](../../CLAUDE.md) — regla "los subagentes no se llaman entre sí, solo el orquestador los invoca".

### Documento de partida
- [docs/2026-05-20-mejoras-radar-y-localizador.md](../2026-05-20-mejoras-radar-y-localizador.md) — UAT y propuesta de las 7 mejoras originales.
