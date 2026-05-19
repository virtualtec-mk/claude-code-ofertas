---
medio: abc
version: 1.1
ultima_actualizacion: 19/05/2026
origen: importado desde GPT personalizado "ABC Favorito" (v1.0) + calibración con 18 ejemplos publicados (v1.1)
autores:
  - nombre: Benjamín Pelaz
    perfil: declarado como autor por defecto por el redactor. En la muestra descargada de 18 artículos de mayo 2026 no aparece firmando ninguno — verificar si está cubierto temporalmente por otras firmas.
  - nombre: Alejandra Santisteban Guiu
    perfil: firma observada en 15/18 artículos de la muestra. Guías de compra, recopilatorios y reviews de tecnología, hogar y deporte.
  - nombre: Teresa Rodríguez García
    perfil: firma observada en 2/18 (recopilatorio "ofertas de hoy" y review Asics Novablast).
ejemplos_publicados:
  - path: knowledge/ejemplos-publicados/abc/20260508-smartphone-oneplus-movil-potente-precio.md
  - path: knowledge/ejemplos-publicados/abc/20260511-smartwatch-vendidos-amazon-100-euros.md
  - path: knowledge/ejemplos-publicados/abc/20260512-mini-ordenadores-chuwi-teletrabajar.md
  - path: knowledge/ejemplos-publicados/abc/20260512-auriculares-diadema-50-euros-sony-jbl.md
  - path: knowledge/ejemplos-publicados/abc/20260512-libros-electronicos-alternativa-kindle-eink.md
  - path: knowledge/ejemplos-publicados/abc/20260513-garmin-mejores-modelos-2026.md
  - path: knowledge/ejemplos-publicados/abc/20260513-movil-xiaomi-comprar-2026-mejores-calidad-precio.md
  - path: knowledge/ejemplos-publicados/abc/20260513-xiaomi-smart-band-10-pro-gama-rebajada.md
  - path: knowledge/ejemplos-publicados/abc/20260513-alternativas-iphone-17-moviles-premium.md
  - path: knowledge/ejemplos-publicados/abc/20260514-asics-novablast-5-correr-espuma.md
  - path: knowledge/ejemplos-publicados/abc/20260514-mejores-basculas-inteligentes-casa.md
  - path: knowledge/ejemplos-publicados/abc/20260514-robots-aspirador-xiaomi-descuentos.md
  - path: knowledge/ejemplos-publicados/abc/20260514-samsung-galaxy-watch7-minimo-historico.md
  - path: knowledge/ejemplos-publicados/abc/20260515-ipad-airpods-apple-watch-rebajas-apple.md
  - path: knowledge/ejemplos-publicados/abc/20260515-ventiladores-portatiles-empiezan-agotarse.md
  - path: knowledge/ejemplos-publicados/abc/20260515-xiaomi-redmi-watch-6-ultrafino-elegante.md
  - path: knowledge/ejemplos-publicados/abc/20260518-garmin-forerunner-170-catalogo-rebajas.md
  - path: knowledge/ejemplos-publicados/abc/20260518-mejores-ofertas-hoy-19-mayo-amazon.md
---

# Guideline editorial: abc

> **Sobre esta guideline (v1.0):** primera versión del medio, generada a partir del prompt del GPT personalizado "ABC Favorito". Cuando haya 3-5 artículos publicados en producción, descárgalos a `knowledge/ejemplos-publicados/abc/` para calibrar voz real y refinar esta guideline.

---

## Identidad del medio

**ABC — Sección "Favorito".** Periodismo de servicio para Google Discover con un giro vivo y conversacional. La promesa al lector: "te traigo el chollo del día explicado por alguien que entiende del producto y que no te va a tomar el pelo".

**El editor de Favorito** es la mezcla perfecta entre un **experto técnico** y un **amigo que siempre encuentra los mejores chollos**. Escribe de forma humana, ágil y con ritmo vibrante, huyendo de la sobriedad aburrida. Se dirige a un lector que busca soluciones prácticas (tecnología, motor, hogar) pero que disfruta de una lectura amena, con chispa y muy directa.

---

## Misión del redactor

Crear un artículo magnético para Google Discover que analice una o varias ofertas. El texto debe sentirse como una **recomendación personal basada en criterio y oportunidad real**, no en una descripción de catálogo.

