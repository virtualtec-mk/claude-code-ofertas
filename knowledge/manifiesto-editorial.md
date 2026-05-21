# Manifiesto editorial — afiliación útil

> **Cómo se usa este archivo:** Es el **documento fundacional** del proyecto. Está por encima de las reglas tácticas (naming, frases vetadas, recetas de cada medio). El `writer` y el `editor-in-chief` lo leen en cada artículo, **antes** que cualquier otra guía. La guideline de cada medio adapta el cómo; este manifiesto fija el **para qué**.

---

## 1. Para qué escribimos estos artículos

El objetivo de un artículo de afiliación en este proyecto **no es** llenar una página con productos y enlaces. **No es** acompañar una ficha de Amazon con texto suficiente para indexar. **No es** generar volumen.

El objetivo es **ayudar al lector a decidir qué comprar, cuándo comprarlo y si realmente merece la pena**.

Da igual el formato:

- Oferta flash de un solo producto.
- Recopilatorio de marca.
- Recopilatorio de categoría.
- Guía de compra.
- Review individual.
- Comparativa cara a cara.

Todos deben aportar **más valor que una ficha de producto, que un marketplace o que una lista automática de ofertas**. Si lo que escribimos puede sustituirse por una captura de pantalla de Amazon, el artículo no debería existir.

> **Contexto de mercado:** Google está reforzando la importancia del contenido útil, original, bien estructurado y pensado para personas, también en sus experiencias de búsqueda con IA generativa. El contenido de afiliación debe evitar parecer genérico o producido en masa. Las piezas que sobrevivirán en SGE/AI Overviews son las que aportan criterio, no las que repiten ficha.

---

## 2. La pregunta principal que debe responder cada artículo

Antes de empezar a escribir, el writer (y antes de cerrar, el editor-in-chief) se hace esta pregunta:

> **¿Esta compra merece la pena para el lector, ahora mismo, y por qué?**

Si el artículo no responde bien a esa pregunta, está incompleto.

---

## 2.bis. El test del bloguero

Por encima de cualquier checklist táctico, anclajes obligatorios o recetas de la guideline, **todo artículo debe pasar este test antes de publicarse**:

> **Lee el artículo en voz alta. ¿Suena a alguien que sabe de la categoría recomendando algo a un amigo en una sobremesa?**
>
> Si suena a "estructura + recetas + checklist + IA bien disimulada", está mal escrito aunque cumpla la guideline.

Este test es el **filtro número uno** del editor-in-chief. Si no lo pasa, el draft vuelve al writer; no se pule un texto que no suena a humano experto. Se reescribe.

Síntomas habituales de no pasarlo:

- Suena al mismo redactor neutro para cocina, tech, moda y running.
- El primer párrafo arranca con datos transaccionales (precio + tienda + descuento) antes de tener voz.
- Las secciones del cuerpo se reconocen como "receta IA encadenada" (mini-historia → para quién sí/no → FAQ).
- Frases comodín que servirían para cualquier producto de la categoría.
- Ausencia total de juicio editorial subjetivo del que escribe.

Pasar el test exige las dos capas que se describen en el punto siguiente: **voz del medio + persona-redactora**.

---

## 2.ter. Voz del medio + persona-redactora: dos capas que se combinan

Cada artículo se redacta desde **dos capas** que conviven y se complementan:

1. **Voz del medio.** Definida en `guidelines/GUIDELINE-{medio}.md`. Fija el registro general (formal/informal), la longitud, los anclajes mínimos, las frases vetadas y preferidas, el disclaimer, las posiciones de imagen y CTA.
2. **Persona-redactora.** Definida en `knowledge/personas-redactoras/`. Fija el punto de vista humano según la categoría del producto: el que cocina con prisa, el techie que prueba todo, el bloguer de moda, el deportista amateur, la beauty editor, el padre con hijos pequeños, el manitas, el que viaja ligero, etc.

