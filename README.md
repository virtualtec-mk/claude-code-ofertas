# Sistema de Agentes Redactores de Ofertas

Este proyecto te ayuda a escribir artículos de ofertas de Amazon y AliExpress de forma rápida y consistente, adaptados a la voz de cada medio.

No necesitas saber programar para usarlo. Solo necesitas tener Claude Code instalado y este proyecto abierto.

---

## Cómo funciona

Pegas **una o varias URLs** de producto, eliges el medio donde vas a publicar, y el sistema genera el artículo completo en markdown listo para pegar en tu CMS.

Por dentro, cinco agentes trabajan en cadena:

1. **Investigador de producto** — lee la ficha del producto en la URL que pegas. Si pegas varias URLs, las investiga todas en paralelo.
2. **Selector de ángulo** — decide el enfoque editorial más adecuado para ese medio. En guías multi-producto, además propone el hilo conductor que justifica que esos N productos vivan en una sola pieza.
3. **Generador de titulares** — propone 30 titulares variados; tú eliges el que más te guste.
4. **Redactor** — escribe el artículo siguiendo la voz del medio.
5. **Editor jefe** — revisa el tono, los datos y el cumplimiento de las normas de afiliación.

Tú no ves ese proceso. Solo recibes el artículo terminado (o una pregunta si el sistema necesita algo de tu parte).

### Artículo simple o guía multi-producto

- **Pegas 1 URL** → el sistema asume que es un artículo de un solo producto y arranca sin más preguntas.
- **Pegas 2 o más URLs** → el sistema te pregunta antes de arrancar:
  - "¿Quieres una sola guía/comparativa con todos los productos juntos?"
  - "¿O prefieres que te genere N artículos separados, uno por producto?"
  - "¿O sólo quieres uno y descarto el resto?"

Si eliges guía multi-producto, después te preguntará qué tipo de guía quieres (comparativa, recopilatorio, top-N, por presupuesto, por uso o longtail de marca), mostrándote solo los formatos que admite el medio elegido.

---

## Antes de empezar

Cada medio donde publiques necesita una **guideline**: un archivo que define el tono, el formato y las reglas editoriales de ese medio. Si es la primera vez que usas el sistema con un medio, crea primero su guideline.

---

## Los tres comandos disponibles

Escríbelos directamente en el chat de Claude Code:

- **`/crear-articulo`** — El flujo principal. El sistema te guía paso a paso.
- **`/crear-guideline`** — Crea o actualiza la voz editorial de un medio.
- **`/importar-gpt`** — Si ya tienes instrucciones de sistema en ChatGPT, las convierte en guideline automáticamente.

---

## Lo que recibes al final

Un archivo markdown en la carpeta `/drafts/` con:

- Frontmatter completo (título, bajada, precio, enlace, medio, ángulo, fecha).
- Cuerpo del artículo listo para copiar y pegar.
- El disclaimer de afiliación correspondiente al medio.

---

## Preguntas frecuentes

**¿Puedo publicar el borrador directamente?**
Sí, siempre que no tenga ningún `[PENDIENTE]` en el frontmatter. El sistema no entrega borradores incompletos.

**¿Qué hago si la URL no carga?**
El sistema te lo dirá y te pedirá que pegues los datos del producto a mano. No es un error tuyo, es una protección normal de algunas páginas.

**¿Puedo usar el sistema con medios nuevos?**
Sí, pero antes necesitas crear la guideline de ese medio con `/crear-guideline`. El sistema te lo recordará si intentas saltarte ese paso.

**¿Dónde se guardan los artículos generados?**
En la carpeta `/drafts/`. Nunca se publican solos; siempre los revisas tú antes.

---

Para más detalles técnicos sobre cómo funciona el sistema por dentro, consulta el archivo `CLAUDE.md` en la raíz del proyecto.
