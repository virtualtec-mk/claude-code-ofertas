---
name: buscar-ofertas
description: Orquesta el flujo completo de descubrimiento, filtrado editorial y enriquecimiento de ofertas para un medio español. Coordina aggregator-scraper (Chollometro) y offer-enricher (Amazon/AliExpress España), aplica el guideline del medio destino para filtrar editorialmente, deja que el redactor valide candidata a candidata, y escribe las validadas en la inbox de claude-code-text-agents lista para que /crear-articulo las consuma sin re-scrapear.
argument-hint: [medio] [anunciante] [watchlist-slug]
disable-model-invocation: true
---

# Skill: buscar-ofertas

Eres el orquestador único de este proyecto. Tu trabajo es coordinar dos subagentes (`aggregator-scraper` y `offer-enricher`), aplicar el filtrado editorial inline (eres tú quien lee guidelines), mantener al redactor informado y pausar candidata a candidata para que decida.

**Mantén el estado** durante toda la sesión: `MEDIO`, `ANUNCIANTE`, `WATCHLIST`, `AFINADO`, `FUENTES`, `CANDIDATAS`, `VALIDADAS`, `RECHAZADAS`, `SALTADAS`, `RUTA_HERMANO`, `RUTA_HISTORIAL`.

## Parámetros de entrada

`$ARGUMENTS` admite hasta tres tokens separados por espacio, todos opcionales:

- `MEDIO`: slug del medio (ej. `mundodeportivo`).
- `ANUNCIANTE`: `amazon` o `aliexpress`.
- `WATCHLIST_SLUG`: nombre de un archivo en `watchlists/` sin el prefijo `WATCHLIST-` y sin `.md` (ej. `auriculares-anc-md`).

Cualquier token que falte se pregunta interactivamente en el Paso 1.

## Constantes

- `RUTA_HERMANO = "../claude-code-text-agents"`
- `RUTA_INBOX = "../claude-code-text-agents/inbox"`
- `RUTA_GUIDELINES = "../claude-code-text-agents/guidelines"`
- `LIMITE_CANDIDATAS_SCRAPING = 25`
- `LIMITE_CANDIDATAS_TRAS_FILTRO = 12` (presenta como mucho 12 al redactor; si tras filtrar quedan más, ordena por mejor encaje editorial y trunca)

---

## PASO 0 — Verificar hermano

Antes de nada, comprueba que existe `../claude-code-text-agents/` y que contiene `guidelines/` con al menos un `GUIDELINE-*.md`.

Si no existe la carpeta hermana:

```
⚠️ No encuentro el proyecto hermano en ../claude-code-text-agents/.

Este proyecto necesita claude-code-text-agents clonado al lado para leer
guidelines y escribir la inbox. Revisa la ubicación y vuelve a lanzar.

Si tu hermano vive en otra ruta, edita CLAUDE.md y .claude/settings.json.
```

Para el flujo. **No continúes.**

Si la carpeta `../claude-code-text-agents/inbox/` no existe todavía, crea el archivo `../claude-code-text-agents/inbox/.gitkeep` para inicializarla.

---

## PASO 1 — Resolver MEDIO, ANUNCIANTE y WATCHLIST (interactivo)

### 1.a — MEDIO

Si `MEDIO` no se proporcionó como argumento:

1. Lista los archivos `GUIDELINE-*.md` en `RUTA_GUIDELINES`.
2. Extrae el slug de cada uno (parte entre `GUIDELINE-` y `.md`).
3. Muestra:

```
Medios disponibles:
  1. {slug-1}
  2. {slug-2}
  ...

¿Para qué medio buscamos hoy? (número o nombre)
```

4. Espera respuesta y asigna `MEDIO`.

Tras tener `MEDIO`, verifica que existe `../claude-code-text-agents/guidelines/GUIDELINE-{MEDIO}.md`. Si no existe:

```
⚠️ GuidelineMissingError: El medio '{MEDIO}' no tiene guideline en text-agents. Crea primero la guideline allí con `/crear-guideline` y vuelve a lanzar.
```

**DETENER el flujo.** No continuar.

### 1.b — ANUNCIANTE

Si `ANUNCIANTE` no se proporcionó:

```
¿Qué anunciante?
  1. amazon       (Amazon España)
  2. aliexpress   (AliExpress España)
```

Espera respuesta. Solo se aceptan esos dos valores en MVP.

### 1.c — WATCHLIST y afinado

Lista los archivos en `watchlists/` con patrón `WATCHLIST-*.md`. Por cada uno, lee el frontmatter y muestra `name` + `medio_sugerido` + `anunciante`.

```
Watchlists disponibles:
  1. auriculares-anc-md       (mundodeportivo / amazon)
  2. zapatillas-running-larazon  (larazon / amazon)
  ...
  0. ninguna / describir libre

¿Qué watchlist uso? (número, 0 para ninguna, o el slug directo)
```

- Si elige una, lee su contenido completo y guárdalo como `WATCHLIST_DATA`.
- Si elige `0`, pide: *"Describe brevemente qué tipo de oferta buscas (categorías, marcas, rangos de precio):"*. Guarda la respuesta como `WATCHLIST_DATA` (texto libre).

Luego, en cualquiera de los dos casos, ofrece afinado conversacional:

```
¿Quieres afinar la búsqueda para esta sesión? (ej. "hoy solo Sony y Bose", "máx 80€", "nada de productos blancos"). Enter para omitir.
```

Guarda la respuesta como `AFINADO` (puede ser vacío). **No modifica el archivo de watchlist**, solo afecta a esta sesión.

### 1.d — FUENTES

Lee `fuentes.md` y extrae los slugs de las fuentes con `inactiva: false`. En MVP son tres: `chollometro`, `telegram-hispachollos`, `telegram-chollazos`.

Pregunta:

```
¿De qué fuentes tiro hoy?
  1. Todas (recomendado)
  2. Solo Chollometro
  3. Solo Telegram (hispachollos + chollazos)
  4. Elegir a mano
```

- Opción 1 (default si Enter): `FUENTES = [chollometro, telegram-hispachollos, telegram-chollazos]`.
- Opción 2: `FUENTES = [chollometro]`.
- Opción 3: `FUENTES = [telegram-hispachollos, telegram-chollazos]`.
- Opción 4: muestra la lista numerada y permite seleccionar varias separadas por coma (ej. `1,3`).

---

## PASO 2 — Invocar scrapers y unificar candidatas

### 2.a — Lanzar scrapers en paralelo

Por cada fuente en `FUENTES`, invoca el subagente correspondiente. Lánzalos **en paralelo** (un solo mensaje con varias invocaciones de Agent) — son independientes.

Mapeo fuente → subagente:

- `chollometro` → `aggregator-scraper` con `ANUNCIANTE` y `LIMITE = LIMITE_CANDIDATAS_SCRAPING`.
- `telegram-hispachollos` → `telegram-scraper` con `CANAL = hispachollos`, `ANUNCIANTE` y `LIMITE = 15`.
- `telegram-chollazos` → `telegram-scraper` con `CANAL = chollazos`, `ANUNCIANTE` y `LIMITE = 15`.

Instrucción genérica a cada subagente (adapta al schema de cada uno; ambos comparten formato de salida):

```
Scrapea {fuente} filtrado por el anunciante: {ANUNCIANTE}.
Límite: {N} candidatas.
Devuelve YAML estructurado según tu schema, con la URL canónica de la
tienda final ya resuelta. Solo dominios amazon.es o es.aliexpress.com.
Si bloqueo/timeout, devuelve parcial con degraded: true y motivo_degradacion.
No reintentes.
```

Guarda los outputs como `RESULTADOS_POR_FUENTE` (mapa fuente → output del scraper).

### 2.b — Manejo de degradación parcial

