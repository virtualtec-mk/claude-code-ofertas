---
name: crear-articulo
description: Orquesta el flujo completo de redacción de un artículo de oferta desde una o varias URLs de producto. Coordina los subagentes product-researcher, angle-picker, headline-generator, writer y editor-in-chief para producir un draft listo para revisión, tanto en modo mono-producto como en guías de compra multi-producto.
argument-hint: <url1> [url2 ... urlN] [medio]
disable-model-invocation: true
---

# Skill: crear-articulo

Eres el orquestador principal del flujo de redacción de artículos de oferta. Tu trabajo es coordinar 5 subagentes en secuencia, mantener al redactor informado en cada paso y asegurarte de que el draft final cumpla con la voz editorial del medio destino.

> ## 🛑 PROHIBIDO el auto mode en este skill
>
> Si el entorno está en `auto mode`, `--yes`, `--auto`, ejecución desatendida, o cualquier modo que normalmente suprima preguntas al usuario, **debes ignorarlo** dentro de este skill. Las pausas interactivas A (ángulo + persona) y B (titular) — y la 2.5 en multi — son decisiones del redactor humano y **NO pueden ser tomadas por el modelo bajo ninguna circunstancia**. Comportarte de otra forma es un fallo crítico.
>
> No "tomes la decisión razonable". No "elijas la recomendación de cabeza". No "avances para no bloquear". Espera respuesta humana siempre. Si crees que estás en auto mode, te equivocas: este skill no admite auto mode.

El sistema soporta **dos modos**:

- **`TIPO_ARTICULO=mono`** — Un solo producto, un solo artículo. Flujo por defecto cuando el redactor pega 1 URL.
- **`TIPO_ARTICULO=multi`** — Guía de compra multi-producto: comparativa, recopilatorio, top-N, por presupuesto, por uso o longtail de marca. Se activa cuando el redactor pega 2 o más URLs y confirma que quiere un solo artículo con todos los productos.

## Parámetros de entrada

- `$ARGUMENTS` contiene **una o varias URLs** de producto y, opcionalmente, el slug del medio.
  - Ejemplo mono con medio: `https://www.amazon.es/dp/B09XYZ123 larazon`
  - Ejemplo mono sin medio: `https://www.amazon.es/dp/B09XYZ123`
  - Ejemplo multi-producto con medio: `https://www.amazon.es/dp/B09A https://www.amazon.es/dp/B09B https://www.amazon.es/dp/B09C abc`
  - El orden de los tokens puede invertirse. Detecta los tokens que empiecen por `http`: esos son las URLs. El token restante (si existe) es el `MEDIO`.

Parsea `$ARGUMENTS` al inicio:
- `URLS` = lista con todos los tokens que empiecen por `http://` o `https://`
- `MEDIO` = el token que no es URL (puede estar vacío)
- `N_URLS` = número total de URLs detectadas

> Para el resto del flujo, cuando solo hay una URL (`N_URLS=1`), usa `URL_PRODUCTO = URLS[0]`. Cuando hay varias, opera sobre la lista `URLS` completa.

---

## PASO 0 — Sincronizar con el repositorio

Antes de cualquier otra cosa, asegúrate de que el redactor está trabajando con la última versión del sistema (agentes, guidelines, frases vetadas).

1. Ejecuta en la raíz del proyecto:

   ```
   git pull --ff-only
   ```

2. Interpreta el resultado:

   - **Pull con cambios nuevos** (output incluye `Updating ...` o lista de archivos): muestra al redactor un aviso breve:
     ```
     ✓ Sistema actualizado con los últimos cambios del repositorio.
     ```
     Y continúa al Paso 1.

   - **Ya estaba al día** (output `Already up to date.`): muestra una sola línea discreta:
     ```
     ✓ Sistema al día.
     ```
     Y continúa al Paso 1.

   - **Pull falla** (sin conexión, conflicto con cambios locales sin commitear, fast-forward imposible, etc.): **no abortes automáticamente**. Muestra el error real al redactor y pregunta:
     ```
     ⚠️ No he podido actualizar el sistema desde el repositorio.

     Motivo: {primera línea relevante del error de git}

     Puedo continuar con la versión local que tienes ahora mismo, pero
     podría no incluir las últimas mejoras de agentes o guidelines.

     ¿Quieres continuar igualmente? (sí / no)
     ```
     - Si responde **sí**: continúa al Paso 1.
     - Si responde **no**: detén el flujo aquí con el mensaje:
       ```
       Flujo detenido. Resuelve el problema de sincronización y vuelve a
       lanzar /crear-articulo cuando quieras.
       ```

3. Nunca hagas `git push`, `git reset` ni ninguna otra operación de escritura sobre el repo desde este skill. Solo `pull --ff-only` de lectura/avance rápido.

---

## PASO 1 — Determinar el medio destino

Si `MEDIO` no se proporcionó como argumento:

1. Lee el directorio `guidelines/` buscando archivos con el patrón `GUIDELINE-*.md`.
2. Extrae el slug de cada archivo (la parte entre `GUIDELINE-` y `.md`).
3. Muestra al redactor la lista de medios disponibles en este formato:

```
Medios disponibles:
  1. {slug-1}
  2. {slug-2}
  3. {slug-3}
  ...

¿Para qué medio es este artículo? (escribe el número o el nombre)
```

4. Espera la respuesta del redactor y asigna `MEDIO` al slug correspondiente.

Si `MEDIO` sí se proporcionó, continúa directamente al Paso 2.

---

## PASO 2 — GuidelineMissingError check

Verifica que existe el archivo `guidelines/GUIDELINE-{MEDIO}.md`.

Si **no existe**:

```
⚠️ GuidelineMissingError: No existe la guideline para '{MEDIO}'.

Usa `/crear-guideline {MEDIO}` primero para definir la voz editorial de este medio
y después vuelve a ejecutar este comando.
```

