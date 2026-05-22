---
name: buscar-ofertas
description: Orquesta el flujo de ofertas usando radar_editorial como fuente principal, filtra editorialmente con guidelines/watchlists, valida candidata a candidata y envia las fichas enriquecidas a la inbox de claude-code-text-agents.
argument-hint: [medio] [anunciante] [watchlist-slug]
disable-model-invocation: true
---

# Skill: buscar-ofertas

Eres el orquestador unico de este proyecto. Tu fuente principal de descubrimiento es `radar_editorial`, consumido mediante el subagente `radar-catalog-client`. Los scrapers directos (`aggregator-scraper` y `telegram-scraper`) quedan como herramientas manuales/diagnosticas y no se invocan automaticamente.

Mantén el estado durante toda la sesion: `MEDIO`, `ANUNCIANTE`, `WATCHLIST`, `AFINADO`, `CANDIDATAS_BRUTAS`, `CANDIDATAS_FILTRADAS`, `VALIDADAS`, `RECHAZADAS`, `SALTADAS`, `DIAGNOSTICOS_RADAR`, `RUTA_HERMANO`, `RUTA_HISTORIAL`.

## Parametros de entrada

`$ARGUMENTS` admite hasta tres tokens separados por espacio:

- `MEDIO`: slug del medio.
- `ANUNCIANTE`: `amazon` o `aliexpress`.
- `WATCHLIST_SLUG`: archivo en `watchlists/` sin `WATCHLIST-` ni `.md`.

Pregunta interactivamente cualquier valor que falte.

## Constantes

- `RUTA_HERMANO = "../claude-code-text-agents"`
- `RUTA_INBOX = "../claude-code-text-agents/inbox"`
- `RUTA_GUIDELINES = "../claude-code-text-agents/guidelines"`
- `LIMITE_CANDIDATAS_RADAR = 25`
- `LIMITE_CANDIDATAS_TRAS_FILTRO = 12`
- `FUENTE_DESCUBRIMIENTO = "radar_editorial"`

## PASO 0 - Verificar hermano y configuracion

Comprueba que existe `../claude-code-text-agents/` y que contiene `guidelines/GUIDELINE-*.md`. Si falta, muestra `GuidelineMissingError` o error de ruta claro y detén el flujo.

Si `../claude-code-text-agents/inbox/` no existe, crea `../claude-code-text-agents/inbox/.gitkeep`.

Verifica que el operador tiene configurados los datos del radar que usara `radar-catalog-client`:

- `RADAR_BASE_URL`
- `RADAR_AGENT_API_TOKEN`

Si faltan, detén el flujo con `RadarConfigError`. No lo confundas con falta de ofertas.

## PASO 1 - Resolver MEDIO, ANUNCIANTE y WATCHLIST

Resuelve `MEDIO` listando `GUIDELINE-*.md` si no se proporciono. Verifica que existe `GUIDELINE-{MEDIO}.md`.

Resuelve `ANUNCIANTE`; solo se aceptan `amazon` y `aliexpress`.

Lista `watchlists/WATCHLIST-*.md`. Si el redactor elige una, lee su contenido completo como `WATCHLIST_DATA`. Si elige ninguna, pide una descripcion libre de busqueda y guardala como `WATCHLIST_DATA`.

Pide afinado opcional para esta sesion y guardalo como `AFINADO` sin modificar la watchlist.

## PASO 2 - Consultar radar_editorial

Invoca `radar-catalog-client` con:

```text
Consulta radar_editorial para:
- ANUNCIANTE: {ANUNCIANTE}
- QUERY: resumen de WATCHLIST_DATA + AFINADO
- LIMITE: LIMITE_CANDIDATAS_RADAR

Devuelve candidatas normalizadas y conserva diagnostics/meta del radar.
```

Guarda la salida como `RESULTADO_RADAR`.

Si llega `RadarConfigError` o `RadarUnavailableError`, informa al redactor y detén el flujo. No invoques scrapers locales.

Si `RESULTADO_RADAR.total == 0`, genera diagnostico accionable:

- Resume `diagnostics` y `meta.quality` del radar.
- Explica que la mejora debe hacerse en `radar_editorial` o sus fuentes semilla.
- Escribe un archivo `historial/YYYY-MM-DD-diagnostico-radar-{n}.md` con `medio`, `anunciante`, `watchlist`, `afinado`, filtros y diagnostics.
- Añade linea en `changelog/changelog-YYYY-MM-DD.txt`.
- Detén el flujo sin llamar a `aggregator-scraper` ni `telegram-scraper`.

Si hay items, normalizalos como `CANDIDATAS_BRUTAS`. Cada candidata conserva:

- `fuente: radar_editorial`
- `radar_offer_id`
- `url_origen`
- `product_url`
- `campos_incompletos`
- `fuente_original`

## PASO 3 - Filtrado editorial inline

Lee completo `../claude-code-text-agents/guidelines/GUIDELINE-{MEDIO}.md`. Ten presentes `WATCHLIST_DATA` y `AFINADO`.

Para cada candidata del radar evalua:

- Encaje con tono y tematica del medio.
- Encaje con watchlist/afinado.
- Descuento aparente y calidad de datos.
- Si `product_url` falta, marcala como incompleta y no la presentes como validacion directa salvo que no haya opciones completas.

Etiqueta cada candidata:

- `encaja`
- `dudosa`
- `fuera`

Ordena primero `encaja`, luego `dudosa`, priorizando datos completos y mejor score. Trunca a `LIMITE_CANDIDATAS_TRAS_FILTRO`.

Si no queda ninguna, muestra hasta 5 candidatas brutas como "fuera del foco editorial" y registra el motivo en historial al cerrar.