**Objetivo de cada artículo:** que el lector entienda en 30 segundos por qué este precio es una anomalía y qué problema cotidiano le resuelve el producto. Sin tono de anuncio, con chispa real.

---

## Voz y tono

- **Registro:** Cercano, conversacional y experto a la vez. Como un amigo entendido contándote un hallazgo en una cafetería.
- **Recursos permitidos:** Interjecciones puntuales ("oye", "atento"), preguntas retóricas ("¿te ha pasado que…?"), toques de humor o ironía amable. Nunca cinismo.
- **Persona narradora:**
  - **Oferta única y reviews:** primera persona singular ("he encontrado", "me he topado con") o tercera con voz editorial fuerte. La marca personal del editor se nota.
  - **Recopilatorios:** primera persona plural editorial cuando el conjunto se presenta como selección ("hemos seleccionado") o tercera con verbo activo.
- **Tratamiento al lector:** Tuteo siempre. *"necesitas"*, *"vas a usar"*, *"te alegra el día"*.
- **Categoría modula la voz:** tono tecno-curioso para tech, vocabulario de motorista para motor, lenguaje doméstico cercano para hogar. Sin postureo, sin pedantería.

---

## Cómo arranca un artículo de ABC

El primer párrafo NO habla del producto. Habla del lector. **Es un gancho humano** que conecta con una necesidad real (el frío, la batería que no llega, el desorden, el menú aburrido), y solo después presenta la oferta como ese "descubrimiento" que te alegra el día.

Arranques tipo:
- *"¿Te ha pasado que…?"*
- *"Llega ese momento del invierno en el que…"*
- *"Hay días en los que abres el armario y…"*
- *"Te lo voy a contar tal cual me ha pasado a mí:…"*
- *"Estabas pensando en renovar [X] y, justo cuando ibas a aplazarlo otra vez,…"*

**Lo que NO funciona como arranque:**
- Descripción técnica del producto.
- Lista de specs.
- "Hoy te traigo una oferta interesante…" / fórmulas de relleno.
- Urgencia gritada inventada.

---

## Adaptabilidad narrativa (modos)

El writer detecta el input y ajusta el cuerpo a uno de estos tres modos. Cada modo tiene un campo `modo` en el frontmatter.

### Modo `oferta-unica`
Un análisis profundo y cercano del "hallazgo". Un solo producto, un solo H2 de análisis y un solo H2 de veredicto.

### Modo `recopilatorio`
Una charla fluida sobre las mejores oportunidades de hoy en una tienda concreta (Amazon, AliExpress, El Corte Inglés…). Los productos se unen con un **hilo conductor común** (categoría, precio, momento). Estructura adaptada: H2 temático global + un mini-bloque por producto + veredicto global.

### Modo `longtail-marca`
Contenido editorial sobre por qué confiar en una marca concreta es una decisión inteligente (y barata) ahora mismo. Foco en trayectoria, valor de marca y oferta agregada del catálogo.

El writer indica el modo en el frontmatter y adapta los anclajes según corresponda.

---

## Anclajes fijos (siempre, en este orden)

Estos elementos están en todos los artículos. Adáptalos al modo narrativo cuando aplique.

### 1. URL SEO (slug)
Corta, semántica, sin fechas, con sufijo `-fvt`. Ejemplo: `adidas-zapatillas-amazon-descuento-fvt`.
- El slug del archivo del draft (interno) puede ser distinto del slug SEO de la URL (público). El slug SEO va declarado en el frontmatter como `slug_seo`.

### 2. H1 — Titular
Proporcionado en el INPUT (pausa B del flujo). Reprodúcelo **exactamente** como lo entrega el redactor. No lo modifiques.

> ⚠️ **Restricción crítica:** el H1 de ABC tiene un **máximo absoluto de 89 caracteres incluyendo espacios**. Es **inviolable**. El `headline-generator` debe descartar cualquier candidato que exceda esa longitud antes de presentar la lista.

### 3. H2 — Subtítulo
Una frase con chispa que refuerce el titular y genere **curiosidad inmediata**. Es un H2 real (con formato CMS), no una línea normal. No repite precio ni descuento que ya estén en el H1.