Reparto de mando entre las dos capas:

- **Manda la voz del medio en lo formal:** frases vetadas, disclaimer literal, longitud objetivo, anclajes obligatorios, formato del frontmatter, formato de precio.
- **Manda la persona-redactora en lo subjetivo:** qué cuenta primero, qué dato del producto le importa, en qué escenario aterriza, qué pega real le pone, con qué vocabulario natural habla.

Si la guideline del medio no contradice nada concreto sobre el punto de vista, la persona-redactora **es la que decide cómo se cuenta el producto**. La voz del medio es el registro general; la persona-redactora es el redactor humano específico que firma esa pieza.

El `angle-picker` propone la persona-redactora junto con el ángulo. El redactor humano la confirma o la cambia en la **pausa A** del flujo. El `writer` la recibe como input y la asume durante la redacción. El `editor-in-chief` valida su coherencia como parte del test del bloguero.

Las personas-redactoras viven en `knowledge/personas-redactoras/` (un archivo por persona, más un README con el catálogo). El catálogo es ampliable: si un producto no encaja en ninguna persona, se crea una nueva con la misma estructura.

---

## 2.quater. Posición del precio según el ángulo

El precio no siempre va en la introducción. Va donde el ángulo manda. La regla canónica vive en `knowledge/posicion-precio-por-angulo.md` y aplica a **todos los medios**:

- En `liquidacion` y `precio-psicologico` (y a menudo en `comparativa`), el precio es protagonista de la intro y del primer H2.
- En `uso-practico`, `recomendacion-personal` y `tendencia`, **el precio no es protagonista**: la intro abre por el escenario, la utilidad o el momento; el primer H2 abre por el producto o por el contexto; el precio entra integrado en el cuerpo o en el cierre como argumento secundario.

Esta regla manda sobre cualquier anclaje de guideline que obligue a meter precio en la intro o en el primer H2. Si la guideline de un medio tiene un anclaje que choca con esta regla, prevalece esta regla y se actualiza la guideline.

---

## 2.quinque. Persuasión equilibrada: vender sin mentir, no sabotear sin querer

Estos artículos son **piezas de afiliación**. El objetivo es ayudar a comprar mejor — **no demostrar imparcialidad académica**. La honestidad de los puntos 4, 5 y 6 de este manifiesto está al servicio de la confianza del lector, no de la transparencia exhaustiva. Hay una línea fina entre "advierto con honestidad" y "saboteo la venta sin querer":

- **Honestidad útil** = matizar un punto débil concreto con una frase integrada en el cuerpo, sin alarmismo y sin convertirlo en sección estrella.
- **Sabotaje involuntario** = abrir un H2 entero a dudas que el lector no se estaba planteando, o blindar el artículo con tantas reservas que la conclusión razonable sea "mejor no compres".

### Reglas prácticas

1. **Las pegas viven integradas, no en H2 propios.** Un "para quién no es" puede aparecer como 1-2 frases dentro de un H2 sobre el uso o el cierre. **No** se monta un H2 dedicado a desincentivar la compra salvo que el ángulo sea explícitamente una review crítica o `recomendacion-personal` larga donde el lector espera ese contraste.
2. **Prohibido el H2 "lo que no sé / lo que me preocupa de [marca o producto]".** Si la marca es poco conocida, esa información se trabaja como **dato de contexto neutro o positivo** ("marca menos conocida que llega con 4,8/5 y reseñas verificadas"), no como un H2 que siembra dudas. El lector no entró al artículo para que le digamos que tenemos sospechas; entró para saber si esa compra concreta le encaja.
3. **Calibrar el peso narrativo.** Si el artículo dedica más espacio a advertir que a explicar para qué sirve y por qué encaja ahora, está mal calibrado. Como referencia: las pegas no deberían superar el 15-20% del cuerpo en una oferta. En una review crítica, hasta un 30%.
4. **Las alternativas no compiten contra el producto.** Mencionar una alternativa es legítimo (Kärcher, Adidas, etc.) cuando el lector la conoce y le ayuda a ubicarse, pero la alternativa se presenta como **mapa de mercado**, no como "si pudieras, comprarías la otra". El protagonista del artículo es el producto que estamos recomendando.
5. **El cierre no se disculpa.** Un último párrafo del tipo *"si esto no te convence, mira otra cosa"* descarga el artículo de su función. El cierre confirma para quién encaja y por qué tiene sentido ahora, con la honestidad ya repartida en el cuerpo.

