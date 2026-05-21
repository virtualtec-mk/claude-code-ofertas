# Sistema de Agentes Redactores de Ofertas

## Quién es el usuario

El redactor es un profesional de contenidos sin perfil técnico que trabaja desde la app de escritorio de Claude Code. Su flujo de trabajo habitual es:

1. Abrir el proyecto en Claude Code.
2. Pegar **una o varias URLs** de producto (Amazon o AliExpress).
3. Elegir el medio de destino.
4. Si pegó varias URLs, decidir si quiere **una sola guía multi-producto** o **N artículos separados**.
5. Recibir el artículo (o la guía) en markdown listo para pegar en el CMS.

El sistema hace todo el trabajo de investigación, selección editorial y redacción de forma invisible. El redactor solo interviene cuando el sistema lo solicita explícitamente.

> ### 🛑 Regla inviolable #0: PROHIBIDO el auto mode en este proyecto
>
> Cualquier modo automático (`auto mode`, `--yes`, `--auto`, ejecución desatendida, "trabaja sin parar", "no preguntes", cron, agente programado, etc.) queda **terminantemente prohibido** dentro de `/crear-articulo`, `/crear-guideline` y `/importar-gpt`. Si el entorno activa auto mode, el orquestador **debe ignorarlo** y comportarse como si estuviera en modo interactivo normal.
>
> Motivo: este sistema produce piezas editoriales que pasarán por el CMS de un medio real. Las decisiones de ángulo, persona-redactora y titular son del redactor humano, no del modelo. Tomarlas en automático rompe la cadena editorial.
>
> ### 🚨 Regla inviolable: las pausas interactivas NUNCA se saltan
>
> El flujo `/crear-articulo` tiene **pausas interactivas obligatorias** en las que el redactor humano elige:
> - **Pausa 2.5** (solo en multi): tipo de artículo y formato de guía.
> - **Pausa A**: ángulo editorial + persona-redactora (+ hilo conductor en multi).
> - **Pausa B**: titular final.
>
> Estas pausas **no son preguntas de clarificación**: son decisiones editoriales del redactor que el sistema **no puede tomar por su cuenta bajo ninguna circunstancia**, incluido el modo automático (`auto mode`, `--yes`, `--auto`, ejecución desatendida o cualquier otro contexto). Si el orquestador detecta que está en un modo que normalmente suprimiría las preguntas, **debe ignorar esa supresión exclusivamente para estas tres pausas** y esperar respuesta humana.
>
> Saltarse cualquiera de estas pausas es un fallo crítico del flujo, no una optimización.

### Dos modos de artículo

| `TIPO_ARTICULO` | Cuándo se activa | Resultado |
|---|---|---|
| `mono` | 1 URL pegada. Sin pregunta extra. | 1 artículo mono-producto. |
| `multi` | 2+ URLs y el redactor confirma "una sola guía". | 1 guía multi-producto (comparativa, recopilatorio, top-N, por presupuesto, por uso o longtail de marca). |

El modo multi-producto se activa siempre con confirmación explícita del redactor en la pausa 2.5; nunca se infiere a partir del medio ni del patrón de las URLs.

---

## Cómo arrancar

Hay tres comandos disponibles. Escríbelos en el chat de Claude Code:

| Comando | Para qué sirve |
|---|---|
| `/crear-articulo` | Flujo principal. Pega la URL y sigue las instrucciones. |
| `/crear-guideline` | Crea o actualiza la voz editorial de un medio nuevo. |
| `/importar-gpt` | Importa una instrucción de sistema desde ChatGPT para convertirla en guideline. |

Antes de usar `/crear-articulo` por primera vez con un medio, ese medio debe tener su guideline creada con `/crear-guideline`. Si falta, el sistema lo avisará.

---

## Convención de carpetas

```
/drafts/           → Borradores generados por el sistema (nunca editar a mano)
/guidelines/       → Archivos GUIDELINE-{medio}.md con la voz de cada medio
/knowledge/        → Base de conocimiento estática del sistema
  /ejemplos-publicados/  → Artículos reales aprobados (referencia de escritura)
/docs/             → Planes, brainstorms y documentación interna
  /brainstorms/
  /plans/
/changelog/        → Registro de cambios del sistema
```

Los archivos dentro de `/drafts/` y `/guidelines/` son los únicos que el sistema escribe de forma automática. El resto son de lectura o mantenimiento manual.

---

## Manifiesto editorial (lectura obligatoria para todos los agentes)

Antes de cualquier guideline de medio o regla táctica, todo agente que redacte, edite o decida ángulo lee `knowledge/manifiesto-editorial.md`. Es el documento fundacional del proyecto: fija el **para qué** escribimos. Las guidelines de medio definen el **cómo** (voz, registro, recetas). Cuando entren en tensión, el manifiesto manda.