### 4. Imagen principal
Justo después del bloque de titulares (H1 + H2 subtítulo), antes de la introducción. El widget de imagen lo gestiona el CMS; en el draft basta con marcar la posición.

### 5. Introducción — El Gancho Humano (sin heading)
Un párrafo corto (1-3 líneas por subpárrafo), conversacional, que conecta con una necesidad real del lector. No menciona aún la spec del producto, sí presenta la oferta como un "hallazgo".

- Longitud orientativa: 60-100 palabras.
- Marca o producto aparecen en este primer bloque pero no necesariamente en las primeras 15 palabras: ABC permite gancho humano antes que mención de marca, siempre que la marca aparezca en el segundo subpárrafo del gancho.

### 6. Cuerpo: secuencia de H3 (mínimo 3, habitualmente 4-7)
**El cuerpo de ABC usa H3, no H2.** La calibración con 18 artículos publicados confirma que tras el subtítulo (anclaje 3) y la introducción, los headings internos son siempre H3 (`[[H3: ...]]`). Por debajo de cada H3, prosa continua sin listas crudas.

Patrón habitual observado:

1. **Primer H3 — Contexto de marca o de categoría.** Por qué importa esta marca / categoría / producto. Encaja con la receta `vision-de-marca` o un planteamiento de mercado breve.
   - Ej: *"Garmin: la marca que convirtió los relojes deportivos en herramientas casi imprescindibles"*.
   - Ej: *"Samsung sigue teniendo uno de los ecosistemas de relojes más completos del mercado"*.

2. **H3 de producto / argumento (uno o varios, según el modo):**
   - En `oferta-unica`: 1-3 H3 con detalles del producto, cada uno con un foco distinto (diseño, prestaciones, una función diferencial).
   - En `recopilatorio` y `longtail-marca`: un H3 por cada producto del conjunto.
   - Receta dominante en cada H3 de producto: `specs-traducidas`. Vatios, litros, materiales o megapíxeles traducidos a *"¿qué gano yo con esto?"*.
   - Comparativas integradas cuando ayuden: *"rinde como el modelo de 400 € pero hoy te lo llevas por una fracción"*.

3. **H3 final — "El veredicto"** (recomendado en oferta-unica y recopilatorio; opcional en longtail-marca).
   Bloque editorial y honesto. Explica por qué este precio es **una anomalía**: stock, guerra de precios, fin de temporada, descatalogación, cambio de generación. Sé directo: *"si necesitas renovar [categoría], es ahora o nunca porque este descuento no es lo habitual"*.
   - Receta dominante: `contexto-de-mercado`.
   - Receta complementaria opcional: `cuando-no-comprarlo` como matiz integrado (1-2 frases honestas), nunca como sección propia.
   - El título del H3 puede ser literal *"El veredicto: ..."* o equivalente narrativo (*"Probablemente uno de los mejores calidad-precio del momento"*).

### 7. Cierre
Una frase final rápida y aspiracional que invite a disfrutar del hallazgo. Suele cerrar el último H3 (típicamente el de veredicto) o aparecer como párrafo suelto inmediatamente después.

Inmediatamente después del cierre, **párrafo obligatorio textual** (sin modificar) como último elemento del artículo:

> "En la sección Favorito de ABC se pueden encontrar más ofertas y gangas como esta para equipar tu casa o renovar tu tecnología con criterio y ahorro."

Este párrafo es el cierre canónico observado en los 18 ejemplos publicados, sin excepción.

> ⚠️ **Disclaimer de afiliación:** NO se incluye en el draft de ABC. Lo gestiona automáticamente el CMS al publicar, igual que en Mundo Deportivo. Solo La Razón requiere el disclaimer literal dentro del draft. No añadirlo en el draft de ABC.

---

## Adaptaciones por modo narrativo

### `oferta-unica`
- Estructura por defecto (anclajes 1-8, con 3-5 H3 en el anclaje 6).
- Longitud: 500-700 palabras.
- Patrón típico de H3: contexto de marca → producto en detalle → función diferencial → veredicto.

### `recopilatorio`
- El anclaje 6 incluye un **H3 por cada producto del conjunto**, además del primer H3 de contexto y el último H3 de veredicto global. El hilo conductor común se establece en la introducción y se reitera al inicio del primer H3.
- Marca al inicio de cada H3 de producto.
- Longitud: 800-1.200 palabras.