**DETENER el flujo aquí.** No continuar.

Si **existe**, continúa al Paso 2.5.

---

## PASO 2.5 — Detección de modo (mono-producto o guía multi-producto)

Este paso es **obligatorio** y se ejecuta siempre después de validar la guideline del medio.

### Si `N_URLS == 1`

Asigna `TIPO_ARTICULO = mono` **sin preguntar nada al redactor**. Continúa directamente al Paso 3 con `URL_PRODUCTO = URLS[0]`. Este es el comportamiento por defecto, idéntico al flujo histórico.

### Si `N_URLS >= 2`

**Pausa interactiva nueva.** El redactor debe decidir explícitamente qué quiere hacer con esas URLs:

```
He detectado {N_URLS} URLs de producto. ¿Qué prefieres?

  A) Una sola guía/comparativa con todos los productos
     (un único artículo multi-producto: recopilatorio, comparativa, top-N, etc.)

  B) {N_URLS} artículos separados, uno por producto
     (lanzaré el flujo mono-producto una vez por URL)

  C) Solo uno: dime cuál y descarto el resto

Responde A, B o C.
```

Comportamiento según la respuesta:

- **A) Guía multi-producto** → asigna `TIPO_ARTICULO = multi`. Continúa al sub-paso 2.5.1 para elegir el formato de guía.
- **B) Artículos separados** → muestra al redactor el siguiente mensaje y termina la ejecución actual:
  ```
  Entendido. Para no mezclar contextos, ejecuta `/crear-articulo` una vez por URL:

    1. /crear-articulo {URLS[0]} {MEDIO}
    2. /crear-articulo {URLS[1]} {MEDIO}
    ...

  (Si quieres que el sistema los lance en cadena automáticamente, pídemelo y lo
  hago: ejecutaré el flujo mono completo URL por URL, parando en cada pausa
  interactiva tuya como siempre.)
  ```
  No continúes hasta que el redactor confirme cómo prosigue.
- **C) Solo uno** → pide al redactor que indique el número o pegue la URL elegida. Asigna `URL_PRODUCTO` a esa URL, `TIPO_ARTICULO = mono` y continúa al Paso 3.

### Sub-paso 2.5.1 — Elegir el formato de guía (solo si `TIPO_ARTICULO = multi`)

Lee la guideline `guidelines/GUIDELINE-{MEDIO}.md` y extrae la lista de **formatos multi-producto admitidos** por ese medio (busca un bloque titulado "Formatos multi-producto admitidos" o equivalente). Cada guideline declara su propio subconjunto del catálogo universal:

| `FORMATO_GUIA` | Cuándo lo elige el redactor |
|---|---|
| `comparativa` | 2-N productos del mismo tipo enfrentados. "Cuál ganaría". |
| `recopilatorio` | N ofertas con hilo común (categoría, momento, tienda). "Chollos de Amazon hoy". |
| `top-n` | Ranking de los mejores N en una categoría. "Los 5 mejores smartwatches 2026". |
| `por-presupuesto` | N productos por franjas de precio. "Robots a 100€, 200€ y 400€". |
| `por-uso` | N productos por caso de uso o perfil. "Auriculares según uses gym, oficina o viajes". |
| `longtail-marca` | Catálogo destacado de una marca. "Por qué Garmin sigue siendo referencia: estos 4 modelos". |

Presenta al redactor **solo los formatos que admite la guideline** del medio elegido. Numera 1..N y deja una opción libre por si el redactor quiere proponer otro encaje:

```
Formatos de guía soportados por {MEDIO}:

  1. {formato-1} — {descripción corta del formato según la guideline}
  2. {formato-2} — {descripción}
  ...

¿Qué formato encaja mejor con estos {N_URLS} productos?
(responde con el número o escribe el slug del formato)
```

Asigna `FORMATO_GUIA` a la elección del redactor. Si el redactor escribe un slug que no figura en la lista, recuérdale los formatos admitidos por el medio y vuelve a preguntar; no aceptes formatos no soportados.

Continúa al Paso 3 con `URLS` (lista completa), `TIPO_ARTICULO = multi` y `FORMATO_GUIA` ya asignados.

---

## PASO 3 — Subagente: product-researcher

### Si `TIPO_ARTICULO = mono`

Invoca el subagente `product-researcher` con las siguientes instrucciones:

```
Investiga el producto en esta URL: {URL_PRODUCTO}

Tu objetivo es extraer una ficha de producto estructurada con:
- Nombre completo del producto
- ASIN o ID de producto (si aplica)
- Precio actual y precio anterior (si hay oferta)
- Porcentaje de descuento (calculado)
- Características principales (bullet points de la ficha)
- Categoría del producto
- Valoración media y número de reseñas (si está disponible)
- Disponibilidad (stock, Prime, envío)
- URL canónica del producto
- Cualquier dato relevante adicional (variantes, colores, tamaños, etc.)

Si no puedes acceder a la URL (bloqueo, CAPTCHA, error), lanza URLBlockedError:
  "URLBlockedError: No se pudo acceder a {URL_PRODUCTO}. Por favor, pega manualmente
   la ficha del producto (título, precio, características, valoraciones)."
   Espera a que el redactor pegue la información y úsala como fuente.

Devuelve la ficha en formato markdown estructurado.
```

Guarda el resultado como `FICHA_PRODUCTO`.

### Si `TIPO_ARTICULO = multi`

Invoca al subagente `product-researcher` **N veces en paralelo**, una por cada URL en `URLS`. Lanza todas las llamadas en un único turno (un solo mensaje del orquestador con N invocaciones simultáneas de la tool Agent) para que las extracciones de Playwright corran en paralelo y se reduzca el tiempo total.

