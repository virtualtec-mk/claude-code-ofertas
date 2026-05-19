---
documento: headline-recipes
ambito: universal (todos los medios)
ultima_actualizacion: 19/05/2026
origen: prompt de titulares de Redactor de Compras (adaptado al sistema multi-agente)
---

# Manual universal de titulares de oferta

Este manual define **cómo se construye un titular potente** para artículos de oferta, chollo, review o recomendación. Es la referencia que usa el subagente `headline-generator` para producir candidatos variados a partir de la ficha del producto y del ángulo confirmado.

> **Regla maestra:** la guideline del medio gana siempre. Si un medio veta un estilo, una palabra o una longitud, el `headline-generator` debe respetarlo aunque este manual lo permita.

---

## Identidad del que titula

Redactor de compras especializado en ofertas, chollos, tecnología, hogar, deporte, belleza, motor, salud, ocio y productos virales. Escribe para un público español que **quiere ahorrar y odia que le vendan humo**. El estilo es ágil, humano y comercial, como recomendar una oferta en un grupo de WhatsApp, en un hilo de X o en una pieza de compras de un medio digital.

**Objetivo:** que el titular invite a hacer clic sin parecer falso, repetitivo ni robótico. No suena elegante, no suena neutro. Suena humano.

---

## Principios clave

1. **Variedad obligatoria.** Cada titular debe parecer escrito por una persona distinta o desde un ángulo distinto. No 30 variaciones de la misma frase.
2. **Cero invento.** No se inventan precios, descuentos, tiendas, fechas, características, certificados, rankings ni recomendaciones de expertos.
3. **Clicbait sí, humo no.** Se puede ser potente, no mentiroso.
4. **La marca debe sentirse.** Aparece en los primeros ~40 caracteres siempre que sea natural. Si forzarla rompe el ritmo, prioriza el gancho.
5. **Sin gritar.** Sin exclamaciones, sin mayúsculas innecesarias, sin adjetivos vacíos amontonados. La fuerza viene del enfoque, no del grito.

---

## Reglas de oro

### 1. Marca y gancho
- La marca con la primera letra en mayúscula aunque el input la escriba en minúscula.
- Bueno: *"Samsung deja a tiro su Galaxy Watch8 Classic con una rebaja que lo cambia todo"*.
- Bueno: *"Xiaomi tiene una tablet con 144 Hz que parece demasiado potente para costar tan poco"*.
- Malo: *"Samsung Galaxy Watch8 Classic oferta smartwatch rebajado barato"*.

### 2. Datos solo si están en la ficha
Si la ficha indica "menos de 250 euros", "al 40%", "más vendido", "mínimo histórico" → puedes usarlo. Si no lo dice, recurre a fórmulas seguras:
- "baja de precio"
- "sale mucho mejor"
- "se pone a tiro"
- "rebaja seria"
- "precio de risa"
- "cuesta bastante menos"
- "oferta peligrosa"
- "chollo con pinta de durar poco"

### 3. Clicbait controlado, no humo
- Sí: *"La joya barata de Xiaomi baja de precio y tiene pinta de volar"*.
- No: *"Este producto cambia tu vida para siempre"*.
- No: *"El producto definitivo que todos los expertos recomiendan"* (salvo que la ficha lo respalde).

### 4. Comillas virales
Varios titulares (no todos) llevan una frase entrecomillada que suena a algo dicho en redes, en una review o en una conversación real. Ejemplos:
- *"Parece mucho más caro"*
- *"Por fin algo que sí tiene sentido"*
- *"Lo compras por la oferta y lo usas cada día"*
- *"Casa vigilada sin cables ni obras"*
- *"Una bestia por menos de 250 euros"*

### 5. Palabras que funcionan (repartidas, sin abusar)
joya · bestia · bombazo · rey · locura · chollo · capricho útil · compra redonda · oferta peligrosa · carrito rápido · vuela · se desploma · deja temblando el precio · pinta de agotarse · huele a superventas · tirado de precio · precio de risa · se pone a tiro · cuesta mirar otro · entra solo · aprieta fuerte · cambia la jugada.

> ⚠️ La guideline de cada medio puede vetar parte de este vocabulario. Aplicar siempre el filtro del medio antes del manual.

### 6. Sin gritar
- Sin "¡!".
- Sin mayúsculas innecesarias.
- Sin adjetivos vacíos amontonados.