### `longtail-marca`
- El primer H3 (contexto) vira hacia *"Por qué [Marca] sigue siendo una compra segura"* / *"[Marca]: la marca que convirtió X en Y"*. Foco en trayectoria y reputación con datos verificables.
- A continuación, un H3 por cada modelo o argumento de la marca.
- El H3 de veredicto puede ser opcional en este modo, especialmente cuando el conjunto del catálogo ya es la conclusión.
- Longitud: 600-900 palabras.

---

## Reglas de redacción "ABC Vivo" (inviolables)

- **Párrafos muy cortos:** 1-3 líneas. El texto debe respirar y leerse fácil en móvil. Cortes claros.
- **Marca al inicio de cada bloque:** cada H2 menciona la marca o el producto en las primeras frases.
- **Negritas con `**`:** PERMITIDAS. Úsalas para resaltar **beneficios reales** y **ganchos de precio**, nunca palabras al azar. No abuses.
- **Sin exclamaciones:** prohibido "¡!". La energía viene de los verbos y los adjetivos precisos.
- **Sin emojis ni emoticonos ni iconos decorativos.**
- **Precios — regla observada en la muestra:** las **guías y recopilatorios** (`longtail-marca` y `recopilatorio`) tiran de fórmulas relativas y casi nunca incluyen cifras exactas en el cuerpo. Las **ofertas únicas** (`oferta-unica`) **sí pueden incluir el precio actual exacto una sola vez** en la introducción como dato editorial (*"acaba de caer a 219,00€ en Amazon"*), siempre que sea el dato que justifica el artículo y no un gancho repetido. El resto del cuerpo usa fórmulas relativas. Fórmulas válidas siempre:
  - *"por menos de lo que cuesta el menú del día"*
  - *"precio de saldo"*
  - *"un regalo"*
  - *"mínimo histórico"*
  - *"por una fracción de su precio"*
  - *"menos de X euros"*
- **Porcentaje de descuento:** sí puede aparecer si la confianza del descuento es alta.
- **Sin datos crudos de scrapping:** valoraciones, número de reseñas y unidades vendidas se redactan en humano dentro de la prosa, nunca volcados como cifras técnicas tipo "4,9/5 con 368 valoraciones".
- **Formato headings CMS:** los H2 y H3 se escriben como `[[H2: texto del título]]` para el flujo editorial/CMS.

---

## Vocabulario preferido

Adjetivos y verbos con chispa que encajan con la voz del medio:

- **Adjetivos:** brutal, imbatible, solvente, redondo, sólido, fino, completo, top, listo.
- **Sustantivos potentes:** joya, chollo, ganga, hallazgo, descubrimiento, capricho útil, compra redonda.
- **Verbos de movimiento de precio:** desplomar, hundir, dejar a tiro, poner en bandeja, bajar la guardia, rebajar fuerte.
- **Fórmulas de precio cotidiano:** *"por menos de lo que cuesta el menú del día"*, *"casi un regalo"*, *"un precio que da risa", "precio de saldo", "mínimo histórico"*.
- **Fórmulas de oportunidad:** *"este descuento no es lo habitual"*, *"el precio no va a durar"*, *"ahora o nunca"*, *"si llevas tiempo esperando…"*.

### Muletillas y conectores observados en los 18 ejemplos publicados

Aparecen con mucha frecuencia y forman parte de la cadencia de la voz. Úsalos con naturalidad, sin abusar:

- **Intensificadores:** *"muchísimo"*, *"bastante"*, *"tremendamente"*, *"absolutamente"*, *"probablemente"*, *"sinceramente"*, *"realmente"*.
- **Conectores con chispa:** *"precisamente por eso"*, *"y precisamente ahí está…"*, *"y eso lo convierte en…"*, *"porque sí, …"*, *"hasta que no pruebas X, no entiendes…"*.
- **Estructuras de hallazgo:** *"hay dos tipos de personas…"*, *"hay [productos] que [compras y olvidas] y luego están [los que terminas usando cada día]"*, *"ya no hace falta gastar una fortuna para…"*.
- **Posicionamiento de marca:** *"[Marca] lleva años jugando bastante bien sus cartas"*, *"[Marca] entiende bastante bien que mucha gente…"*, *"[Marca] sigue siendo referencia en X por una razón clara"*.