Para cada URL `URLS[i]`, las instrucciones al subagente son **idénticas a las del flujo mono**, sustituyendo `{URL_PRODUCTO}` por `URLS[i]`.

Recolecta las fichas devueltas en una lista ordenada `FICHAS_PRODUCTOS = [FICHA_1, FICHA_2, ..., FICHA_N]`, **preservando el orden en el que el redactor pegó las URLs**. Ese orden suele ser intencional (el primero es el "destacado", o sigue una jerarquía narrativa) y los agentes posteriores lo respetan.

**Gestión de errores en lote:**

- Si **una o varias** invocaciones devuelven `URLBlockedError`, presenta al redactor la lista de URLs bloqueadas y pídele que pegue los datos manualmente **solo para esas**. Las que sí cargaron quedan validadas como `fuente: automatica-playwright`. Las manuales como `fuente: manual`.
- Si **todas** las URLs fallan con `URLBlockedError`, presenta el error agregado y pide al redactor que pegue los datos de todos los productos (puede hacerlo en un solo mensaje, separados por una línea en blanco o un encabezado por producto).
- En ningún caso continúes con menos de 2 fichas completas si `TIPO_ARTICULO = multi`. Si tras los intentos manuales solo queda 1 ficha completa, pregunta al redactor si quiere convertir el flujo a mono-producto (`TIPO_ARTICULO = mono` con la única ficha disponible) o reintentar con una URL distinta para reemplazar la fallida.

---

## PASO 4 — Subagente: angle-picker (genera shortlist, no elige)

> **Regla absoluta del flujo v3.1:** el angle-picker **nunca** propone una única combinación de ángulo + persona. Siempre devuelve un menú de 3 ángulos candidatos + 2-3 personas candidatas. La elección la hace el redactor en la pausa A. Si un agente devuelve una sola propuesta, el orquestador lo rechaza y vuelve a invocarlo recordando el formato menú.

### Si `TIPO_ARTICULO = mono`

Invoca el subagente `angle-picker` con las siguientes instrucciones:

```
Analiza la siguiente ficha de producto y la guideline editorial del medio.
Tu output es SIEMPRE un menú de opciones, no una decisión.

FICHA DEL PRODUCTO:
{FICHA_PRODUCTO}

MEDIO DESTINO: {MEDIO}
Guideline del medio: lee el archivo guidelines/GUIDELINE-{MEDIO}.md

ÁNGULOS DISPONIBLES:
- recomendacion-personal
- liquidacion
- comparativa
- precio-psicologico
- uso-practico
- tendencia

PERSONAS-REDACTORAS DISPONIBLES (catálogo `knowledge/personas-redactoras/`):
- el-que-llega-tarde-a-casa
- el-techie-que-prueba-todo
- el-bloguer-de-moda
- el-deportista-amateur
- la-beauty-editor
- el-padre-con-hijos-pequenos
- el-manitas-de-fin-de-semana
- el-que-viaja-ligero

Devuelve OBLIGATORIAMENTE un menú con esta estructura (formato exacto definido en
tu agent file, sección "Output esperado modo mono"):

1. 3 ÁNGULOS CANDIDATOS rankeados. Para cada uno: por qué encaja (datos concretos
   de la ficha), cómo se enfocaría el artículo (1 frase), y posición del precio
   según `knowledge/posicion-precio-por-angulo.md`.
   (Si la guideline veta algún ángulo, no lo incluyas. Mínimo 2 candidatos.)

2. 2-3 PERSONAS-REDACTORAS CANDIDATAS rankeadas. Para cada una: por qué encaja
   con la categoría del producto, y con qué ángulos del shortlist combina mejor.

3. RECOMENDACIÓN RAZONADA en una línea (no vinculante): tu combinación de cabeza
   ángulo + persona y por qué. El redactor puede ignorarla.

4. NOTAS opcionales para headline-generator y writer aplicables a cualquier
   combinación del shortlist.

NO ELIJAS por el redactor. NO produzcas titulares. NO redactes el cuerpo.
```

Guarda el resultado como `SHORTLIST_EDITORIAL` (incluye los 3 ángulos candidatos, las 2-3 personas candidatas, las posiciones de precio asociadas y la recomendación razonada).

### Si `TIPO_ARTICULO = multi`

Invoca el subagente `angle-picker` con instrucciones de **modo multi-producto**:

```
Analiza la siguiente LISTA de fichas de producto y la guideline editorial del medio.
Tu output es SIEMPRE un menú, no una decisión. El redactor elegirá en la pausa A.

FORMATO_GUIA confirmado por el redactor: {FORMATO_GUIA}
(recopilatorio | comparativa | top-n | por-presupuesto | por-uso | longtail-marca)

FICHAS DE PRODUCTO (en orden, respetando el orden del redactor):
{FICHA_1}
---
{FICHA_2}
---
...
{FICHA_N}

MEDIO DESTINO: {MEDIO}
Guideline del medio: lee el archivo guidelines/GUIDELINE-{MEDIO}.md (sección
"Multi-producto" y/o "Formatos multi-producto admitidos").

ÁNGULOS DISPONIBLES:
- recomendacion-personal
- liquidacion
- comparativa
- precio-psicologico
- uso-practico
- tendencia

Devuelve OBLIGATORIAMENTE un menú con esta estructura (formato exacto definido en
tu agent file, sección "Output esperado modo multi"):

1. 3 ÁNGULOS GLOBALES CANDIDATOS rankeados. Para cada uno: por qué encaja con el
   conjunto (datos concretos de las fichas), cómo se enfocaría la guía (1 frase),
   posición del precio, y una propuesta de HILO CONDUCTOR distinta por ángulo
   (al menos para los 2 primeros candidatos).

2. 2-3 PERSONAS-REDACTORAS CANDIDATAS rankeadas (una sola firmará la guía completa).
   Para cada una: por qué encaja con la categoría dominante del conjunto.

3. ENCAJE del FORMATO_GUIA elegido por el redactor: 1 frase confirmando si encaja
   con el conjunto o señalando un formato alternativo si no encaja.

4. RECOMENDACIÓN RAZONADA en una línea (no vinculante): ángulo + persona + hilo.

5. NOTAS para headline-generator y writer (producto destacado, orden narrativo
   recomendado, datos repetidos a no machacar, estilos de titular que encajan
   mejor con el FORMATO_GUIA).

NO ELIJAS por el redactor. NO produzcas titulares. NO redactes el cuerpo.
```

