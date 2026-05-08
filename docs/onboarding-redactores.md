# Guía de inicio para redactores

Bienvenido al sistema de redacción de artículos de oferta. Esta guía te explica todo lo que necesitas saber para empezar a usarlo sin conocimientos técnicos.

---

## 1. ¿Qué es esto?

Es una herramienta que te ayuda a escribir artículos de oferta para Amazon y AliExpress de forma rápida y consistente. Tú pegas la URL del producto, eliges el enfoque del artículo, y la herramienta genera un borrador en el estilo del medio para el que escribes. El resultado queda guardado como un archivo de texto que puedes revisar y publicar.

No necesitas saber programar. No necesitas entender cómo funciona por dentro. Solo necesitas seguir esta guía.

---

## 2. Antes de empezar

Antes de tu primera sesión, asegúrate de tener:

- **Cuenta de Claude con plan Pro o Teams.** El plan gratuito no es suficiente para esta herramienta.
- **Acceso a la carpeta compartida del proyecto en OneDrive.** Tu responsable te habrá enviado el enlace. Si no lo tienes, pídelo antes de continuar.
- **La aplicación de Claude Code instalada** en tu ordenador. Si no la tienes, pídele a tu responsable que te ayude a instalarla (tarda menos de 5 minutos).

---

## 3. Abrir el proyecto

Cada vez que quieras usar la herramienta, sigue estos pasos:

1. Abre la aplicación de Claude Code en tu ordenador.
2. Selecciona la opción para abrir una carpeta o proyecto existente.
3. Navega hasta la carpeta del proyecto que tienes sincronizada desde OneDrive y selecciónala.
4. La herramienta cargará el proyecto y verás un área de chat donde puedes escribir comandos.

> **Nota:** Las capturas de pantalla detalladas de cada paso se añadirán durante la sesión de onboarding en equipo. Si tienes dudas antes de esa sesión, escribe a tu responsable.

Una vez abierta la carpeta correcta, ya puedes empezar a escribir artículos.

---

## 4. Escribir un artículo de oferta

El comando principal para crear artículos es `/crear-articulo`.

### Paso a paso

**1. Copia la URL del producto.**
Ve a Amazon o AliExpress, busca el producto del que quieres escribir y copia la URL completa de la barra de direcciones de tu navegador.

**2. Escribe el comando en el chat.**
En el área de chat de la herramienta, escribe:

```
/crear-articulo [pega aquí la URL del producto]
```

Por ejemplo:

```
/crear-articulo https://www.amazon.es/dp/B0XXXXXXXXX
```

**3. Qué ocurre a continuación.**
La herramienta comienza a trabajar de forma automática:
- Busca información del producto (nombre, precio, características, valoraciones).
- Analiza qué ángulos editoriales son más interesantes para ese artículo.
- Prepara una lista de posibles enfoques para que tú elijas.

Este proceso tarda entre 30 segundos y 2 minutos dependiendo del producto.

### La pausa del ángulo

En algún momento del proceso, la herramienta se detiene y te pregunta qué ángulo quieres para el artículo. Esto es normal y necesario: es el momento en el que tú pones tu criterio editorial.

Verás algo parecido a esto:

```
He encontrado 3 posibles ángulos para este artículo:

1. Relación calidad-precio: el producto más barato de su categoría con buenas valoraciones.
2. Regalo práctico: ideal para regalar por menos de 30 €.
3. Alternativa al líder del mercado: mismas funciones, mejor precio.

¿Cuál prefieres? Puedes responder con el número, escribir el tuyo propio, o escribir "elige tú" para que seleccione el más adecuado.
```

Tus opciones son:
- **Escribir el número** del ángulo que más te gusta (por ejemplo: `2`).
- **Dictar el tuyo propio** si tienes una idea diferente (por ejemplo: `Quiero enfocarlo como opción para estudiantes con presupuesto ajustado`).
- **Escribir "elige tú"** si no tienes preferencia y quieres que la herramienta decida.

Después de tu respuesta, la herramienta termina de escribir el artículo sola.

### Dónde encontrar el resultado

El artículo generado se guarda automáticamente en la carpeta `drafts/` del proyecto, dentro de una subcarpeta con el nombre del medio para el que está escrito. El nombre del archivo incluye la fecha y el título del producto.

Por ejemplo:
```
drafts/
  xataka/
    2026-05-08-auriculares-sony-wh1000xm5.md
```