Por cada fuente cuyo output venga con `degraded: true`, NO bloquees al resto. Acumula los avisos.

Al terminar las invocaciones, si hay alguna fuente degradada:

```
⚠️ AggregatorBlockedError parcial:
  - {fuente_1}: {N1} candidatas antes del bloqueo ({motivo_1})
  - {fuente_2}: ok ({N2} candidatas)
  ...

¿Continúo con todo lo recogido o aborto?
  C) Continúo con las {N_total} candidatas combinadas
  A) Aborto la sesión
```

Si TODAS las fuentes están degradadas y la suma de candidatas es 0 → aborta automáticamente con mensaje claro, no preguntes.

### 2.c — Unificar y deduplicar

Une todas las listas en `CANDIDATAS_BRUTAS`. Aplica dedupe por `url_canonica`:

1. Normaliza la `url_canonica` antes de comparar: minúsculas, sin trailing slash, sin query string excepto para AliExpress (donde el ID está en el path).
2. Si dos o más candidatas comparten `url_canonica` normalizada, fusiónalas en una única:
   - **Prevalece** la candidata con `precio_anterior` no nulo. Si empatan, prevalece la de Chollometro (tiene % descuento más fiable).
   - El campo `fuentes_origen` de la candidata fusionada es la lista de todas las fuentes donde apareció (ej. `[chollometro, telegram-hispachollos]`).
3. Las candidatas únicas conservan su `fuentes_origen` como lista de un elemento.

Resultado: `CANDIDATAS_BRUTAS` es una lista limpia con un item por producto, anotando en `fuentes_origen` dónde apareció.

### 2.d — Lista vacía tras unificar

Si tras dedupe `CANDIDATAS_BRUTAS` está vacía (no degradado pero 0 items útiles), avisa al redactor y pregunta si cambia de anunciante/fuentes o aborta. No sigas sin candidatas.

---

## PASO 3 — Filtrado editorial inline

**Lo hace el orquestador, no un subagente.** Es razonamiento puro sobre archivos ya cargados.

1. Lee `../claude-code-text-agents/guidelines/GUIDELINE-{MEDIO}.md` completo.
2. Ten también presente `WATCHLIST_DATA` y `AFINADO`.
3. Para cada candidata en `CANDIDATAS_BRUTAS`, evalúa:
   - ¿Encaja con el tono y la temática del medio según la guideline?
   - ¿Cumple los criterios de la watchlist (keywords, marcas, precio_min/max si aplican)?
   - ¿Respeta el afinado de la sesión?
   - ¿El descuento aparente justifica un artículo (no es un precio normal disfrazado)?
4. Asigna a cada candidata una de estas etiquetas:
   - `encaja` — entra al filtro final.
   - `dudosa` — encaje débil pero defendible.
   - `fuera` — no encaja con el medio o la watchlist.
5. Ordena: primero `encaja` (por relevancia editorial subjetiva), luego `dudosa`. Las `fuera` se descartan **salvo** que el conjunto `encaja + dudosa` esté vacío (ver fallback abajo).
6. Trunca a `LIMITE_CANDIDATAS_TRAS_FILTRO`.

Guarda como `CANDIDATAS_FILTRADAS`, donde cada item lleva todos los campos del scraper + un campo `justificacion` (1 línea explicando por qué entra).

### Fallback: 0 candidatas tras filtro

Si `CANDIDATAS_FILTRADAS` queda vacía, presenta las primeras 5 de `CANDIDATAS_BRUTAS` marcadas explícitamente como "fuera del foco editorial" y avisa al redactor:

```
ℹ️ Ninguna de las {N} candidatas brutas encaja con el foco editorial de {MEDIO} ni con tu watchlist/afinado. Te muestro las 5 primeras igualmente por si quieres revisarlas. Trátalas como fuera de foco.
```

Luego sigue al Paso 4 con esas 5.

---

## PASO 4 — Validación interactiva candidata a candidata

**Pausa obligatoria por candidata.** No proceses la siguiente sin respuesta del redactor.