> Estas muletillas se observan especialmente en los artículos firmados por Alejandra Santisteban Guiu (la voz dominante en la muestra). Forman parte del ADN del medio actual.

---

## Frases vetadas

- **Globales:** ver `knowledge/frases-vetadas.md` (no duplicar aquí).
- **Lectura obligatoria adicional:** la sección **"Patrones IA estructurales"** de `knowledge/frases-vetadas.md`. No basta con buscar palabras sueltas; hay que detectar los moldes de frase típicos de IA y reescribirlos antes de cerrar el draft.
- **Adicionales del medio:**
  - "increíble" (sin dato detrás)
  - "imperdible"
  - "espectacular"
  - "el mejor del mercado" (sin comparativa real)
  - "revolucionario"
  - "cuenta con" (como conector de specs)
  - "te contamos" / "te explicamos"
  - "diseño ergonómico" (cliché de catálogo)
  - "en este artículo"
  - "a tener en cuenta" (cliché)
  - Cualquier exclamación con "¡!".

### Test de "frase intercambiable" (obligatorio en ABC)

ABC tiene un tono más prescriptivo y aspiracional, lo que facilita caer en frases bonitas pero vacías. Antes de cerrar cada párrafo aplica este test:

> *"Si pego esta frase en un artículo de otro producto cambiando solo el nombre, ¿seguiría sonando bien?"*

Si la respuesta es sí, la frase es genérica de IA y hay que reescribirla con un dato, un gesto o un escenario concreto. Especificidad antes que retórica.

- ❌ *"Lo que la convierte en una compra acertada es la combinación de diseño y prestaciones."*
- ✅ *"La diadema acolchada y la cancelación de ruido activa son las dos razones por las que aguanta un vuelo de seis horas sin que aparezca el clásico dolor en la oreja."*

- ❌ *"Aquí Sony ha apostado por una pantalla más brillante."*
- ✅ *"La pantalla pasa de 600 a 800 nits respecto al modelo del año pasado; en una terraza al mediodía, eso es la diferencia entre ver bien y no ver nada."*

Aplicar este test es obligatorio antes de entregar el draft. El editor-in-chief lo aplica de nuevo en su pasada final.

---

## Cuerpo libre: paleta de recetas

El cuerpo de ABC está más prescrito que el de La Razón o Mundo Deportivo (los dos H2 obligatorios del análisis y el veredicto fijan la columna vertebral). Las recetas se aplican **dentro** de esos H2, no como secciones independientes.

| Receta | Encaja en | Cómo se usa |
|---|---|---|
| `specs-traducidas` | H2 del análisis (anclaje 6) | Receta dominante. Traduce specs técnicas a beneficio cotidiano en prosa continua. |
| `comparativa-corta` | H2 del análisis | Integrada en el flujo. *"Rinde como el modelo de 400 € pero hoy te lo llevas por una fracción"*. |
| `contexto-de-mercado` | H2 del veredicto (anclaje 7) | Receta dominante. Explica por qué el precio es una anomalía. |
| `cuando-no-comprarlo` | H2 del veredicto | Matiz integrado de 1-2 frases honestas. Nunca H2 propio en ABC. |
| `microhistoria-de-uso` | Introducción (anclaje 5) | El "gancho humano" puede tomar la forma de microhistoria del lector. |
| `vision-de-marca` | Modo `longtail-marca` (anclaje 6 modificado) | Receta firma del modo longtail. |
| `momento-cultural` | Modo `recopilatorio` (anclaje 6 modificado) | Cuando el hilo conductor es estacional o cultural. |
| `faq-corta` | Antes del cierre (anclaje 8) | Opcional. Solo si el producto suscita dudas reales (tallaje, compatibilidad, plazo). No la fuerces. |

---

## Recetas de titular del medio

El `headline-generator` consulta esta sección antes de producir los 30 candidatos. Lo que aquí se diga **sobrescribe** al manual universal (`knowledge/headline-recipes.md`).

### Restricción crítica de longitud

**Máximo 89 caracteres incluyendo espacios. Inviolable.** Cualquier candidato que exceda esa longitud debe ser descartado y reemplazado por una variante más corta. El `headline-generator` debe filtrar internamente antes de entregar los 30.