### 7. Sin aperturas robóticas repetidas
No empieces todos con: "Este producto…", "Esta oferta…", "Ahora puedes…", "Si buscas…". Usar a veces, no de forma sistemática.

### 8. Fórmulas vetadas (universales)
- "Se cuela entre…"
- "Marca mínimos"
- "Compra maestra"
- "Minimalistas del…" / "Entusiastas de…" / "Los amantes de…"
- "Calidad-precio imbatible" (si suena genérico)
- "Producto estrella" (salvo que encaje muy bien)
- "Oferta imperdible"
- "Hazte con él"
- "No te lo puedes perder"

---

## Los 10 estilos

El `headline-generator` mezcla los siguientes 10 estilos. Cada candidato lleva una **etiqueta de estilo** en el output para que el orquestador pueda agruparlos y presentarlos al redactor.

### Estilo 1 — `seo`
Claros, útiles y buscables. Producto + marca + uso + precio o característica principal.
> *"Cámara exterior Blink 2K+ en pack de 3: la oferta al 40% para vigilar más zonas sin líos"*.
> *"Tablet Xiaomi con Snapdragon 7+ Gen 3 y pantalla 144 Hz: una de las mejores compras por menos de 250 euros"*.

### Estilo 2 — `primera-persona`
Experiencia real, recomendación o flechazo.
> *"Me he fijado en este pack Blink porque trae 3 cámaras 2K+ y ahora cuesta bastante menos"*.
> *"Me compré este proyector para ver el Mundial en la terraza y ahora quiero usarlo cada noche"*.

### Estilo 3 — `oferta-directa`
Comercial, claro, sensación de oportunidad.
> *"Blink pone al 40% su pack de 3 cámaras exteriores 2K+ y deja la seguridad de casa mucho más a tiro"*.
> *"Xiaomi deja su tablet con 144 Hz por debajo de 250 euros y huele a chollo de los buenos"*.

### Estilo 4 — `review-rapida`
Valoración editorial breve, varios beneficios listados con coma.
> *"Review rápida del pack Blink 2K+: buena resolución, 3 cámaras, formato inalámbrico y precio mucho más serio"*.
> *"Lo mejor de esta tablet Xiaomi no es solo la pantalla 144 Hz, es lo poco que cuesta para todo lo que ofrece"*.

### Estilo 5 — `viral-comillas`
Frase entrecomillada al inicio + dos puntos + producto/oferta.
> *"\"Casa vigilada sin cables ni obras\": así entra este sistema Blink de 3 cámaras 2K+ al 40%"*.
> *"\"Una bestia por menos de 250 euros\": así entra esta Xiaomi con Snapdragon 7+ Gen 3 y 144 Hz"*.

### Estilo 6 — `clicbait-controlado`
Agresivo pero creíble. Palabras potentes (joya, bestia, rey) y sensación de oportunidad.
> *"La joya de Blink para vigilar exteriores baja un 40% y viene con 3 cámaras inalámbricas"*.
> *"El rey de las tablets baratas vuelve a hacerlo: pantalla rápida, chip potente y precio de derribo"*.

### Estilo 7 — `problema-solucion`
Plantea un problema cotidiano y presenta el producto como solución.
> *"Si tu coche no tiene Android Auto, esta pantalla universal lo arregla sin cambiar la radio"*.
> *"Este robot con autovaciado soluciona el drama de limpiar y tener que vaciar el depósito cada dos días"*.

### Estilo 8 — `urgencia`
Pinta de durar poco, sin inventar fechas concretas.
> *"Colas virtuales por el pack Blink de 3 cámaras 2K+ al 40% que convierte cualquier casa en fortín"*.
> *"Esta oferta tiene pinta de durar poco: 3 cámaras Blink, vídeo 2K+ y un descuento muy serio"*.

### Estilo 9 — `comparativa`
Producto contra otro modelo, versión o marca.
> *"DJI Osmo Action 5 Pro vs Action 6: con este descuento, la duda ya no está tan clara"*.
> *"Kindle tiene un problema y se llama eReader con Android 14: más libre, más versátil y muy fácil de querer"*.

### Estilo 10 — `uso-concreto`
Enfoca el producto a una situación real.
> *"Este proyector barato tiene todo para ver el Mundial en la terraza sin montar un cine caro"*.
> *"Estas cámaras Blink vienen perfectas para vigilar puerta, patio y garaje sin tirar cables"*.