Para cada candidata en `CANDIDATAS_FILTRADAS`:

Muestra:

```
[{i}/{total}] {titulo}
  Precio: {precio_actual}   (antes {precio_anterior} · -{descuento_pct}%)
  Tienda: {tienda}
  URL:    {url_canonica}
  Fuentes: {fuentes_origen ej. "chollometro + telegram-hispachollos"}
  Encaje editorial: {justificacion}

¿Qué hago?
  V) Validar — enriquecer y mandar a la inbox
  R) Rechazar — opcionalmente dime el motivo
  S) Saltar (no la valido pero no la marco como rechazada)
  Q) Cerrar la sesión aquí
```

Espera respuesta. Acciones:

- **V**: salta al Paso 5 para esta candidata. Cuando termine, vuelve aquí con la siguiente.
- **R**: pide `"¿Motivo? (Enter para omitir)"`. Añade a `RECHAZADAS` con `{url, titulo, motivo}` y pasa a la siguiente.
- **S**: añade a `SALTADAS` con `{url, titulo}` y pasa a la siguiente.
- **Q**: deja de presentar candidatas. Las pendientes no se añaden a nada. Salta al Paso 6.

Cuando se agoten las candidatas, ofrece guardar la búsqueda afinada como watchlist:

```
¿Guardo "{descripcion-afinado}" como nueva watchlist en watchlists/? (s/n)
```

Si sí, propon un slug en kebab-case (máx 60 chars), pide confirmación o renombrado, y escribe `watchlists/WATCHLIST-{slug}.md` con el frontmatter mínimo (`name`, `medio_sugerido`, `anunciante`, y un cuerpo con el `AFINADO` literal en una sección "Notas").

---

## PASO 5 — Enriquecer una candidata validada

Invoca `offer-enricher` con:

```
Enriquece esta URL: {url_canonica}

Devuelve la ficha con el schema espejado de product-researcher: frontmatter
YAML con nombre, marca, modelo, asin, ean, url_origen, tienda, fuente,
fecha_extraccion; y secciones Precio, Descripción corta, Especificaciones
clave, Reseñas.

Si la tienda bloquea, lanza StoreBlockedError exactamente como
especifica tu prompt y espera a que el redactor pegue los datos a mano
(marcando fuente: manual).
```

Guarda como `FICHA_ENRIQUECIDA`.

### Si llega `StoreBlockedError`

Reproduce el mensaje del subagente al redactor tal cual y espera datos manuales. Una vez recibidos, el subagente debe haberlos estructurado y devuelto la ficha con `fuente: manual`.

### Escribir a la inbox

1. Calcula `SLUG_PRODUCTO`: del título, en kebab-case, sin acentos, máximo 60 caracteres.
2. Calcula `FECHA_HOY` en formato `DD-MM-YYYY`.
3. Calcula `FECHA_HUMANA` en formato `DD/MM/YYYY` para frontmatter visible.
4. Ruta: `../claude-code-text-agents/inbox/{FECHA_HOY}-{SLUG_PRODUCTO}.md`.
5. Si esa ruta ya existe, añade sufijo `-2`, `-3`... hasta encontrar una libre (sin lógica de dedupe real en MVP, solo evitar sobrescribir).

Construye el contenido **fusionando** la ficha del enricher con metadatos del flujo:

```markdown
---
medio: {MEDIO}
anunciante: {ANUNCIANTE}
url_producto: {url_canonica}
titulo: "{titulo}"
precio_actual: {precio_actual_normalizado}
descuento_pct: {descuento_pct}
vendedor: "{marca_o_amazon}"
fecha_validacion: {FECHA_HUMANA}
nota_redactor: "{nota_si_la_dejó, vacío si no}"
fuente_enriquecimiento: {automatica-playwright | manual}
---

# Ficha enriquecida

{contenido completo de FICHA_ENRIQUECIDA — el bloque interno con su
propio frontmatter y las secciones Precio, Descripción corta,
Especificaciones clave, Reseñas, tal como lo devolvió offer-enricher}
```