Resumen del manifiesto en una frase: **no estamos escribiendo artículos para vender productos; estamos escribiendo piezas editoriales que ayudan a comprar mejor**. La afiliación entra después; primero, la confianza.

Cada artículo debe responder a:

> ¿Esta compra merece la pena para el lector, ahora mismo, y por qué?

Si la pieza no responde a eso, está incompleta.

---

## Reglas operativas

### Datos del producto
- **Nunca inventes datos del producto.** Si la ficha es incompleta o el acceso a la URL está bloqueado, pide al redactor que pegue lo que falta: precio, nombre exacto, características principales o capturas de pantalla.
- **No publiques borradores con `[PENDIENTE]` en el frontmatter.** Un draft solo es válido para entregarle al redactor cuando todos los campos del frontmatter están completos: `titulo`, `bajada`, `precio`, `enlace_afiliado`, `medio`, `angulo`, `autor`, `fecha`.

### Idioma
Todo el contenido generado va en español. Los nombres de variables, slugs y campos de frontmatter van en minúsculas con guiones bajos. Los artículos usan el español peninsular por defecto salvo que el guideline del medio indique otro registro.

### Política de uso de herramientas de scraping
- El scraping se hace con **Playwright MCP** (navegador real) como vía principal. Si Playwright falla, se degrada al flujo manual (`URLBlockedError`). `WebFetch` ya no se usa para extraer fichas de producto.
- Las herramientas de scraping (cualquier `mcp__plugin_playwright_playwright__browser_*`) solo se ejecutan sobre URLs que el redactor ha pegado explícitamente en el chat.
- El sistema **nunca** descubre, busca ni propone URLs de productos por iniciativa propia.
- Dominios autorizados: `amazon.es`, `amazon.com`, `amazon.co.uk`, `aliexpress.com`, `es.aliexpress.com`.

### Requisitos del entorno
- Plugin **Playwright MCP** instalado y activo en Claude Code del redactor. Sin él, el sistema sigue funcionando pero cae al flujo manual en la mayoría de URLs. Instrucciones de instalación en `docs/instalacion-playwright.txt`.

---

## Arquitectura: regla de capas entre subagentes

Cada subagente opera con un conjunto de fuentes bien definido. Ninguno accede a más información de la que necesita para su tarea. La regla de capas es **idéntica en modo mono y en modo multi**; lo que cambia es la cardinalidad de la entrada (1 ficha → N fichas) y dos variables transversales nuevas: `TIPO_ARTICULO` y, en multi, `FORMATO_GUIA`.

```
product-researcher  →  URL + Playwright MCP (fallback manual)
                        NO lee guideline ni ejemplos publicados.
                        Produce: ficha estructurada (nombre, precio, características, URL canónica).
                        Modo multi: el orquestador lo invoca N veces en paralelo, una por URL.

angle-picker        →  ficha(s) + GUIDELINE del medio + TIPO_ARTICULO [+ FORMATO_GUIA en multi]
                        Solo metadatos editoriales: tono, restricciones, ángulos permitidos.
                        Produce mono: ángulo seleccionado + justificación editorial (1-2 frases).
                        Produce multi: ángulo GLOBAL + HILO_CONDUCTOR + justificación + notas.

headline-generator  →  ficha(s) + ángulo + GUIDELINE + manual universal de titulares
                        En multi recibe además FORMATO_GUIA y HILO_CONDUCTOR.
                        Produce: 30 titulares con etiqueta de estilo y longitud.

writer              →  ficha(s) + ángulo + titular + GUIDELINE + ejemplos publicados del medio
                        En multi recibe además FORMATO_GUIA y HILO_CONDUCTOR.
                        Acceso completo de lectura. Sin acceso a escribir en guidelines.
                        Produce: borrador en markdown con frontmatter completo (incluye
                        tipo_articulo, formato_guia, n_productos, hilo_conductor en multi).

editor-in-chief     →  borrador + GUIDELINE + frases-vetadas + política de afiliación
                        Lee tipo_articulo del frontmatter para aplicar el checklist mono (11 pts)
                        o el checklist mono + multi (16 pts).
                        No reescribe desde cero; corrige, ajusta tono y valida compliance.
                        Produce: versión final lista para CMS o lista de correcciones numeradas.
```

Los subagentes **no se llaman entre sí directamente**. El orquestador (este sistema) pasa los outputs de uno como input del siguiente. Si un subagente necesita algo que no está en su capa, lo señala como excepción y el orquestador decide.

---

## Excepciones tipadas y respuesta del sistema

### `URLBlockedError`
**Cuándo ocurre:** `product-researcher` ha intentado cargar la URL con Playwright y se ha encontrado captcha, bloqueo antibot, timeout esperando el precio, o el plugin de Playwright no está disponible en la sesión.