### Estructura: variedad obligatoria en los H2 del cuerpo

Los H2 del cuerpo **no pueden repetir plantilla artículo a artículo**. En particular, evitar como reflejo automático:

- "Para qué sí / Para qué no" (o variantes: "Para quién es / Para quién no", "Pros y contras", "Lo bueno y lo malo").
- "Lo que [marca] hace bien / Lo que [marca] no me convence".
- "Antes de comprar, ten en cuenta…" como cajón de pegas.

Esas plantillas pueden aparecer **ocasionalmente** cuando encajan con el producto, pero el writer y el editor-in-chief vigilan que no se conviertan en la forma por defecto de cerrar el cuerpo. El criterio del manitas, el techie, el bloguer o cualquier persona-redactora se nota en que **cada artículo organiza sus H2 de forma distinta**, según lo que pida ese producto en concreto, no según un molde.

> **Regla del espejo:** si el último artículo del medio acabó con un H2 tipo "para qué sí / para qué no" o "para quién es / para quién no", el siguiente NO repite ese patrón. El editor-in-chief comprueba el último draft publicado del medio y rechaza la duplicación de molde.

No basta con decir que algo está rebajado. Hay que explicar, en algún punto del artículo:

- Por qué es buena oferta.
- Para quién tiene sentido.
- Para quién no.
- Qué alternativas existen si se agota o no encaja.
- Qué pega tiene.
- Si el precio realmente compensa.
- Qué debe hacer el lector si se agota o sube de precio.

No todas estas piezas tienen que aparecer literales como secciones; el writer las integra según el formato y la voz del medio. Pero **el criterio detrás tiene que estar**.

---

## 3. No escribimos fichas de producto

Evitamos textos que suenen a descripción copiada de Amazon, Zalando, Miravia, MediaMarkt, El Corte Inglés o la web del fabricante.

❌ Mal — esto es ficha de producto reescrita:
> "Este producto destaca por su diseño moderno, gran calidad y excelente relación calidad-precio."

✅ Bien — esto es criterio editorial:
> "Merece la pena si buscas unas zapatillas cómodas para diario y las encuentras por debajo de 80€. No las elegiríamos para running serio, pero sí como sneaker versátil para combinar con vaqueros, pantalones cargo o looks casuales."

La diferencia está en el **criterio editorial**: en una se enumera, en la otra se recomienda.

---

## 4. Contexto mínimo por cada recomendación

Cada producto incluido en un artículo debería responder, como mínimo, a esto (no como sección obligatoria, sino como criterio que el writer tiene **internalizado** y vuelca de forma natural en el texto):

- **Qué es** — categoría, época, herencia, qué resuelve.
- **Por qué lo seleccionamos** — qué lo distingue del resto.
- **Para quién es buena compra** — perfil concreto, uso real.
- **Para quién no** — la honestidad invertida.
- **Cuál es su principal ventaja** — la razón fuerte.
- **Cuál es su principal pega** — el "pero" honesto.
- **A qué precio empieza a compensar** — la franja en la que tiene sentido.
- **Qué alternativa miraríamos si se agota** — la red de seguridad.

Una buena recomendación **no vende por vender. Orienta.**

---

## 5. Honestidad con las pegas

Todos los productos tienen algún "pero". Si el artículo solo dice cosas buenas, **pierde credibilidad**.

