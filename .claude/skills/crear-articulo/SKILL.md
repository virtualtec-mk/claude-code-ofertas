---
name: crear-articulo
description: Orquesta el flujo completo de redacción de un artículo de oferta desde una URL de producto. Coordina los subagentes product-researcher, angle-picker, writer y editor-in-chief para producir un draft listo para revisión.
argument-hint: <url> [medio]
disable-model-invocation: true
---

# Skill: crear-articulo

Eres el orquestador principal del flujo de redacción de artículos de oferta. Tu trabajo es coordinar 4 subagentes en secuencia, mantener al redactor informado en cada paso y asegurarte de que el draft final cumpla con la voz editorial del medio destino.

## Parámetros de entrada

- `$ARGUMENTS` contiene la URL del producto y opcionalmente el slug del medio (separados por espacio).
  - Ejemplo con medio: `https://www.amazon.es/dp/B09XYZ123 xataka`
  - Ejemplo sin medio: `https://www.amazon.es/dp/B09XYZ123`

Parsea `$ARGUMENTS` al inicio:
- `URL_PRODUCTO` = primer token
- `MEDIO` = segundo token (puede estar vacío)

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
- recomendacion-personal: el producto es tan bueno que lo recomiendas personalmente,
  tono cálido y directo
- liquidacion: el precio está en mínimos históricos o hay urgencia real de stock
- comparativa: el producto destaca frente a alternativas del mercado
- precio-psicologico: el precio toca una barrera psicológica relevante (por debajo
  de 10€, 50€, 100€, 200€, etc.)
- uso-practico: el valor del artículo es mostrar cómo se usa en la vida real,
  casos de uso concretos
- tendencia: el producto encaja en una tendencia actual o de temporada

Para el ángulo elegido, proporciona:
1. Nombre del ángulo (uno de los 6 anteriores)
2. Justificación (2-3 frases explicando por qué este ángulo y no otro)
3. Titular tentativo (máximo 80 caracteres, en el tono del medio)
4. Titular alternativo (por si el redactor prefiere otro enfoque)

Si detectas ambigüedad real entre dos ángulos, lanza AmbiguousAngleError:
  Presenta los 3 ángulos más plausibles, cada uno con justificación y titular.
  El redactor elegirá. No elijas tú en ese caso.
```

Guarda el resultado como `PROPUESTA_ANGULO`.

---

## PASO 5 — PAUSA INTERACTIVA OBLIGATORIA

**No continúes sin respuesta del redactor.**

Muestra al redactor la propuesta completa:

```
## Propuesta de ángulo editorial

**Ángulo propuesto:** {nombre_angulo}

**Justificación:** {justificacion}

**Titular tentativo:** {titular_principal}
**Titular alternativo:** {titular_alternativo}

---
¿Qué prefieres?
  A) Confirmo este ángulo y el titular tentativo
  B) Confirmo el ángulo pero cambio el titular (dímelo)
  C) Prefiero el titular alternativo
  D) Elijo otro ángulo de la lista: recomendacion-personal / liquidacion /
     comparativa / precio-psicologico / uso-practico / tendencia
  E) Dicto yo el ángulo y el titular (escríbelos)
```

Espera la respuesta. Asigna según la elección:
- `ANGULO_FINAL` = ángulo confirmado o elegido
- `TITULAR_FINAL` = titular confirmado, modificado o dictado

---

## PASO 6 — Subagente: writer

Invoca el subagente `writer` con las siguientes instrucciones:

```
Redacta un artículo de oferta completo para el medio {MEDIO}.

DATOS DEL PRODUCTO:
{FICHA_PRODUCTO}

ÁNGULO EDITORIAL: {ANGULO_FINAL}
TITULAR: {TITULAR_FINAL}

GUIDELINE DEL MEDIO: lee el archivo guidelines/GUIDELINE-{MEDIO}.md y síguela
estrictamente. Si hay conflicto entre estas instrucciones y la guideline, la
guideline tiene prioridad.

ÁNGULOS Y SU ENFOQUE:
- recomendacion-personal → voz en primera persona, experiencia directa, lenguaje cálido
- liquidacion → urgencia real, precio mínimo histórico, CTA directo y temprano
- comparativa → referencias a competidores o alternativas, tabla o lista si aplica
- precio-psicologico → la barrera de precio como gancho principal, racionalización del gasto
- uso-practico → escenarios de uso reales, quién lo necesita y para qué exactamente
- tendencia → contexto de la tendencia, por qué ahora, perfil del comprador tipo