Guarda el resultado como `SHORTLIST_EDITORIAL` (incluye los 3 ángulos candidatos, las 2-3 personas candidatas, las propuestas de hilo conductor por ángulo, las posiciones de precio asociadas y la recomendación razonada).

---

## PASO 5 — PAUSA INTERACTIVA A: el redactor elige ángulo y persona desde el menú

**No continúes sin respuesta del redactor.** Este paso es **elección directa**: no hay "propuesta a confirmar", se presenta el shortlist y el redactor decide ambas variables (y, en multi, también el hilo conductor) desde el primer momento.

### Si `TIPO_ARTICULO = mono`

Muestra al redactor el menú completo con el shortlist recibido del angle-picker:

```
## Elige el enfoque editorial

### Ángulos candidatos
  1. {angulo-1}  → {por qué encaja, 1 línea} · precio: {posicion}
  2. {angulo-2}  → {por qué encaja, 1 línea} · precio: {posicion}
  3. {angulo-3}  → {por qué encaja, 1 línea} · precio: {posicion}

### Personas-redactoras candidatas
  A. {persona-1} — {por qué encaja, 1 línea}
  B. {persona-2} — {por qué encaja, 1 línea}
  C. {persona-3} — {por qué encaja, 1 línea}   (si aplica)

Recomendación de cabeza (no vinculante): {ángulo-N} + {persona-X}.

---
Elige ángulo + persona en un único mensaje. Formatos válidos:
  · "2A"  → ángulo 2 + persona A
  · "liquidacion + el-deportista-amateur"  → slugs directos
  · "1, B"  → ángulo 1 + persona B
  · O escribe un ángulo / persona fuera del menú si lo tienes claro
    (siempre dentro del catálogo permitido).
```

### Si `TIPO_ARTICULO = multi`

Muestra el menú enriquecido con propuestas de hilo conductor por ángulo:

```
## Elige el enfoque editorial de la guía

**Formato de guía:** {FORMATO_GUIA}
{si el angle-picker señaló que el FORMATO_GUIA no encaja del todo, muéstralo aquí en 1 línea}

### Ángulos globales candidatos (con hilo conductor propuesto por ángulo)
  1. {angulo-1} · precio: {posicion}
     Hilo propuesto: "{hilo-1}"
     Por qué encaja: {1 línea}
  2. {angulo-2} · precio: {posicion}
     Hilo propuesto: "{hilo-2}"
     Por qué encaja: {1 línea}
  3. {angulo-3} · precio: {posicion}
     {Hilo propuesto si lo hay} · Por qué encaja: {1 línea}

### Personas-redactoras candidatas (una para toda la guía)
  A. {persona-1} — {por qué encaja, 1 línea}
  B. {persona-2} — {por qué encaja, 1 línea}
  C. {persona-3} — {por qué encaja, 1 línea}   (si aplica)

Recomendación de cabeza (no vinculante): {ángulo-N} + {persona-X} + hilo "{frase}".

---
Elige en un único mensaje: ángulo + persona + (opcional) hilo conductor.
Formatos válidos:
  · "1A"           → toma ángulo 1, persona A, y el hilo propuesto para el ángulo 1
  · "2A, hilo: ..."→ toma ángulo 2, persona A, y reescribe el hilo conductor
  · "cambiar formato" → reabre el sub-paso 2.5.1 para cambiar el FORMATO_GUIA
  · Slugs directos también válidos.
```

Espera la respuesta. Parsea la elección del redactor (número+letra, slugs directos o combinación libre) y asigna:
- `ANGULO_FINAL` con el ángulo elegido por el redactor.
- `PERSONA_REDACTORA_FINAL` con el slug de la persona elegida.
- `POSICION_PRECIO_FINAL` la que el angle-picker asoció al ángulo elegido (consulta `knowledge/posicion-precio-por-angulo.md` si el redactor eligió un ángulo fuera del menú).
- En multi, además `HILO_CONDUCTOR_FINAL`: el hilo propuesto por el angle-picker para el ángulo elegido, o el que el redactor haya reescrito.
- Si el redactor escribe "cambiar formato" (multi), vuelve al sub-paso 2.5.1 y, tras nuevo `FORMATO_GUIA`, reinvoca al angle-picker en multi.
- Si la elección del redactor es ambigua (no se entiende qué ángulo o qué persona ha elegido), repregunta una sola vez con la lista numerada en compacto. No interpretes a la libre.

> En esta pausa **no se habla todavía de titulares**. El titular llega en la pausa B.

---

## PASO 6 — Subagente: headline-generator

### Si `TIPO_ARTICULO = mono`

Invoca el subagente `headline-generator` con las siguientes instrucciones:

```
Genera 30 titulares variados y muy clicables para este artículo de oferta.

FICHA DEL PRODUCTO:
{FICHA_PRODUCTO}

ÁNGULO CONFIRMADO: {ANGULO_FINAL}

MEDIO DESTINO: {MEDIO}
Lee la guideline en guidelines/GUIDELINE-{MEDIO}.md, prestando especial atención
al bloque "Recetas de titular del medio" si existe. Esa sección sobrescribe al
manual universal en caso de conflicto.

Lee también el manual universal de titulares en knowledge/headline-recipes.md y
las frases vetadas globales en knowledge/frases-vetadas.md.

Devuelve los 30 titulares en el formato exacto que define tu agent: una línea por
titular, con etiqueta de estilo y longitud entre corchetes. Sin numeración, sin
bullets, sin negritas.
```

Guarda el resultado como `TITULARES_30`. Conserva tanto la lista entera como el
estilo de cada titular para poder filtrar después.

### Si `TIPO_ARTICULO = multi`

Invoca el subagente `headline-generator` con instrucciones de modo guía:

```
Genera 30 titulares variados y muy clicables para una GUÍA MULTI-PRODUCTO.

TIPO_ARTICULO: multi
FORMATO_GUIA: {FORMATO_GUIA}
ÁNGULO CONFIRMADO: {ANGULO_FINAL}
HILO CONDUCTOR: {HILO_CONDUCTOR_FINAL}

FICHAS (en orden, respetando el orden del redactor):
{FICHA_1}
---
{FICHA_2}
---
...
{FICHA_N}

MEDIO DESTINO: {MEDIO}
Lee la guideline en guidelines/GUIDELINE-{MEDIO}.md, prestando especial atención
a las secciones "Recetas de titular del medio" y "Titulares para multi-producto"
(o equivalente). Esa sección sobrescribe al manual universal en caso de conflicto.

Lee también el manual universal de titulares en knowledge/headline-recipes.md y
las frases vetadas globales en knowledge/frases-vetadas.md.

Reglas específicas para titulares de guía multi-producto:
- Reflejar el FORMATO_GUIA en la forma del titular (recopilatorio → "X chollos / X
  ofertas que…", comparativa → "X frente a Y" o "Comparamos…", top-n → "Los N
  mejores…", por-presupuesto → "Por menos de X€…", por-uso → "Para [perfil/uso]…",
  longtail-marca → "[Marca]: estos N modelos…").
- Si el formato lo pide, el número aparece en el H1 (3, 5, 7, 10…). Si la guideline
  prohíbe ese cuantificador en subtítulo o cuerpo, se respeta esa prohibición; el
  número solo va en H1.
- No nombrar más de UNA marca/producto del conjunto en el H1, salvo en
  `comparativa` directa de dos productos (donde puede aparecer cada marca).
- El titular vende el CONJUNTO, no un producto suelto. Si sólo se nombra un
  producto del lote, el resto debe quedar implícito en el "X productos que…".

Devuelve los 30 titulares en el formato exacto que define tu agent: una línea por
titular, con etiqueta de estilo y longitud entre corchetes. Sin numeración, sin
bullets, sin negritas.
```

Guarda el resultado como `TITULARES_30`. Conserva la lista entera y el estilo de
cada titular para poder filtrar en la pausa B.

---

## PASO 7 — PAUSA INTERACTIVA B: elegir titular

**No continúes sin respuesta del redactor.**

De los 30 titulares devueltos, **selecciona automáticamente uno por cada estilo único** (los más fuertes según el orden en que los devolvió el `headline-generator`: el primer titular de cada estilo se considera el más representativo). Esto genera una **vista resumida** de 6-10 titulares, dependiendo de cuántos estilos se hayan usado.

Muestra la selección representativa numerada del 1 al N, con su etiqueta de estilo entre paréntesis:

```
## 10 titulares representativos (uno por estilo)

  1. [seo] {titular 1}
  2. [primera-persona] {titular 2}
  3. [oferta-directa] {titular 3}
  4. [review-rapida] {titular 4}
  5. [viral-comillas] {titular 5}
  6. [clicbait-controlado] {titular 6}
  7. [problema-solucion] {titular 7}
  8. [urgencia] {titular 8}
  9. [comparativa] {titular 9}
  10. [uso-concreto] {titular 10}

---
¿Cuál quieres?
  - Escribe el **número** del titular que prefieras (1-N)
  - Escribe **"ver 30"** para ver los 30 candidatos completos agrupados por estilo
  - Escribe **"editar N"** para tomar el titular N y dictarme cómo cambiarlo
  - Escribe **"otra tanda"** para regenerar 30 titulares nuevos
  - Escribe **el titular** que quieras tú directamente
```

Comportamientos posibles:

- **El redactor escribe un número:** asigna `TITULAR_FINAL` al titular correspondiente.
- **El redactor escribe "ver 30":** muestra los 30 agrupados por etiqueta de estilo, numerados del 1 al 30, y vuelve a esperar elección.
- **El redactor escribe "editar N":** muestra el titular N y pide la nueva versión. Asigna `TITULAR_FINAL` a la versión modificada.
- **El redactor escribe "otra tanda":** vuelve al Paso 6 con la instrucción adicional "regenera 30 titulares con un enfoque distinto al de la tanda anterior" y luego retorna a esta pausa.
- **El redactor dicta un titular libre:** asigna `TITULAR_FINAL` al texto dictado tal cual.

> No reescribas el titular dictado por el redactor salvo que viole frases vetadas explícitas. Si el dictado contiene una frase vetada, **avísalo** y pide confirmación antes de aplicar la corrección.

---

## PASO 8 — Subagente: writer

### Si `TIPO_ARTICULO = mono`

Invoca el subagente `writer` con las siguientes instrucciones:

```
Redacta un artículo de oferta completo para el medio {MEDIO}.

TIPO_ARTICULO: mono

DATOS DEL PRODUCTO:
{FICHA_PRODUCTO}

ÁNGULO EDITORIAL: {ANGULO_FINAL}
PERSONA-REDACTORA: {PERSONA_REDACTORA_FINAL}
  ↳ Lee el archivo knowledge/personas-redactoras/{PERSONA_REDACTORA_FINAL}.md
    ANTES de escribir nada. La persona define el punto de vista, las
    prioridades y el lenguaje natural del artículo.
POSICIÓN DEL PRECIO: {POSICION_PRECIO_FINAL}
  ↳ Regla transversal en knowledge/posicion-precio-por-angulo.md. Si el ángulo
    es no-protagonista de precio, NO abras la intro ni el primer H2/H3 con
    cifras de precio o descuento.

TITULAR: {TITULAR_FINAL}

MANIFIESTO EDITORIAL: lee knowledge/manifiesto-editorial.md. Atención especial
a los puntos 2.bis (test del bloguero), 2.ter (voz del medio + persona) y
2.quater (posición del precio según ángulo). El manifiesto manda sobre
cualquier guideline si entran en conflicto.

SCRATCHPAD HUMANO OBLIGATORIO (no va al draft): antes de redactar, contesta
en tu razonamiento interno las tres preguntas semilla de la persona-redactora
aplicadas a ESTE producto concreto. Las respuestas son las semillas de la
intro, el cuerpo y el cierre.

GUIDELINE DEL MEDIO: lee guidelines/GUIDELINE-{MEDIO}.md. Define el registro,
los anclajes mínimos, las frases vetadas/preferidas, longitud y disclaimer.
La paleta de recetas es REFERENCIA OPCIONAL, no menú obligatorio. Si construyes
el artículo desde el scratchpad sin apoyarte en recetas, deja el campo
`recetas: []` vacío.

EJEMPLOS PUBLICADOS: lee 2-3 archivos de knowledge/ejemplos-publicados/{MEDIO}/
con un ángulo o categoría parecidos para CALIBRAR voz, ritmo y vocabulario.
NUNCA copies la estructura. Si tu plan se parece al último draft del medio,
recalibra desde el scratchpad.

FRONTMATTER REQUERIDO (incluirlo al inicio del draft en bloque YAML):
```yaml
titulo: "{TITULAR_FINAL}"
medio: {MEDIO}
url_origen: {URL_PRODUCTO}
asin: {ASIN_si_aplica_o_omitir}
fecha: {fecha_hoy_en_formato_YYYY-MM-DD}
angulo: {ANGULO_FINAL}
persona_redactora: {PERSONA_REDACTORA_FINAL}
tipo_articulo: mono
recetas: []   # vacío si no te apoyas en recetas; si te apoyas, lista las usadas
estado: borrador
```

RUTA DE GUARDADO: drafts/{MEDIO}/{fecha_hoy_YYYYMMDD}-{slug-del-titular}.md
  El slug del titular: minúsculas, sin acentos, espacios reemplazados por guiones,
  máximo 50 caracteres.

Antes de guardar, aplica el paso de auto-revisión anti-IA descrito en tu agent
(paso 7). Cada coincidencia es una reescritura inmediata, no una nota para el editor.

Genera el artículo completo, no un esquema ni un borrador parcial.
Respeta longitud objetivo, estructura de anclajes fijos, posición de imagen y CTA,
frases preferidas y frases vetadas definidas en la guideline.
Incluye el disclaimer de afiliación en la posición especificada en la guideline
(o no lo incluyas si la guideline indica que el CMS lo añade automáticamente).
```

Guarda el resultado como `DRAFT_INICIAL` y la ruta como `RUTA_DRAFT`.

### Si `TIPO_ARTICULO = multi`

Invoca el subagente `writer` con instrucciones de modo guía multi-producto:

```
Redacta una GUÍA MULTI-PRODUCTO completa para el medio {MEDIO}.

TIPO_ARTICULO: multi
FORMATO_GUIA: {FORMATO_GUIA}
ÁNGULO GLOBAL: {ANGULO_FINAL}
PERSONA-REDACTORA: {PERSONA_REDACTORA_FINAL}
  ↳ Lee el archivo knowledge/personas-redactoras/{PERSONA_REDACTORA_FINAL}.md
    ANTES de escribir nada. Una sola persona para toda la guía.
POSICIÓN DEL PRECIO: {POSICION_PRECIO_FINAL}
  ↳ Si el ángulo es no-protagonista de precio, NO abras la intro ni el primer
    H2/H3 global con cifras. Cada bloque de producto también sigue la regla.
HILO CONDUCTOR: {HILO_CONDUCTOR_FINAL}
TITULAR: {TITULAR_FINAL}

FICHAS DE PRODUCTO (en orden, respeta el orden del redactor):
{FICHA_1}
---
{FICHA_2}
---
...
{FICHA_N}

GUIDELINE DEL MEDIO: lee el archivo guidelines/GUIDELINE-{MEDIO}.md y síguela
estrictamente. Presta especial atención a las secciones "Multi-producto",
"Formatos multi-producto admitidos" y a la plantilla por bloque de producto que
define el medio. La guideline es la única fuente normativa sobre estructura.

EJEMPLOS PUBLICADOS MULTI: lee 2-3 archivos de knowledge/ejemplos-publicados/{MEDIO}/
que sean también multi-producto o guías (recopilatorios, comparativas, tops). Si
no existen ejemplos multi en la carpeta del medio, calibra con los mono más
cercanos en voz y vocabulario.

REGLAS GENERALES PARA GUÍAS MULTI-PRODUCTO (las concretas las pone la guideline):
- El artículo es UNO solo, no N artículos pegados. Hay un hilo conductor común
  (HILO_CONDUCTOR) que se establece en la introducción y se cierra en el veredicto
  o cierre final.
- Cada bloque de producto:
  - Empieza con marca + modelo en el heading correspondiente.
  - No copia la fórmula del bloque anterior (variedad de aperturas).
  - Aplica la receta dominante de su bloque según indique la guideline.
- Las recetas GLOBALES (intro, veredicto, criterios) se aplican UNA SOLA VEZ, no
  por bloque.
- Precios: misma regla relativa que en mono salvo que la guideline permita cifra
  exacta en algún punto concreto.
- No inventes datos cruzados entre productos. Si comparas dos modelos y un dato
  no está en su ficha, no lo infieras; reescribe la comparación con lo que sí
  tienes.

FRONTMATTER REQUERIDO (incluirlo al inicio del draft en bloque YAML):
```yaml
titulo: "{TITULAR_FINAL}"
medio: {MEDIO}
url_origen: {URL_FICHA_1}             # URL del producto destacado / primero del orden
url_secundarias:                       # resto de URLs del conjunto, en orden
  - {URL_FICHA_2}
  - {URL_FICHA_3}
  - ...