Escribe el archivo. Añade a `VALIDADAS` con `{url, titulo, ruta_inbox}`.

Antes de pasar a la siguiente candidata del Paso 4, confirma brevemente al redactor:

```
✅ Ficha guardada en {ruta_inbox}
```

---

## PASO 6 — Cierre de sesión

Cuando se agoten las candidatas o el redactor cierre con `Q`:

### 6.a — Escribir historial

Calcula `RUTA_HISTORIAL`:

1. Hoy en `YYYY-MM-DD`.
2. Numera la sesión: si ya existen `historial/{HOY}-sesion-1.md`, `...-sesion-2.md`, etc., usa el siguiente N.
3. Ruta final: `historial/{HOY}-sesion-{N}.md`.

Contenido:

```markdown
---
fecha: {FECHA_HUMANA}
medio: {MEDIO}
anunciante: {ANUNCIANTE}
fuentes: [{FUENTES separadas por coma}]
watchlist: {WATCHLIST_SLUG_o_"ninguna"}
afinado: "{AFINADO}"
total_brutas: {N}
total_filtradas: {M}
total_validadas: {len(VALIDADAS)}
total_rechazadas: {len(RECHAZADAS)}
total_saltadas: {len(SALTADAS)}
---

## Validadas
{por cada item: - {url_canonica} — {titulo} — {precio_actual}}
{si vacío: "(ninguna)"}

## Rechazadas
{por cada item: - {url_canonica} — {motivo si lo dejó}}
{si vacío: "(ninguna)"}

## Saltadas
{por cada item: - {url_canonica}}
{si vacío: "(ninguna)"}
```

### 6.b — Línea en changelog

Calcula `changelog/changelog-{YYYY-MM-DD}.txt`. Si no existe el archivo del día, créalo con cabecera:

```
====================================================
CHANGELOG — DD/MM/YYYY
====================================================
```

Añade una línea (append):

```
[HH:MM] /buscar-ofertas {MEDIO} {ANUNCIANTE} [fuentes: {FUENTES}] → {V} validadas, {R} rechazadas, {S} saltadas. Historial: {RUTA_HISTORIAL}
```

### 6.c — Resumen al redactor

```
## Sesión cerrada

Medio:        {MEDIO}
Anunciante:   {ANUNCIANTE}
Fuentes:      {FUENTES separadas por coma}
Watchlist:    {WATCHLIST_SLUG_o_"ninguna"}
Afinado:      "{AFINADO}"

Validadas:    {len(VALIDADAS)}
Rechazadas:   {len(RECHAZADAS)}
Saltadas:     {len(SALTADAS)}

Historial:    {RUTA_HISTORIAL}
Inbox del hermano: ../claude-code-text-agents/inbox/

Las fichas validadas están listas para que /crear-articulo las consuma en
claude-code-text-agents sin re-scrapear.
```

---

## Reglas de comportamiento general

- **Eres el único que lee guidelines y watchlists.** Los subagentes no las tocan.
- **Eres el único que escribe a la inbox.** El enricher devuelve la ficha; tú la fusionas con metadatos y la guardas.
- **No saltes la pausa interactiva del Paso 4.** Cada candidata exige una respuesta del redactor.
- **No reintentes** los subagentes cuando devuelven error. Aplica el manejo de error definido y deja decidir al redactor.
- **Mantén el estado** entre pasos.
- **Si Playwright MCP no está disponible**, el `aggregator-scraper` te lo dirá en el output. Comunícalo al redactor sin traceback y para limpio.
- **Texto al redactor siempre en español**, ortografía correcta, fechas `DD/MM/YYYY` en lo visible, `YYYY-MM-DD` solo en nombres de archivo.
- **Números** en formato español: `1.299,00 €`.
- **Convención de slugs**: kebab-case, sin acentos, sin caracteres especiales, máx 60 chars.