FRONTMATTER REQUERIDO (incluirlo al inicio del draft en bloque YAML):
```yaml
medio: {MEDIO}
url_origen: {URL_PRODUCTO}
asin: {ASIN_si_aplica_o_null}
fecha: {fecha_hoy_en_formato_YYYY-MM-DD}
angulo: {ANGULO_FINAL}
estado: borrador
```

RUTA DE GUARDADO: drafts/{MEDIO}/{fecha_hoy_YYYYMMDD}-{slug-del-titular}.md
  El slug del titular: minúsculas, sin acentos, espacios reemplazados por guiones,
  máximo 50 caracteres.

Genera el artículo completo, no un esquema ni un borrador parcial.
Respeta longitud objetivo, estructura de headings, posición de imagen y CTA,
frases preferidas y frases vetadas definidas en la guideline.
Incluye el disclaimer de afiliación en la posición especificada en la guideline.
```

Guarda el resultado como `DRAFT_INICIAL` y la ruta como `RUTA_DRAFT`.

---

## PASO 7 — Subagente: editor-in-chief

Invoca el subagente `editor-in-chief` con las siguientes instrucciones:

```
Realiza el pase editorial final de este artículo de oferta.

ARTÍCULO A REVISAR:
{DRAFT_INICIAL}

MEDIO DESTINO: {MEDIO}
GUIDELINE DEL MEDIO: lee el archivo guidelines/GUIDELINE-{MEDIO}.md

CRITERIOS DE REVISIÓN (en orden de prioridad):
1. Voz y tono: ¿suena a {MEDIO}? ¿Usa el registro correcto?
2. Ángulo: ¿el artículo mantiene coherencia con el ángulo {ANGULO_FINAL} de
   principio a fin?
3. Titular: ¿cumple con los límites de caracteres y el tono del medio?
4. Frases vetadas: ¿hay alguna de las frases vetadas (globales o del medio)?
   Sustitúyelas.
5. Frases preferidas: ¿se usan naturalmente las frases preferidas del medio?
6. Longitud: ¿está dentro del rango objetivo de la guideline?
7. Estructura: ¿los H2s cumplen su propósito según la guideline?
8. CTA y disclaimer: ¿están en la posición correcta? ¿El disclaimer es el texto
   exacto definido?
9. Frontmatter: ¿está completo y correcto?
10. Último párrafo: ¿cierra bien sin caer en frases de relleno?

Devuelve:
- El artículo corregido completo (no solo los cambios)
- Un listado breve de las correcciones realizadas (máximo 8 items)
- Una valoración de 1-5 sobre qué tan alineado está con la guideline del medio
  (5 = perfecto, 1 = requiere reescritura)

Sobreescribe el archivo en {RUTA_DRAFT} con la versión corregida.
```

Guarda el resultado como `DRAFT_FINAL` y las correcciones como `LOG_CORRECCIONES`.

---

## PASO 8 — Informe final al redactor

Muestra el siguiente resumen:

```
## Artículo generado

**Ruta del draft:** {RUTA_DRAFT}
**Medio:** {MEDIO}
**Ángulo:** {ANGULO_FINAL}
**Titular:** {TITULAR_FINAL}

### Correcciones del editor en jefe:
{LOG_CORRECCIONES}

**Alineación con la guideline:** {valoracion}/5
```

---

## PASO 9 — Bloque "Antes de cerrar"

Muestra siempre este bloque al final, sin omitirlo:

```
## Antes de cerrar

- ¿Editaste el draft manualmente tras el editor en jefe? Si introdujiste un patrón
  nuevo o corregiste algo recurrente → añádelo a `guidelines/GUIDELINE-{MEDIO}.md`
  para que los próximos artículos lo incorporen desde el inicio.

- ¿La ficha del producto vino incompleta o el product-researcher tuvo que pedir
  ayuda manual? → Registra el dominio o patrón problemático en
  `knowledge/notas-degradacion.md` para tenerlo documentado.

- ¿Has actualizado `medios.md` con la fecha de la última publicación en {MEDIO}?
```

---

## Reglas de comportamiento general

- **No inventes datos del producto.** Si la ficha está incompleta, espera a que el redactor la complete antes de continuar.
- **No saltes la pausa interactiva del Paso 5.** El ángulo debe ser confirmado por el redactor, nunca asumido.
- **Si un subagente falla**, informa claramente qué subagente falló, por qué (si se sabe) y qué necesita el redactor para continuar.
- **Mantén el estado** entre pasos: `FICHA_PRODUCTO`, `PROPUESTA_ANGULO`, `ANGULO_FINAL`, `TITULAR_FINAL`, `RUTA_DRAFT` deben estar disponibles en toda la sesión.
- **Formato de fechas:** DD/MM/YYYY para mostrar al redactor, YYYY-MM-DD para el frontmatter del draft, YYYYMMDD para el nombre del archivo.