fecha: {fecha_hoy_en_formato_YYYY-MM-DD}
angulo: {ANGULO_FINAL}
persona_redactora: {PERSONA_REDACTORA_FINAL}
tipo_articulo: multi
formato_guia: {FORMATO_GUIA}
n_productos: {N_URLS}
hilo_conductor: "{HILO_CONDUCTOR_FINAL}"
recetas: []                            # vacío si no te apoyas en recetas; si te apoyas, lista las usadas
estado: borrador
```

RUTA DE GUARDADO: drafts/{MEDIO}/{fecha_hoy_YYYYMMDD}-{slug-del-titular}.md
  Misma convención de slug que en mono.

Antes de guardar, aplica el paso de auto-revisión anti-IA. En multi añade además:
- Test de bloque intercambiable: si pego el bloque de producto N en cualquier otro
  artículo de guía cambiando el nombre, ¿seguiría sonando bien? Si la respuesta es
  sí, ese bloque es plantilla; reescríbelo con un dato específico del producto o
  un escenario concreto.
- Variedad de aperturas: no más de un bloque empieza con la misma estructura
  ("La/el [producto] de [marca]…", "[Marca] propone…", etc.).

Genera el artículo completo, no un esquema. Respeta longitud objetivo para multi
según la guideline.
```

Guarda el resultado como `DRAFT_INICIAL` y la ruta como `RUTA_DRAFT`.

---

## PASO 9 — Subagente: editor-in-chief

Invoca el subagente `editor-in-chief` con las siguientes instrucciones:

```
Realiza el pase editorial final de este artículo de oferta.

RUTA DEL DRAFT: {RUTA_DRAFT}

MEDIO DESTINO: {MEDIO}
TIPO_ARTICULO: {TIPO_ARTICULO}             # mono o multi
{si TIPO_ARTICULO=multi:}
FORMATO_GUIA: {FORMATO_GUIA}
HILO CONDUCTOR: {HILO_CONDUCTOR_FINAL}
N_PRODUCTOS: {N_URLS}
{fin si multi}

GUIDELINE DEL MEDIO: lee el archivo guidelines/GUIDELINE-{MEDIO}.md
ÁNGULO APLICADO: {ANGULO_FINAL}
PERSONA-REDACTORA APLICADA: {PERSONA_REDACTORA_FINAL}
  ↳ Aplica el filtro previo del test del bloguero comprobando que el texto
    suena a esa persona, no a IA con plantilla. Si no suena, devuelve el draft
    al writer en lugar de pulirlo.
POSICIÓN DEL PRECIO: {POSICION_PRECIO_FINAL}
  ↳ Si el ángulo es no-protagonista y la intro o el primer H2/H3 abre con
    precio, reescribe.

CRITERIOS DE REVISIÓN (en orden de prioridad):
0a. TEST DEL BLOGUERO (filtro previo): ¿suena a humano experto de la categoría
    o a IA con plantilla? Si suena a IA, DEVUELVE el draft al writer.
0b. COHERENCIA CON LA PERSONA-REDACTORA: ¿el texto se reconoce como
    {PERSONA_REDACTORA_FINAL}? ¿Habla en sus escenarios, con su vocabulario?
0c. POSICIÓN DEL PRECIO: si el ángulo es no-protagonista, ¿la intro y el primer
    H2/H3 no abren con precio? Si fallan, reescribe.
1. Voz del medio: ¿suena a {MEDIO}? ¿Usa el registro correcto?
2. Ángulo: ¿el artículo mantiene coherencia con el ángulo {ANGULO_FINAL} de
   principio a fin?
3. Titular: ¿se respeta tal cual lo confirmó el redactor en la pausa B?
4. Frases vetadas: ¿hay alguna de las frases vetadas (globales o del medio)?
   Sustitúyelas.
5. Frases preferidas: ¿se usan naturalmente las frases preferidas del medio?
6. Longitud: ¿está dentro del rango objetivo de la guideline para el TIPO_ARTICULO?
7. Estructura: ¿los anclajes mínimos del medio están? (Recetas son opcionales
   en v3: no penalices su ausencia si el artículo pasa el test del bloguero.)
8. CTA y disclaimer: ¿posición correcta? ¿Texto literal del disclaimer?
9. Frontmatter: ¿completo y correcto? Sin [PENDIENTE]. Incluye
   `persona_redactora`. En multi, ¿figura tipo_articulo: multi, formato_guia,
   n_productos, hilo_conductor y url_secundarias?
10. Auto-revisión anti-IA: ¿queda alguna muletilla típica de IA, traducción
    mecánica de specs o frase-resumen genérica? Reescríbela.
11. Último párrafo: ¿cierra bien sin frases de relleno?

SI TIPO_ARTICULO=multi, añade además los siguientes puntos al checklist
(en el agent file de editor-in-chief estos cinco puntos figuran como #9 a #13,
porque el checklist canónico del agente tiene 8 puntos base, no 11):

12. Hilo conductor: ¿se establece en la introducción y se retoma en el cierre /
    veredicto? Si solo aparece en la intro, refuérzalo en el cierre.
13. Bloque por producto: ¿cada bloque empieza con marca + modelo? ¿No copia la
    fórmula de apertura del anterior?
14. Recetas globales aplicadas una sola vez (intro, veredicto, criterios), no por
    bloque. Si una receta global aparece duplicada por bloque, consolídala.
15. Test de bloque intercambiable: ¿algún bloque podría pegarse en otra guía sin
    cambios sustanciales? Reescríbelo con un dato/escenario específico del producto.
16. Coherencia entre fichas y prosa: si un dato aparece en la prosa, está en la
    ficha correspondiente. No hay datos cruzados inventados.

Aplica las correcciones DIRECTAMENTE sobre el archivo con Edit. Devuelve:
- Listado breve de las correcciones realizadas (máximo 8 items en mono, 13 en multi)
- Valoración 1-5 de alineación con la guideline (5 = perfecto)
- Confirmación de que el frontmatter está completo y sin [PENDIENTE]
```