## PASO 4 - Validacion interactiva candidata a candidata

Pausa por cada candidata. Muestra:

```text
[{i}/{total}] {titulo}
  Precio: {precio_actual} (antes {precio_anterior} - {descuento_pct}%)
  Tienda: {tienda}
  Fuente: radar_editorial / {fuente_original}
  Radar ID: {radar_offer_id}
  URL origen: {url_origen}
  Producto: {product_url o "incompleta"}
  Calidad: {campos_incompletos}
  Encaje editorial: {justificacion}

¿Que hago?
  V) Validar - enriquecer y mandar a la inbox
  R) Rechazar - opcionalmente dime el motivo
  S) Saltar
  Q) Cerrar la sesion aqui
```

Si falta `product_url`, no llames a `offer-enricher`; ofrece rechazar, saltar o cerrar y registra `product_url_missing` como diagnostico.

## PASO 5 - Enriquecer candidata validada

Solo tras `V` y con `product_url` presente, invoca `offer-enricher` con este payload:

```text
product_url: {product_url}
titulo_radar: {titulo}                   # SIEMPRE - el titulo crudo del radar
asin_esperado: {asin si el radar lo expone limpio, sino omitir}
```

`asin_esperado` solo se incluye cuando el radar lo expone como campo independiente o la `product_url` ya es la URL canonica con `/dp/{ASIN}` o `item/{ID}.html`. Si no, se omite y el enricher cae al matching por tokens.

Examina la respuesta del enricher:

### 5.a - Ficha completa devuelta

Continua como hasta hoy: fusiona la ficha con metadatos del radar y escribe `../claude-code-text-agents/inbox/{DD-MM-YYYY}-{slug-producto}.md`.

El frontmatter visible debe incluir:

```yaml
medio: {MEDIO}
anunciante: {ANUNCIANTE}
fuente_descubrimiento: radar_editorial
radar_offer_id: {radar_offer_id}
url_origen: {url_origen}
url_producto: {product_url}
titulo: "{titulo}"
titulo_radar: "{titulo_radar}"
titulo_tienda: "{titulo_tienda devuelto por el enricher}"
coherencia_titulo: ok           # ok cuando el matching paso; forzada cuando el operador eligio F
precio_actual: {precio_actual}
descuento_pct: {descuento_pct}
fecha_validacion: {DD/MM/YYYY}
fuente_enriquecimiento: {automatica-playwright | manual}
```

Anade a `VALIDADAS` la ruta de inbox.

### 5.b - StoreBlockedError

Sigue el flujo manual ya existente (el redactor pega los datos, ficha con `fuente_enriquecimiento: manual`). `coherencia_titulo: ok` por defecto (no se ha podido verificar; queda registrado como manual).

### 5.c - StoreMismatchError (nuevo)

No escribas a inbox. Pausa al redactor mostrando exactamente:

```text
⚠️ Mismatch detectado en {titulo_radar}
    URL pidio: {titulo_radar}
    URL cargo: {titulo_tienda}
    Tokens identidad radar: {tokens_radar}
    Tokens identidad tienda: {tokens_tienda}
    Interseccion significativa: {interseccion}

¿Que hago?
  S) Saltar - registrar como diagnostico y continuar (recomendado)
  R) Rechazar - con motivo opcional
  F) Forzar - confio en la URL, enriquecer igualmente
```

- **`S`** -> anade a `SALTADAS` con `motivo: store_mismatch` y guarda `titulo_radar`, `titulo_tienda`, `tokens_intersect` y `radar_offer_id` como diagnostico. Continua con la siguiente candidata.
- **`R`** -> anade a `RECHAZADAS` con motivo redactado por el operador (puede ser vacio). Misma carga diagnostica que `S`.
- **`F`** -> vuelve a invocar `offer-enricher` con el mismo payload mas `force_match: true`. El enricher omite el Paso 3.5 y construye la ficha. Escribe a inbox como en 5.a pero con `coherencia_titulo: forzada` en el frontmatter. Anade a `VALIDADAS`.

En los tres casos, anade el caso a `DIAGNOSTICOS_RADAR` con tipo `store_mismatch` para arrastrarlo al historial y al changelog (PASO 6).

## PASO 6 - Cierre de sesion

Escribe `historial/{YYYY-MM-DD}-sesion-{n}.md` con:

- `fuente_descubrimiento: radar_editorial`
- `diagnosticos_radar` (incluye los `store_mismatch` con `titulo_radar`, `titulo_tienda`, `tokens_intersect` y `radar_offer_id`)
- candidatas validadas, rechazadas y saltadas; para cada `SALTADAS`/`RECHAZADAS` por `store_mismatch` anade el motivo y los tokens
- candidatas validadas con `coherencia_titulo: forzada` se anotan aparte para auditoria
- `radar_offer_id`, `url_origen`, `product_url` y campos incompletos cuando existan

Añade linea en `changelog/changelog-YYYY-MM-DD.txt` con conteos y ruta de historial. Si hubo `store_mismatch`, indica el conteo (`mismatches=N`) y cuantos se forzaron (`forzados=M`) como senal para mejorar la ingesta del radar.

Pregunta si se guarda el afinado como nueva watchlist solo cuando haya habido una sesion con candidatas.

## Reglas generales

- No hay fallback automatico a scrapers locales.
- El orquestador es el unico que lee guidelines y watchlists.
- El orquestador es el unico que escribe a la inbox.
- Cada candidata exige pausa interactiva.
- Texto al redactor siempre en espanol, con fechas visibles `DD/MM/YYYY`.
- Numeros en formato espanol.
- Si el radar no cubre una intencion, el resultado correcto es diagnostico persistido para mejorar `radar_editorial`.
