---
date: 2026-05-08
topic: agentes-redactores-ofertas
---

# Sistema de agentes Claude Code para redactores de artículos de oferta

## Problem Frame

Existe un proyecto previo (Django, panel web, scraping + scoring) pensado para ayudar a un equipo de redactores a producir artículos de oferta. **No fue adoptado**: del flujo completo, los redactores solo usaban el listado de ofertas como buscador y hacían el resto fuera del sistema (montar payload manual, ir al GPT personalizado por medio, copiar/pegar el markdown, retocar). Las cuatro causas se confirmaron simultáneamente: cambiaba su flujo, solo automatizaba el principio, el criterio del scoring no acertaba, y faltó acompañamiento.

La nueva propuesta invierte el enfoque siguiendo el patrón de [thruuu-claude-writer](https://github.com/thruuu/thruuu-claude-writer): en lugar de un panel web pesado, un proyecto Claude Code ligero donde el redactor pega una URL de oferta y un pipeline de subagentes produce un markdown listo para revisar y subir, en su misma herramienta de IA. Los GPTs personalizados por medio se reemplazan por archivos `GUIDELINE-{medio}.md` que codifican voz, estructura y compliance.

El cambio crítico respecto al intento anterior: el sistema **no sustituye el flujo del redactor**, lo *cubre*. El redactor sigue descubriendo ofertas como ya hace; lo que se automatiza es exactamente la parte dolorosa que hoy ocurre fuera de cualquier herramienta.

## Requirements

- **R1. Entrada por URL de oferta**
  El redactor inicia el flujo pegando una URL de Amazon/AliExpress/etc. al lanzar un slash command (p.ej. `/crear-articulo`). No se requiere brief, payload ni metadatos previos. El sistema deduce todo lo necesario a partir de la URL y del medio destino.

- **R2. Selección de medio**
  Antes (o durante) la ejecución, el redactor indica el medio destino. El sistema usa el `GUIDELINE-{medio}.md` correspondiente para tono, estructura, longitud, secciones, compliance de afiliación y políticas editoriales.

- **R3. Pipeline de subagentes especializados**
  El proyecto contiene un orquestador (`CLAUDE.md`) y subagentes (`.claude/agents/`) que se encargan, mínimamente, de: extraer datos del producto desde la URL, contrastar precio/descuento, resumir reseñas, elegir ángulo editorial, redactar siguiendo la guideline del medio, humanizar y revisar. La descomposición exacta queda para planning, pero el resultado debe ser un único markdown final.

- **R4. Guidelines por medio como reemplazo de los GPTs personalizados**
  Existe un slash command `/crear-guideline` que entrevista al redactor sobre el medio (tono, longitud típica, estructura H2/H3, do's & don'ts, frases prohibidas, formato de afiliación) y genera o actualiza `GUIDELINE-{medio}.md`. Es el equivalente al "create guideline" de thruuu, adaptado a medios de oferta. Permite jubilar progresivamente los GPTs personalizados manteniendo la voz.

- **R5. Conocimiento propietario opcional**
  Carpeta `/knowledge` con material que afina los outputs sin estar atado a un medio: artículos publicados de referencia, frases vetadas a nivel de marca, criterios de afiliación, glosario, ángulos preferidos. Los agentes la consultan cuando aporta. Empieza vacía o con 2-3 ficheros mínimos.

- **R6. Output como markdown local revisable**
  El artículo final se guarda en `/drafts/{medio}/{fecha}-{slug}.md` con frontmatter (URL origen, medio, fecha, ángulo elegido). El redactor lo abre, lo revisa, lo edita si hace falta, y lo sube manualmente al CMS. La publicación al medio queda fuera de alcance.

- **R7. Operable desde la app Claude por usuarios no técnicos**
  Los redactores no tocan terminal. Abren el proyecto desde la app de Claude (desktop/web), seleccionan el slash command y siguen las preguntas que el agente les hace. El setup inicial (instalar app, abrir el proyecto compartido) debe estar documentado paso a paso para perfiles no técnicos.

## Success Criteria

- Un redactor produce un artículo de oferta de calidad publicable en **menos tiempo del que tarda hoy** con el GPT personalizado, en al menos el 70% de los casos. Cifra base a medir con el primer redactor antes de generalizar.
- **≥ 80%** de los markdowns generados se publican con edición ligera (no reescritura completa). Si baja de ese umbral en un medio concreto, el problema está en su `GUIDELINE-{medio}.md`, no en la pipeline.
- El redactor es capaz de actualizar la guideline de su medio por sí mismo (vía `/crear-guideline`) sin intervención de un técnico, después de haberla creado una vez con acompañamiento.
- Adopción real medida en uso semanal, no en demos. Si tras 3 semanas un redactor sigue usando el GPT antiguo en paralelo, hay un fallo de diseño que toca atender, no insistir.

## Scope Boundaries

- **Fuera de alcance**: descubrimiento/scraping de ofertas. El input es una URL pegada por el redactor.
- **Fuera de alcance**: integración con el sistema Django previo. No se lee su BD, no se escribe en ella. Conviven sin acoplarse.
- **Fuera de alcance**: panel web, bot Telegram/Discord, o cualquier UI propia. La UI es la app de Claude.
- **Fuera de alcance**: deduplicación / control de "ya publicado" en MVP. Se confía en el criterio del redactor. Se reabrirá si aparecen duplicados reales.
- **Fuera de alcance v1**: artículos SEO long-form (estilo thruuu original). El diseño debe permitir añadirlos después reusando piezas (humanizer, editor, guidelines), pero no se implementan ahora.
- **Fuera de alcance**: publicación automática al CMS. El redactor sube manualmente.
- **Fuera de alcance**: reescritura de los GPTs personalizados como prompts API directos. Se sustituyen por guidelines en markdown leídas por los agentes.

## Key Decisions

- **Patrón thruuu como base arquitectónica**: `CLAUDE.md` orquestador + `.claude/agents/` + slash commands + carpetas `/drafts` `/knowledge` `/guidelines`. *Rationale*: receta validada en el dominio adyacente (SEO content), trabaja en el entorno donde el redactor ya conversa con IA, y minimiza superficie técnica para no repetir el lastre del Django previo.

- **Reemplazo de GPTs por `GUIDELINE-{medio}.md`**: una herramienta única (Claude) en lugar de Claude + chatgpt.com. *Rationale*: simplifica setup, elimina fragilidad operacional (Playwright contra chatgpt.com era el principal punto débil del diseño anterior), y permite versionar la voz editorial en texto plano.

- **Input por URL pegada, no integración con descubrimiento**: el descubrimiento es lo único que sí funcionaba en el sistema previo y los redactores ya lo hacen bien por su cuenta. *Rationale*: aislar el problema real (todo lo que viene después de elegir la oferta) sin arrastrar dependencias del sistema viejo.

- **Usuarios directos los redactores, vía app Claude**: misma decisión que falló antes, pero con dos diferencias materiales: (a) sin terminal, sin panel propio, todo en una app que ya es "chat con IA"; (b) sin obligación de cambiar el descubrimiento, solo lo que ya hacen mal. *Rationale*: si esta forma tampoco se adopta, ningún rediseño técnico va a salvarlo y la conclusión sería que el redactor no quiere automatizar la redacción, no que la herramienta esté mal.

- **Sin control de duplicados en MVP**: aplazado deliberadamente. *Rationale*: foco. Si aparece como problema real en uso, se añade `/published.md` o lectura ligera del Django. Antes, no.

- **Diseño extensible a SEO long-form, sin construirlo**: las piezas reusables (humanizer, editor, guidelines, knowledge) se nombran y se ubican pensando en que mañana entre una segunda pipeline. *Rationale*: la extensión a SEO genérico es plausible y compartirá voz/medio. Diseñar contra ese futuro tiene coste cero hoy.

## Dependencies / Assumptions

- Los redactores aceptarán instalar la app de Claude y abrir un proyecto compartido. Si no, hay que volver a la mesa de dibujo del canal de uso.
- Hay al menos un redactor "champion" dispuesto a ser el primer usuario y a ayudar a iterar guidelines y knowledge antes de generalizar al equipo.
- La voz de los GPTs personalizados se puede capturar razonablemente bien en un markdown estructurado. Si la voz depende de fine-tuning con cientos de ejemplos imposibles de describir, el reemplazo no es viable y habría que volver a Playwright.
- Volumen objetivo se mantiene en ≤ 10 artículos/día/equipo. Un salto a 100/día reabriría preguntas de orquestación y descubrimiento.
- Cada redactor tendrá una cuenta Claude con plan suficiente para correr pipelines de varios subagentes diariamente.

## Outstanding Questions

### Resolve Before Planning

*(ninguna bloqueante — el brainstorm cierra las decisiones de producto)*

### Deferred to Planning

- **[Afecta R3][Técnico]** Descomposición exacta de subagentes: candidatos a evaluar — `product-researcher` (extrae ficha desde URL), `price-validator` (contrasta descuento), `reviews-summarizer`, `angle-picker` (elige ángulo editorial entre recomendación / liquidación / comparativa / precio psicológico / uso práctico / tendencia), `writer`, `humanizer`, `editor-in-chief`. Decidir cuáles fusionar para no inflar la pipeline en artículos de 600-1200 palabras.
- **[Afecta R1, R3][Técnico / necesita research]** Estrategia de extracción de datos de Amazon/AliExpress desde Claude Code: WebFetch nativo, MCP de scraping, o simplemente leer la página y dejar al modelo extraer. Validar bloqueos antibot y calidad de datos.
- **[Afecta R4][Producto]** Estructura concreta de `GUIDELINE-{medio}.md`: qué campos son obligatorios, cómo se versionan, dónde encajan ejemplos de artículos publicados como anclaje de estilo.
- **[Afecta R6][Producto]** Convención de carpetas, frontmatter, naming, y dónde vive el proyecto compartido (Git, Drive sincronizado, OneDrive). Determina cómo varios redactores trabajan sin pisarse.
- **[Afecta R7][Operacional]** Guía de instalación y onboarding para perfiles no técnicos: cómo abren el proyecto, cómo identifican qué slash command usar, qué pasa si la app pide permisos. Material de soporte mínimo viable.
- **[Afecta R3][Producto]** Cuánta interactividad tiene la pipeline: ¿el redactor puede vetar/sustituir el ángulo elegido por `angle-picker` antes de redactar? ¿Hay un punto de pausa intermedio o es one-shot?
- **[Afecta éxito global][Operacional]** Plan de validación con el redactor champion antes de extender al equipo: cuántos artículos, qué se mide, criterios de go/no-go.

## Next Steps

→ `/ce:plan` para planificación estructurada de la implementación.