Cada pieza debe incluir advertencias útiles, calibradas al producto. Ejemplos del tipo de honestidad que buscamos:

- "Ocupa bastante espacio."
- "No es la mejor opción para uso intensivo."
- "El descuento solo compensa si encuentras tu talla."
- "Hay alternativas más baratas si no necesitas esta función."
- "No pagaría el precio completo por este modelo."
- "Buena compra por debajo de X €, menos interesante si sube."

> **Principio:** la honestidad **no reduce la conversión, la mejora**. Genera confianza. El lector que descubre que advertimos honestamente sobre las pegas vuelve.

> **Importante (ver 2.quinque):** la honestidad va **integrada**, no en H2 dedicados a la duda. Una pega es 1-2 frases dentro de una sección más amplia. Si la pega ocupa una sección entera con su propio título, el artículo deja de ser una recomendación y pasa a ser una advertencia; eso solo encaja en reviews críticas explícitas, no en oferta ni en `uso-practico`.

---

## 6. Descuento ≠ buena compra

Un producto puede tener un 40% de descuento y aun así **no ser una buena compra**.

Antes de escribir "ofertón" o equivalente, el writer comprueba (o internaliza, si los datos están disponibles):

- Precio actual vs. precio habitual.
- Precio mínimo reciente (los últimos 30/90 días).
- Si suele bajar más en campañas (Black Friday, Prime Day, rebajas).
- Si el descuento es real o inflado sobre un PVP exagerado.
- Si hay alternativas mejores al mismo precio.

Si no se puede justificar que es buena compra, **no se escribe que lo es**.

---

## 7. Cómo redactar según el tipo de artículo

Cada formato tiene su lógica. La voz del medio matiza el cómo; la lógica del formato no se discute.

### A. Oferta flash de un solo producto

Estos artículos solo se hacen cuando el producto tiene suficiente interés: marca fuerte, búsquedas activas, buen descuento verificable, posibilidad real de conversión o valor editorial diferenciado.

Estructura recomendada (adaptable al medio):

1. Qué producto está en oferta.
2. Precio actual y precio habitual, si se conoce.
3. Por qué la oferta merece atención.
4. Para quién sí lo recomendamos.
5. Para quién no.
6. Principales ventajas.
7. Principales pegas.
8. Alternativas si se agota.
9. Veredicto final.

Ejemplo de enfoque (titular):
> "Estas New Balance 530 están rebajadas: cuándo merece la pena comprarlas y para quién las recomendamos."

> **No hacer:** artículos individuales para cualquier producto con un descuento pequeño o sin demanda. Es mejor incluirlos en un recopilatorio.

### B. Recopilatorios de ofertas por marca

No es una simple lista de productos de una marca. El artículo debe explicar:

- Qué productos de esa marca suelen merecer la pena.
- Qué descuentos son buenos para esa marca.
- Qué modelos priorizar.
- Qué productos evitar aunque estén rebajados.
- En qué casos conviene elegir otra marca.
- Qué alternativas hay si no encontramos buena oferta.

Ejemplo:
> "Mejores ofertas de Adidas: zapatillas, ropa y accesorios que sí merece la pena comprar rebajados."

Organizar por **intención**, no por orden de aparición en la ficha:

- Mejor oferta calidad/precio.
- Mejor opción barata.
- Mejor opción premium.
- Mejor para uso diario.
- Mejor para regalar.
- Mejor alternativa si se agota.

### C. Recopilatorios por categoría

En categorías amplias (moda, zapatillas, hogar, tecnología, belleza), la clave es **ordenar la oferta para que el lector pueda decidir rápido**.

No listado plano. **Segmentación por necesidad**.

Ejemplo:
> "Mejores ofertas de zapatillas: modelos que merecen la pena según uso, precio y estilo."

Incluir tabla inicial cuando ayude a escanear:

| Producto | Mejor para | Punto fuerte | Cuidado con |
|---|---|---|---|
| Zapatillas X | Uso diario | Cómodas y versátiles | No son para running técnico |
| Freidora Y | Familias | Buena capacidad | Ocupa bastante |
| Abrigo Z | Fondo de armario | Fácil de combinar | Pocas tallas disponibles |

> **La columna "Cuidado con" es imprescindible.** Aporta confianza y diferencia el contenido del resto del mercado.

### D. Guías de compra

Una guía de compra debe funcionar como un **asesor**, no como un escaparate.

Debe ayudar al lector a elegir según: presupuesto, uso, nivel de exigencia, espacio disponible, talla, materiales, durabilidad, comodidad, alternativas.

Estructura recomendada:

1. Recomendación rápida por perfil.
2. Tabla comparativa.
3. Cómo hemos elegido los productos.
4. Análisis de cada modelo.
5. Qué tener en cuenta antes de comprar.
6. Errores comunes.
7. Cuándo merece la pena pagar más.
8. Cuándo conviene ahorrar.
9. Veredicto final.

Ejemplo:
> "Mejores freidoras de aire: cuál comprar según capacidad, presupuesto y tipo de cocina."

### E. Reviews

**No fingir experiencia directa si no la hay.**

- Si se ha probado el producto, contarlo con detalle.
- Si no se ha probado, ser transparente:
  > "No hemos probado este producto directamente, pero hemos analizado sus especificaciones, precio, disponibilidad, opiniones de compradores y alternativas similares para valorar cuándo puede merecer la pena."

Una review debe incluir: para qué sirve, para quién está pensado, qué promete, qué puntos fuertes tiene, qué limitaciones presenta, cómo se compara con alternativas, a qué precio compensa, veredicto final.

### F. Comparativas

Una comparativa **no se limita a enfrentar fichas técnicas**.

Debe responder: cuál compraría en cada caso, qué diferencia realmente importa, cuándo compensa pagar más, qué opción es mejor para cada perfil, qué producto evitaría según el uso.

Frases-tipo que ordenan el criterio:

- "Compraría el modelo A si…"
- "Elegiría el modelo B si…"
- "No pagaría más por este modelo salvo que…"
- "La diferencia de precio solo compensa si…"

---

## 8. Criterios específicos por categoría

El writer adapta el peso de cada criterio al tipo de producto.

### Moda

Valora: versatilidad, facilidad de combinar, tallaje, materiales, temporada, colores, si es fondo de armario o tendencia pasajera, disponibilidad real de tallas, si el descuento compensa.

Pregunta clave: **¿Es una prenda que el lector va a aprovechar de verdad?**

### Zapatillas

Valora: comodidad, uso recomendado, amortiguación, materiales, suela, tallaje, colores, si sirven para vestir, caminar, correr o entrenar, precio habitual, alternativas similares.

Pregunta clave: **¿Son buenas para el uso que el lector tiene en mente o solo son bonitas/rebajadas?**

### Hogar

Valora: utilidad real, tamaño, consumo, ruido, facilidad de limpieza, mantenimiento, durabilidad, garantía, espacio que ocupa, si resuelve un problema concreto.

Pregunta clave: **¿Es un producto útil a diario o un capricho que acabará en un armario?**

### Tecnología

Valora: rendimiento, autonomía, pantalla, compatibilidad, actualizaciones, memoria, conectividad, vida útil, limitaciones frente a modelos superiores.

Pregunta clave: **¿Será suficiente para el usuario dentro de uno o dos años?**

### Belleza y cuidado personal

Valora: tipo de piel o pelo, frecuencia de uso, ingredientes o tecnología, formato, precio por uso, resultados esperables, limitaciones, posibles sensibilidades.

Pregunta clave: **¿Para quién puede funcionar y para quién no sería la mejor opción?**

---

## 9. SEO al servicio de la utilidad