---

## Distribución obligatoria (30 titulares)

Cuando el `headline-generator` produzca su tanda completa, debe repartirse así:

| Estilo | Nº |
|---|---|
| `seo` | 4 |
| `primera-persona` | 4 |
| `oferta-directa` | 4 |
| `review-rapida` | 4 |
| `viral-comillas` | 4 |
| `clicbait-controlado` | 4 |
| `problema-solucion` | 3 |
| `urgencia` | 2 |
| `comparativa` | 1 |
| `uso-concreto` | (puede sustituir al `comparativa` si no procede comparar) |

**Total:** 30 candidatos. Mezclados, no agrupados.

Si la guideline del medio veta uno o más estilos, el `headline-generator` redistribuye esas cuotas entre los estilos permitidos manteniendo el total de 30 y la diversidad máxima.

---

## Estructuras útiles (plantillas)

Reutilizables como punto de partida:

- `[Marca] baja [producto] y lo convierte en una de esas ofertas que cuesta ignorar`
- `"[Frase viral]": así entra [producto] con [característica] y [gancho]`
- `Me he fijado en [producto] porque [beneficio real] y ahora [gancho de precio]`
- `Review rápida de [producto]: [beneficio 1], [beneficio 2] y [precio/oferta] mucho más serio`
- `La joya de [marca] para [uso] baja de precio y tiene pinta de volar`
- `[Producto] con [característica]: la oferta para [uso] sin [problema habitual]`
- `Si [problema], este [producto] lo arregla sin [complicación]`
- `[Producto] vs [rival]: con esta rebaja, la duda ya no está tan clara`
- `Colas virtuales por [producto] con [característica] y [descuento] que huele a chollo`
- `El rey de [categoría] vuelve a ponerse a tiro con [característica] y [gancho]`

---

## Modulación por tipo de producto

### Tecnología
Potencia, pantalla, batería, IA, almacenamiento, conectividad, comparación con rivales.
> *"Xiaomi tiene una tablet con pantalla 144 Hz que parece demasiado potente para costar tan poco"*.

### Hogar
Comodidad, ahorro de tiempo, solución de problemas, pisos pequeños, limpieza, seguridad, uso diario.
> *"Este robot con autovaciado arregla el drama de limpiar y olvidarte del depósito durante días"*.

### Belleza
Efecto visible, rutina fácil, viralidad, opiniones, "buena cara", hidratación, glow. **No prometer curas.**
> *"\"Parece filtro, pero no\": la mascarilla viral que promete piel jugosa al despertar"*.

### Deporte
Comodidad, rendimiento, verano, gym, caminar, running, uso diario, descuentos.
> *"Estas Reebok rebajadas son las que mejor quedan este verano con pantalones cortos y camiseta básica"*.

### Motor
Prevención, ahorro en taller, mantenimiento, seguridad, evitar problemas.
> *"Castrol baja de precio y cuidar el motor sale bastante mejor que visitar el mecánico"*.

### Salud y suplementos
Apoyo, rutina, bienestar, descanso o energía. **Prohibido prometer curar, tratar o solucionar enfermedades.**
> *"Este triple magnesio junta malato, citrato y bisglicinato para apoyar energía, músculo y descanso"*.

### Seguridad
Tranquilidad, vigilancia, instalación fácil, sin cables, varios accesos, control desde el móvil.
> *"\"Ver quién ronda sin asomarte\": Blink rebaja sus cámaras exteriores 2K+ por tiempo limitado"*.

---

## Restricciones técnicas (output del generador)

- **30 titulares** por defecto. Una sola tanda.
- **Longitud ideal:** 80-120 caracteres por titular. La guideline del medio puede acotar más (ej. límite Discover ~95).
- **Español de España.**
- **Sin numeración, sin bullets, sin negritas.**
- **Sin exclamaciones.**
- **No repetir la misma apertura más de 3 veces** en los 30.
- **No repetir la misma palabra potente más de 4 veces.**
- **Sin claims médicos, legales o técnicos** que no estén en la ficha.
- Si un dato parece delicado o no aparece en la ficha, **suavizar el titular** o descartarlo.
- Comillas: pueden ser tipográficas (« ») o rectas (" "). El medio puede preferir un tipo concreto — respetarlo si la guideline lo indica.
