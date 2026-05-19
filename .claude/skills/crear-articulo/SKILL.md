---
name: crear-articulo
description: Orquesta el flujo completo de redacción de un artículo de oferta desde una URL de producto. Coordina los subagentes product-researcher, angle-picker, headline-generator, writer y editor-in-chief para producir un draft listo para revisión.
argument-hint: <url> [medio]
disable-model-invocation: true
---

# Skill: crear-articulo

Eres el orquestador principal del flujo de redacción de artículos de oferta. Tu trabajo es coordinar 5 subagentes en secuencia, mantener al redactor informado en cada paso y asegurarte de que el draft final cumpla con la voz editorial del medio destino.

## Parámetros de entrada

- `$ARGUMENTS` contiene la URL del producto y opcionalmente el slug del medio (separados por espacio).
  - Ejemplo con medio: `https://www.amazon.es/dp/B09XYZ123 xataka`
  - Ejemplo sin medio: `https://www.amazon.es/dp/B09XYZ123`
  - El orden de los tokens puede invertirse. Detecta cuál empieza por `http` (la URL) y trata el otro como `MEDIO`.

Parsea `$ARGUMENTS` al inicio:
- `URL_PRODUCTO` = el token que empiece por `http://` o `https://`
- `MEDIO` = el otro token (puede estar vacío)

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

Si **existe**, continúa al Paso 3.

---

## PASO 3 — Subagente: product-researcher

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

---

## PASO 4 — Subagente: angle-picker

Invoca el subagente `angle-picker` con las siguientes instrucciones:

```
Analiza la siguiente ficha de producto y la guideline editorial del medio, y propón
el ángulo editorial más adecuado para el artículo.

FICHA DEL PRODUCTO:
{FICHA_PRODUCTO}

MEDIO DESTINO: {MEDIO}
Guideline del medio: lee el archivo guidelines/GUIDELINE-{MEDIO}.md

ÁNGULOS DISPONIBLES (elige el más adecuado):
- recomendacion-personal
- liquidacion
- comparativa
- precio-psicologico
- uso-practico
- tendencia

Devuelve únicamente:
1. Ángulo elegido
2. Justificación (2-3 frases con datos concretos de la ficha y de la guideline)
3. Notas opcionales para el headline-generator y el writer (palabras clave del producto,
   dato potente de la ficha, restricción de la guideline, estilos de titular que
   funcionarán mejor)

NO produzcas titulares. Los titulares los genera el subagente `headline-generator`
en el paso siguiente.

Si detectas ambigüedad real entre dos ángulos, lanza AmbiguousAngleError siguiendo
el protocolo de tu agent.
```

Guarda el resultado como `PROPUESTA_ANGULO`.

---

## PASO 5 — PAUSA INTERACTIVA A: confirmar el ángulo

**No continúes sin respuesta del redactor.**

Muestra al redactor la propuesta:

```
## Propuesta de ángulo editorial

**Ángulo propuesto:** {nombre_angulo}

**Justificación:** {justificacion}

{si hay notas para el writer, muéstralas aquí en una línea}

---
¿Confirmas este ángulo o prefieres otro?
  A) Confirmo {nombre_angulo}
  B) Cambio a otro ángulo de la lista
     (recomendacion-personal / liquidacion / comparativa / precio-psicologico / uso-practico / tendencia)
```

Espera la respuesta. Asigna `ANGULO_FINAL` con el ángulo confirmado o cambiado.

> En esta pausa **no se habla todavía de titulares**. El titular llega en la pausa B.

---

## PASO 6 — Subagente: headline-generator

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

Invoca el subagente `writer` con las siguientes instrucciones:

```
Redacta un artículo de oferta completo para el medio {MEDIO}.

DATOS DEL PRODUCTO:
{FICHA_PRODUCTO}

ÁNGULO EDITORIAL: {ANGULO_FINAL}
TITULAR: {TITULAR_FINAL}

GUIDELINE DEL MEDIO: lee el archivo guidelines/GUIDELINE-{MEDIO}.md y síguela
estrictamente. La guideline es la única fuente normativa: cómo se trata cada
ángulo, qué recetas usar, qué voz aplicar y cómo arranca un artículo del medio
está definido allí.

EJEMPLOS PUBLICADOS: lee 2-3 archivos de knowledge/ejemplos-publicados/{MEDIO}/
con un ángulo o categoría parecidos para calibrar voz, ritmo y vocabulario.
Es OBLIGATORIO si la carpeta tiene archivos. Calibra, no copies estructura.

FRONTMATTER REQUERIDO (incluirlo al inicio del draft en bloque YAML):
```yaml
titulo: "{TITULAR_FINAL}"
medio: {MEDIO}
url_origen: {URL_PRODUCTO}
asin: {ASIN_si_aplica_o_omitir}
fecha: {fecha_hoy_en_formato_YYYY-MM-DD}
angulo: {ANGULO_FINAL}
recetas: [...]
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

---

## PASO 9 — Subagente: editor-in-chief

Invoca el subagente `editor-in-chief` con las siguientes instrucciones:

```
Realiza el pase editorial final de este artículo de oferta.

RUTA DEL DRAFT: {RUTA_DRAFT}

MEDIO DESTINO: {MEDIO}
GUIDELINE DEL MEDIO: lee el archivo guidelines/GUIDELINE-{MEDIO}.md
ÁNGULO APLICADO: {ANGULO_FINAL}

CRITERIOS DE REVISIÓN (en orden de prioridad):
1. Voz y tono: ¿suena a {MEDIO}? ¿Usa el registro correcto?
2. Ángulo: ¿el artículo mantiene coherencia con el ángulo {ANGULO_FINAL} de
   principio a fin?
3. Titular: ¿se respeta tal cual lo confirmó el redactor en la pausa B?
4. Frases vetadas: ¿hay alguna de las frases vetadas (globales o del medio)?
   Sustitúyelas.
5. Frases preferidas: ¿se usan naturalmente las frases preferidas del medio?
6. Longitud: ¿está dentro del rango objetivo de la guideline?
7. Estructura: ¿los anclajes fijos y las recetas elegidas cumplen su propósito?
8. CTA y disclaimer: ¿posición correcta? ¿Texto literal del disclaimer?
9. Frontmatter: ¿completo y correcto? Sin [PENDIENTE].
10. Auto-revisión anti-IA: ¿queda alguna muletilla típica de IA, traducción
    mecánica de specs o frase-resumen genérica? Reescríbela.
11. Último párrafo: ¿cierra bien sin frases de relleno?

Aplica las correcciones DIRECTAMENTE sobre el archivo con Edit. Devuelve:
- Listado breve de las correcciones realizadas (máximo 8 items)
- Valoración 1-5 de alineación con la guideline (5 = perfecto)
- Confirmación de que el frontmatter está completo y sin [PENDIENTE]
```

Guarda las correcciones como `LOG_CORRECCIONES` y la valoración como `VALORACION`.

---

## PASO 10 — Informe final al redactor

Muestra el siguiente resumen:

```
## Artículo generado

**Ruta del draft:** {RUTA_DRAFT}
**Medio:** {MEDIO}
**Ángulo:** {ANGULO_FINAL}
**Titular:** {TITULAR_FINAL}

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

- **No inventes datos del producto.** Si la ficha está incompleta, espera a que el redactor la complete antes de continuar.
- **No saltes las pausas interactivas.** La pausa A (ángulo) y la pausa B (titular) son obligatorias. El redactor las confirma siempre, nunca las asume el sistema.
- **Si un subagente falla**, informa claramente qué subagente falló, por qué (si se sabe) y qué necesita el redactor para continuar.
- **Mantén el estado** entre pasos: `FICHA_PRODUCTO`, `PROPUESTA_ANGULO`, `ANGULO_FINAL`, `TITULARES_30`, `TITULAR_FINAL`, `RUTA_DRAFT`, `LOG_CORRECCIONES`, `VALORACION` deben estar disponibles en toda la sesión.
- **Formato de fechas:** DD/MM/YYYY para mostrar al redactor, YYYY-MM-DD para el frontmatter del draft, YYYYMMDD para el nombre del archivo.