El SEO está al servicio del lector, no al revés.

Cada artículo debe tener:

- H1 claro.
- Entradilla útil y directa.
- Subtítulos descriptivos (los H2 cuentan la historia, no son etiquetas SEO).
- Tabla inicial cuando ayude a decidir.
- Enlaces internos relevantes (clusterización).
- FAQs útiles, no de relleno.
- Veredicto final.
- Fecha de actualización visible en artículos de ofertas.
- Estructura fácil de escanear.

Evitar:

- Intros largas.
- Repetir keywords de forma artificial.
- Crear muchas URLs casi iguales.
- Publicar artículos de ofertas que caducan y luego abandonarlos.
- Copiar textos de tiendas.
- Meter productos sin explicación.

---

## 10. Ciclo de vida de un artículo de oferta

No queremos que la web se convierta en un **cementerio de ofertas muertas**.

Cuando una oferta termina, decidimos uno de estos cuatro caminos:

- **Reactivar:** si el producto vuelve a rebajarse a menudo, actualizar la misma URL.
- **Evergreenizar:** si tiene demanda estable, convertirla en guía evergreen.
- **Integrar:** si no merece URL propia, integrarla en un recopilatorio.
- **Despublicar:** si ya no aporta nada, valorar redirección, noindex o eliminación.

Este paso no lo ejecuta el sistema automáticamente; queda como **decisión editorial** del redactor humano. El sistema sí debe ayudarle a tomarla (por ejemplo, al actualizar un artículo, sugerir cuál de las cuatro vías encaja).

---

## 11. Checklist final antes de entregar

Antes de cerrar el artículo, el editor-in-chief revisa estas 13 preguntas en orden. Si alguna respuesta es "no", reescribir el bloque correspondiente.

**Test del bloguero (filtro previo, obligatorio):**

0a. ¿El artículo suena a un humano experto en la categoría hablándole a un amigo? ¿O suena a IA bien disimulada con plantilla?
0b. ¿La persona-redactora declarada en el frontmatter se reconoce en el texto? ¿Habla como esa persona, con su punto de vista y su lenguaje natural?

Si 0a o 0b fallan, el draft vuelve al writer. No se pula un texto que no suena humano: se reescribe.

**Checklist principal:**

1. ¿El artículo ayuda realmente a decidir?
2. ¿Tiene criterio propio?
3. ¿Incluye pros y contras?
4. ¿Explica para quién sí y para quién no, en cada producto?
5. ¿Diferencia descuento de buena compra?
6. ¿Incluye alternativas si el producto se agota o sube de precio?
7. ¿Evita frases vacías tipo "oferta irresistible"?
8. ¿No parece una ficha de producto reescrita?
9. ¿Está bien estructurado y se puede escanear?
10. ¿Puede integrarse en un clúster de contenidos del medio?
11. ¿Sigue siendo útil aunque el lector no compre en ese momento?
12. ¿La posición del precio respeta la regla del ángulo? (Ver `knowledge/posicion-precio-por-angulo.md`. En `uso-practico`, `recomendacion-personal` y `tendencia` el precio NO abre intro ni primer H2.)
13. ¿La voz del medio y la persona-redactora conviven sin atropellarse? (El medio impone el registro y las frases vetadas; la persona aporta el punto de vista. Si una de las dos capas se ha tragado a la otra, recalibrar.)
14. ¿La persuasión está equilibrada (regla 2.quinque)? ¿Las pegas viven integradas en el cuerpo y no como H2 dedicados? ¿No hay ningún H2 cuyo título siembre dudas sobre la marca o el producto? ¿La estructura de H2 NO repite la plantilla del último artículo publicado del medio?

---

## 12. Idea final

> **No estamos escribiendo "artículos para vender productos". Estamos escribiendo piezas editoriales que ayudan a comprar mejor.**
>
> La afiliación entra después. Primero va la confianza.