Puedes abrir ese archivo con cualquier editor de texto (el Bloc de notas funciona, aunque se lee mejor con una app como Typora o directamente en la web del medio).

---

## 5. Crear la voz de un nuevo medio

Antes de escribir artículos para un medio, la herramienta necesita conocer el estilo de ese medio: su tono, su longitud habitual, si usa frases coloquiales o formales, qué texto de aviso legal pone en los artículos de afiliación, etc. Toda esa información se guarda en lo que llamamos una **guideline**.

El comando para crear una guideline es `/crear-guideline`.

### Cuándo usarlo

Usa `/crear-guideline` cuando:
- Vas a publicar en un medio por primera vez y no existe todavía una guideline para él.
- La herramienta te avisa de que no encuentra la guideline de un medio.

### Qué te va a preguntar

La herramienta te irá haciendo preguntas una a una. No tienes que tenerlas preparadas de antemano; puedes responder con lo que sepas y dejar en blanco lo que no. Las preguntas habituales son:

- ¿Cómo se llama el medio? (el nombre tal como aparece en la web)
- ¿Cuál es el tono general? (informal y cercano, técnico y detallado, aspiracional, directo...)
- ¿Cuántas palabras suelen tener los artículos? (ej. entre 400 y 600 palabras)
- ¿Qué texto exacto usa el medio como aviso de afiliación?
- ¿Hay palabras o expresiones que ese medio nunca usa o siempre usa?
- ¿Tienes algún artículo publicado de ejemplo que puedas pegar o adjuntar?

Si pegas un artículo de ejemplo, la herramienta aprende el estilo directamente de él y necesita hacerte menos preguntas.

### Dónde queda guardado

La guideline se guarda en la carpeta `guidelines/` con el nombre `GUIDELINE-{nombre-del-medio}.md`. También se añade automáticamente una fila en el archivo `medios.md`.

---

## 6. Migrar desde un GPT personalizado

Si antes usabas un GPT personalizado de ChatGPT para escribir artículos y quieres trasladar su configuración a esta herramienta, el comando `/importar-gpt` se encarga de eso.

### Cómo conseguir las instrucciones de tu GPT actual

1. Abre ChatGPT y ve a tu GPT personalizado.
2. Entra en la configuración del GPT (el lápiz o botón de edición).
3. Copia el texto del campo **"Instrucciones"** (a veces llamado "System prompt").
4. Si también tienes texto en el campo **"Comportamiento"** o **"Conocimiento"**, cópialo también.

### Qué pegar en la herramienta

En el chat de la herramienta, escribe:

```
/importar-gpt
```

La herramienta te pedirá que pegues el texto de las instrucciones de tu GPT. Pégalo tal cual, sin modificarlo. La herramienta lo analiza y crea una guideline a partir de esa información, haciéndote preguntas solo cuando falta algo importante.

---

## 7. Preguntas frecuentes

**"La herramienta no pudo acceder a la URL de Amazon."**

Esto pasa a veces porque Amazon bloquea accesos automáticos o porque la oferta ya no está disponible. Prueba lo siguiente:
1. Comprueba que la URL es correcta copiándola de nuevo desde el navegador.
2. Asegúrate de que la oferta sigue activa abriendo la URL tú mismo.
3. Si el problema persiste, puedes copiar manualmente el nombre del producto, el precio y las características principales y pasárselos a la herramienta escribiendo: `/crear-articulo [descripción manual del producto]`.

---

**"No existe la guideline para este medio."**

Significa que nadie ha configurado todavía el estilo de ese medio. Sigue los pasos de la sección 5 de esta guía y crea la guideline con `/crear-guideline` antes de volver a intentarlo.

---

**"El artículo tiene [REVISAR] en algún campo."**

Cuando la herramienta no tiene información suficiente para rellenar un campo (por ejemplo, no pudo leer el precio exacto), lo marca con `[REVISAR]` para que lo completes tú manualmente. Abre el archivo del draft, busca todas las ocurrencias de `[REVISAR]` y sustitúyelas por el dato correcto antes de publicar.

---

## 8. Contacto

Si algo no funciona como esperas o tienes dudas que esta guía no resuelve, escribe a tu responsable editorial. No intentes modificar los archivos de configuración de la herramienta por tu cuenta: un cambio incorrecto puede afectar a todos los redactores del equipo.

Para incidencias urgentes (la herramienta no arranca, no puedes abrir el proyecto), contacta directamente con el administrador del sistema.

---

*Última actualización: 08/05/2026*