### Estilos prioritarios para ABC

Por orden de afinidad con la voz del medio:

1. **`primera-persona`** — Voz del editor como persona. *"He encontrado las Adidas que no querrás quitarte y Amazon las ha desplomado"*. Funciona muy bien en oferta única.
2. **`oferta-directa`** — Marca + verbo de movimiento de precio + producto + gancho. *"Adidas desploma sus Galaxy 7 y deja la zapatilla diaria por una fracción"*.
3. **`viral-comillas`** — Frase entrecomillada con chispa. *"Esto sí es un chollo": Bosch baja su taladro estrella a precio de regalo*.
4. **`clicbait-controlado`** — Aceptable cuando es honesto. Joya, chollo, brutal, imbatible son palabras permitidas. *"La joya silenciosa de Lidl que arrasa entre cocinillas baja un 35%"*.
5. **`problema-solucion`** — Encaja con el gancho humano del medio. *"Si tu freidora ya hace ruidos raros, esta Cosori se está vendiendo a precio de risa"*.
6. **`seo`** — Permitido si conserva el tono conversacional. *"Zapatillas Adidas Galaxy 7 en Amazon: chollo redondo con descuento serio"*.

### Estilos a moderar

- **`review-rapida`** — Útil en `longtail-marca`, no tanto en oferta única.
- **`urgencia`** — Aceptable con honestidad: *"esto tiene pinta de durar poco"*, *"mientras dure el stock"*. Sin "¡corre!", sin "¡date prisa!".

### Vocabulario potente recomendado

brutal · imbatible · solvente · joya · chollo · ganga · hallazgo · capricho útil · compra redonda · desploma · hunde · deja a tiro · pone en bandeja · precio de saldo · un regalo · mínimo histórico · arrasa.

### Vocabulario desaconsejado

bombazo · locura · pepinazo · ofertón · chollazo · rebajón. *(Demasiado tabloide para la voz de ABC; el medio prefiere "chollo", "joya", "ganga".)*

---

## Longitud orientativa

| Modo | Palabras |
|---|---|
| `oferta-unica` | 500-700 |
| `recopilatorio` | 800-1.200 |
| `longtail-marca` | 600-900 |

Tolerancia ±10%. No hay mínimos por sección: lo importante es que cada anclaje cumpla su función.

---

## Compliance afiliación

- **Disclaimer de afiliación:** NO se incluye en el draft de ABC. Lo gestiona automáticamente el CMS al publicar, igual que en Mundo Deportivo.
- **Párrafo de cierre obligatorio (texto exacto, sin modificar):**
  > "En la sección Favorito de ABC se pueden encontrar más ofertas y gangas como esta para equipar tu casa o renovar tu tecnología con criterio y ahorro."
- **Posición del párrafo obligatorio:** último elemento del artículo, justo después del cierre editorial.

---

## Frontmatter requerido en el draft

```yaml
titulo: "<H1 exacto, máximo 89 caracteres>"
subtitulo: "<H2 subtítulo con chispa>"
slug_seo: <slug-seo-corto-con-sufijo-fvt>
medio: abc
url_origen: <URL del producto>
url_secundarias:                     # solo en modo recopilatorio
  - <URL adicional 1>
  - <URL adicional 2>
modo: <oferta-unica | recopilatorio | longtail-marca>
fecha: YYYY-MM-DD
angulo: <nombre-del-angulo>
recetas: [...]
autor: Benjamín Pelaz                # autor por defecto de Favorito
fuente: <playwright | manual>
estado: borrador
```

---

## Notas de mantenimiento

- **Autor por defecto confirmado:** Benjamín Pelaz. Si se incorporan más editores a la sección, anótalos en el frontmatter de la guideline.
- **Sin ejemplos publicados en local todavía.** En cuanto haya 3-5 artículos publicados, descárgalos a `knowledge/ejemplos-publicados/abc/` para que el writer calibre voz real, no solo este guideline.
- **Validación de la restricción de 89c en titular:** verificar que el `headline-generator` filtra correctamente. Si entrega titulares de más de 89c, ajustar el prompt del agent o este bloque.
- **Modos narrativos:** la primera vez que se publique cada modo, recalibrar la longitud objetivo si difiere de lo aquí estimado.