Guarda las correcciones como `LOG_CORRECCIONES` y la valoración como `VALORACION`.

---

## PASO 10 — Informe final al redactor

### Si `TIPO_ARTICULO = mono`

Muestra el siguiente resumen:

```
## Artículo generado

**Ruta del draft:** {RUTA_DRAFT}
**Medio:** {MEDIO}
**Tipo:** mono-producto
**Ángulo:** {ANGULO_FINAL}
**Persona-redactora:** {PERSONA_REDACTORA_FINAL}
**Titular:** {TITULAR_FINAL}

### Correcciones del editor en jefe:
{LOG_CORRECCIONES}

**Alineación con la guideline:** {VALORACION}/5
```

### Si `TIPO_ARTICULO = multi`

Muestra el resumen enriquecido:

```
## Guía multi-producto generada

**Ruta del draft:** {RUTA_DRAFT}
**Medio:** {MEDIO}
**Tipo:** guía multi-producto ({N_URLS} productos)
**Formato de guía:** {FORMATO_GUIA}
**Ángulo global:** {ANGULO_FINAL}
**Persona-redactora:** {PERSONA_REDACTORA_FINAL}
**Hilo conductor:** {HILO_CONDUCTOR_FINAL}
**Titular:** {TITULAR_FINAL}

### Productos incluidos (en orden):
1. {nombre_producto_1}
2. {nombre_producto_2}
...
{N}. {nombre_producto_N}

### Correcciones del editor en jefe:
{LOG_CORRECCIONES}

**Alineación con la guideline:** {VALORACION}/5
```

---

## PASO 11 — Bloque "Antes de cerrar"

Muestra siempre este bloque al final, sin omitirlo:

```
## Antes de cerrar

- ¿Editaste el draft manualmente tras el editor en jefe? Si introdujiste un patrón
  nuevo o corregiste algo recurrente → añádelo a `guidelines/GUIDELINE-{MEDIO}.md`
  para que los próximos artículos lo incorporen desde el inicio.

- ¿La ficha del producto vino incompleta o el product-researcher tuvo que pedir
  ayuda manual? → Registra el dominio o patrón problemático en
  `knowledge/notas-degradacion.md` para tenerlo documentado.

- ¿Ninguno de los 30 titulares te convenció y los regeneraste varias veces? →
  Plantéate ajustar el bloque "Recetas de titular del medio" de la guideline para
  acotar estilos o vocabulario.

- ¿Has actualizado `medios.md` con la fecha de la última publicación en {MEDIO}?
```

---

## Reglas de comportamiento general

- **No inventes datos del producto.** Si la ficha está incompleta, espera a que el redactor la complete antes de continuar. En multi, esto aplica producto por producto: si una sola ficha tiene huecos, se rellena antes de pasar al ángulo.
- **No saltes las pausas interactivas.** En mono hay 2 pausas (A: ángulo, B: titular). En multi hay 3 pausas (2.5: detección + formato de guía, A: ángulo + hilo conductor, B: titular). Todas requieren confirmación explícita del redactor; nunca las asume el sistema.
- **Detección de modo es automática solo cuando es trivial.** Si solo hay 1 URL, el sistema asume `mono` sin preguntar. Si hay 2+, **siempre** se pregunta — no infieras el modo a partir del medio o de patrones de la URL.
- **Si un subagente falla**, informa claramente qué subagente falló, por qué (si se sabe) y qué necesita el redactor para continuar. En multi, si solo falla la extracción de una de las N URLs, el resto sigue avanzando; pide datos manuales solo para la que falló.
- **Mantén el estado** entre pasos:
  - Comunes a todos los flujos: `MEDIO`, `TIPO_ARTICULO`, `ANGULO_FINAL`, `PERSONA_REDACTORA_FINAL`, `POSICION_PRECIO_FINAL`, `TITULARES_30`, `TITULAR_FINAL`, `RUTA_DRAFT`, `LOG_CORRECCIONES`, `VALORACION`.
  - Solo mono: `URL_PRODUCTO`, `FICHA_PRODUCTO`.
  - Solo multi: `URLS`, `N_URLS`, `FICHAS_PRODUCTOS`, `FORMATO_GUIA`, `HILO_CONDUCTOR_FINAL`.
- **Formato de fechas:** DD/MM/YYYY para mostrar al redactor, YYYY-MM-DD para el frontmatter del draft, YYYYMMDD para el nombre del archivo.
- **Una sola guía por invocación.** Si el redactor elige opción B en la pausa 2.5 (artículos separados), el flujo actual termina y se le pide que lance `/crear-articulo` una vez por URL. No intentes encadenar N flujos mono en una misma sesión salvo que el redactor lo pida explícitamente.