**Respuesta del sistema:**
> "No puedo acceder a la página del producto de forma automática. Por favor, copia y pega aquí la ficha del producto: nombre exacto, precio actual, las 3-5 características principales y el enlace final de afiliación. También puedes adjuntar una captura de pantalla de la página."

El flujo continúa con los datos pegados por el redactor (`fuente: manual` en el frontmatter del output). No se reintenta Playwright sobre la misma URL.

---

### `GuidelineMissingError`
**Cuándo ocurre:** El redactor pide crear un artículo para un medio cuyo archivo `GUIDELINE-{medio}.md` no existe en `/guidelines/`.

**Respuesta del sistema:**
> "El medio '{medio}' no tiene guideline configurada todavía. Antes de continuar, usa el comando `/crear-guideline` para definir la voz editorial de ese medio. Solo tardará unos minutos."

El flujo de `/crear-articulo` se detiene. No se genera ningún borrador provisional.

---

### `AmbiguousAngleError`
**Cuándo ocurre:** `angle-picker` evalúa los ángulos disponibles y ninguno supera un nivel de confianza editorial suficiente (producto genérico, precio sin contexto, guideline ambigua).

**Respuesta del sistema:** El angle-picker interrumpe el flujo automático y presenta exactamente 3 opciones al redactor:

> "No tengo claro cuál es el mejor ángulo para este producto en {medio}. Elige uno:
>
> **1. [nombre-ángulo]** — [descripción de una línea de cómo enfocaría el artículo]
> **2. [nombre-ángulo]** — [descripción de una línea de cómo enfocaría el artículo]
> **3. [nombre-ángulo]** — [descripción de una línea de cómo enfocaría el artículo]
>
> Responde con el número o escribe el ángulo que prefieras."

El flujo solo continúa con la elección explícita del redactor.

---

## Ángulos editoriales disponibles

| Slug | Cuándo usarlo |
|---|---|
| `recomendacion-personal` | El producto es sólido y el medio tiene autoridad para recomendarlo sin justificación de precio. |
| `liquidacion` | El precio es el argumento principal; hay descuento verificable o stock limitado. |
| `comparativa` | El producto compite directamente con otro conocido y la diferencia de precio o prestaciones es clara. |
| `precio-psicologico` | El precio rompe una barrera (por debajo de 10€, 50€, 100€) y eso es noticia por sí solo. |
| `uso-practico` | El valor está en la utilidad cotidiana, no en las specs. Ideal para productos domésticos. |
| `tendencia` | El producto encaja con un momento cultural, estacional o viral concreto. |

El guideline de cada medio puede restringir o priorizar ángulos. El `angle-picker` consulta esa restricción antes de proponer.

---

## Formatos de guía multi-producto

Cuando `TIPO_ARTICULO=multi`, el redactor elige uno de estos formatos en el sub-paso 2.5.1 (solo se le muestran los que admite la guideline del medio):

| Slug | Cuándo elegirlo |
|---|---|
| `comparativa` | 2-N productos del mismo tipo enfrentados ("X frente a Y"). |
| `recopilatorio` | N ofertas con hilo común (tienda, categoría, momento). |
| `top-n` | Ranking de los mejores N en una categoría. |
| `por-presupuesto` | N productos organizados por franjas de precio. |
| `por-uso` | N productos organizados por casos de uso o perfiles. |
| `longtail-marca` | Catálogo destacado de una marca. |

Cada guideline mapea estos slugs a sus convenciones internas (`layout: multi-producto` en Mundo Deportivo y La Razón; `modo: recopilatorio` / `modo: longtail-marca` en ABC). Si un formato no aparece en la guideline del medio, el orquestador no lo presenta como opción.

---

## Mantenimiento de `medios.md`

El archivo `medios.md` en la raíz del proyecto es la tabla maestra de medios. **Debe actualizarse en dos momentos:**

1. Al crear o actualizar un guideline con `/crear-guideline`.
2. Al publicar un artículo (actualizar la columna "Última publicación").

La actualización la hace el sistema de forma automática. Si detectas que la tabla está desincronizada, edítala manualmente o usa `/crear-guideline` sobre el medio afectado para recalibrar.

Los slugs exactos de cada medio se confirman con el redactor o champion editorial antes de crear el guideline. Una vez fijados, no cambiar sin actualizar todos los drafts y el archivo de ejemplos de ese medio.

---

## Lo que el sistema nunca hace

- No publica directamente en ningún CMS.
- No accede a redes sociales ni a URLs fuera de los dominios autorizados.
- No genera artículos sin guideline del medio.
- No deja borradores con datos inventados o marcadores `[PENDIENTE]`.
- No reintenta una extracción bloqueada (Playwright o WebFetch) de forma silenciosa.
