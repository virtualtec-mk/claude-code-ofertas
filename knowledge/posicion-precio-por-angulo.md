# Posición del precio según el ángulo

> **Regla transversal aplicable a todos los medios.** El precio y el descuento son siempre un dato del artículo, pero **dónde aparecen depende del ángulo**. Esta tabla es la fuente canónica; las guidelines de cada medio la citan en lugar de definir su propia regla, para evitar contradicciones entre la "voz del medio" y el "ángulo editorial".

---

## Tabla canónica

| Ángulo | Precio en intro | Precio en primer H2/H3 del cuerpo | Precio en el resto del cuerpo | Precio en el cierre |
|---|---|---|---|---|
| `liquidacion` | **Sí, protagonista.** Es la razón de publicar. | **Sí.** El primer H2 puede llevar el descuento como claim. | Refuerzo natural. | Recordatorio del precio. |
| `precio-psicologico` | **Sí, protagonista.** El precio cruza una barrera. | **Sí.** Patrón "baja a {franja relativa}". | Refuerzo del umbral. | Cierre con el dato del precio. |
| `comparativa` | Mención breve, no protagonista. Lo que importa es el contraste. | **Opcional.** Si el precio diferencia productos, sí. | Comparación de precios entre productos. | Veredicto que incluye precio. |
| `recomendacion-personal` | Mención breve. El argumento es el producto, no el precio. | **No protagonista.** El primer H2 cuenta el producto o la marca. | Integrado donde encaje. | Cierre con precio como dato útil. |
| `uso-practico` | **No protagonista.** La intro habla de la utilidad real, no del descuento. | **No protagonista.** El primer H2 abre por el uso, el escenario o la promesa concreta del producto. | Integrado donde encaje, sin ser eje. | Cierre puede incorporar precio como argumento final. |
| `tendencia` | **No protagonista.** La intro ancla en el momento cultural/estacional. | **No protagonista.** El primer H2 desarrolla el momento. | Integrado cuando el producto se presenta. | Cierre que enlaza tendencia y oferta. |

---

## Qué significa "no protagonista"

En los ángulos marcados como **"no protagonista"** (uso-practico, recomendacion-personal, tendencia), el precio:

- **No puede ser la primera información factual** que recibe el lector en la introducción. La introducción se abre con el escenario, el problema, la utilidad o el momento — no con la rebaja.
- **No puede ser el claim del primer H2/H3 del cuerpo**. El patrón "baja a / tiene un X% / por menos de Y euros" en el primer heading queda reservado para `liquidacion` y `precio-psicologico`.
- **Sí aparece** en el cuerpo, integrado en el flujo cuando suma. Y **sí puede aparecer** en el cierre como argumento de "y encima ahora está rebajado".

Esta regla **manda sobre** cualquier "anclaje fijo" de las guidelines que obligue a meter precio en la intro o en el primer H2. Los anclajes se interpretan flexibles según el ángulo. Cuando una guideline tenga un anclaje que choque con este documento, **prevalece este documento** y se actualiza la guideline.

---

## Posición preferida del precio cuando NO es protagonista

Cuando el ángulo no convierte el precio en eje, el sitio natural del precio depende del tipo de artículo:

- **Mono-producto:** lo más habitual es introducirlo al final del primer H2/H3 (donde se cuenta qué es el producto y por qué importa) o en el segundo H2/H3 (cuando ya se ha establecido la utilidad). El cierre también es válido.
- **Multi-producto / guía:** el precio relativo del lote aparece en la intro (sin ser el gancho) o en el primer bloque de producto. En el cierre, la fórmula "y encima ahora con descuento" funciona bien si la noticia no era el precio.

---

## Fórmulas relativas obligatorias en todos los ángulos

Independientemente del ángulo, **el precio se expresa en formato relativo** en el cuerpo del artículo. Esto es regla universal, no depende del ángulo ni del medio (salvo excepción explícita en la guideline del medio):

- "menos de X euros"
- "por debajo de los Y euros"
- "rebaja del Z%"
- "precio mínimo histórico"
- "precio de saldo"
- "casi un regalo"
- "por una fracción"

Las cifras exactas con céntimos (`48,11 €`) se reservan para el widget de pricebox del CMS. Si la guideline del medio permite la cifra exacta en un punto concreto (típicamente, una vez en la intro de una `oferta-unica` en ABC), se respeta lo que diga la guideline, pero el resto del cuerpo sigue siendo relativo.

---

## Cómo lo aplican los agentes

- **`angle-picker`** señala explícitamente en las notas al writer la **posición del precio** que toca según el ángulo elegido. Una línea es suficiente: *"Precio: no protagonista, integrar en cuerpo o cierre"*.
- **`writer`** comprueba antes de redactar la intro y el primer H2/H3 cuál es la posición que le toca según este documento. Si el ángulo es no-protagonista, no abre la intro ni el primer heading con precio o descuento.
- **`editor-in-chief`** valida la posición del precio como parte del check de coherencia de ángulo. Si en `uso-practico` la intro o el primer H2 abren con precio, se reescribe o se devuelve al writer.

---

## Casos límite

- **Descuento bajo con confianza media o baja.** En cualquier ángulo, un descuento de menos del 15% sobre PVP del fabricante no se trata como noticia: se integra como dato, no se titula con él. Si el ángulo es `liquidacion` o `precio-psicologico`, conviene revaluar si el ángulo es realmente el adecuado.
- **Producto sin precio anterior verificable.** Se omite el "antes/ahora"; se habla en términos absolutos del precio actual ("por menos de X euros") sin inventar referencias.
- **Multi-producto con descuentos dispares.** El claim del primer H2 evita el porcentaje y se mueve a "rango de descuento" o se enfoca en el hilo conductor del lote.
