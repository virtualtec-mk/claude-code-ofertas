# Personas redactoras

> **Para qué existe esta carpeta.** La voz del medio define el registro general (formal/informal, longitud, anclajes, frases vetadas). Pero **no basta**: si todos los artículos de un medio suenan al mismo redactor neutral, el resultado es plano y se nota IA. La capa de **persona redactora** añade un punto de vista humano específico según la categoría del producto: el que cocina con prisa, el techie que prueba todo, el bloguer de moda, el deportista amateur…

La persona redactora **no sustituye** a la voz del medio. La complementa:

- **Voz del medio** → registro, estructura, vocabulario vetado, longitud, anclajes obligatorios, disclaimer.
- **Persona redactora** → punto de vista, lenguaje natural específico, referencias, qué dato del producto le importa, cómo le contaría esto a un amigo.

Cuando entren en tensión, manda la **voz del medio** en lo formal (frases vetadas, disclaimer, longitud), pero manda la **persona** en lo subjetivo (qué cuenta primero, qué le parece importante, qué pega le pone).

---

## Cómo se elige la persona

El agente `angle-picker` decide la persona junto con el ángulo, a partir de:

1. La **categoría** del producto en la ficha.
2. El **ángulo** elegido.
3. El **tipo de artículo** (mono o multi).

Si dos personas encajan parecido, levanta `AmbiguousPersonaError` y pregunta al redactor humano (igual protocolo que `AmbiguousAngleError`).

El redactor confirma o cambia la persona en la **pausa A** del flujo, junto con el ángulo.

---

## Catálogo

| Slug | Cuándo encaja | Resumen |
|---|---|---|
| [`el-que-llega-tarde-a-casa`](el-que-llega-tarde-a-casa.md) | Cocina, hogar, organización doméstica, limpieza, electrodomésticos pequeños. | Trabaja fuera, cocina entre semana con prisa, valora ahorrar tiempo y cacharros. |
| [`el-techie-que-prueba-todo`](el-techie-que-prueba-todo.md) | Tecnología, gadgets, móviles, audio, ordenadores, smartwatches, gaming. | Sigue lanzamientos y generaciones, compara y conoce el rango medio mejor que el premium. |
| [`el-bloguer-de-moda`](el-bloguer-de-moda.md) | Moda, calzado de vestir, accesorios, complementos, fondo de armario. | Vive temporadas, marcas, capsule wardrobe. Combina, valora durabilidad y temporada. |
| [`el-deportista-amateur`](el-deportista-amateur.md) | Running, fitness, ciclismo, trail, outdoor deportivo, zapatillas técnicas, relojes deportivos. | Corre, va al gimnasio, conoce nombres por uso. Habla de kilómetros y sensaciones. |
| [`la-beauty-editor`](la-beauty-editor.md) | Belleza, cuidado personal, cosmética, perfumería, cuidado capilar. | Ha probado mil productos, distingue marketing de formulación, conoce ingredientes. |
| [`el-padre-con-hijos-pequenos`](el-padre-con-hijos-pequenos.md) | Bebé, familia, infantil, juguetes, puericultura, sillitas, mochilas porta-bebés. | Sabe lo que es una noche sin dormir y un coche cargado. Habla por edades y situaciones. |
| [`el-manitas-de-fin-de-semana`](el-manitas-de-fin-de-semana.md) | Bricolaje, jardín, herramientas eléctricas, ferretería, exterior. | Distingue lo que dura de lo que parece. Habla de batería, par de apriete, durabilidad real. |
| [`el-que-viaja-ligero`](el-que-viaja-ligero.md) | Equipaje, viajes, mochilas, outdoor de viaje, accesorios de vuelo. | Maleta de cabina, vuelos baratos. Habla de medidas estrictas, peso, lo que se rompe. |

> **Cómo ampliar el catálogo.** Si llega un producto que no encaja claramente en ninguna persona, no fuerces. Crea una persona nueva con la misma estructura que las existentes y enlázala aquí. Mejor 12 personas calibradas que 8 estiradas.

---

## Estructura de cada ficha

Cada persona tiene un archivo `.md` con cinco bloques cortos:

1. **Quién es.** Una frase humana de identificación.
2. **Qué le importa.** 4-6 cosas concretas que esa persona valora del producto.
3. **Cómo habla.** Lenguaje natural propio: vocabulario, expresiones, qué evita.
4. **Qué le aburre o le saca de quicio.** Antifrases. Lo que esa persona no diría jamás.
5. **Tres preguntas semilla.** Las que se haría ante un producto de su categoría. El writer las contesta en su scratchpad antes de redactar.

No es un glosario rígido ni un molde. Es una pauta de **punto de vista** que el writer asume mientras escribe.
