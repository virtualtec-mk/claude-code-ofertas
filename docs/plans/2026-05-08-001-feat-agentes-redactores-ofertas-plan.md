---
title: Sistema de agentes Claude Code para redactores de artículos de oferta
type: feat
status: phase1-built
date: 2026-05-08
origin: docs/brainstorms/2026-05-08-agentes-redactores-ofertas-requirements.md
---

# Sistema de agentes Claude Code para redactores de artículos de oferta

## Overview

Construir un proyecto Claude Code que un redactor abre desde la app oficial (sin terminal), pega una URL de Amazon/AliExpress, indica el medio destino, y obtiene un markdown listo para revisar y subir al CMS. La voz por medio se codifica en archivos `GUIDELINE-{medio}.md` que reemplazan los GPTs personalizados actuales. Cuatro subagentes especializados (`product-researcher`, `angle-picker`, `writer`, `editor-in-chief`) orquestados por `CLAUDE.md` cubren toda la pipeline. Sin panel web, sin Django, sin scraping propio, sin Playwright.

Inspiración arquitectónica directa: [thruuu-claude-writer](https://github.com/thruuu/thruuu-claude-writer), adaptado al dominio de oferta (artículos cortos, ángulo editorial explícito, compliance afiliación) y al perfil de usuario (redactores no técnicos vía app de Claude).

## Problem Statement / Motivation

(carry from origin: ver `docs/brainstorms/2026-05-08-agentes-redactores-ofertas-requirements.md` § Problem Frame)

El proyecto previo en `C:\Users\andre\proyectos-IA\Proyecto analizador de ofertas` (Django + scraping + scoring + panel) no fue adoptado por las cuatro causas a la vez (cambiaba flujo, solo automatizaba el principio, scoring no acertaba, faltó change management). El único uso real fue como buscador de ofertas. Esta propuesta no compite con esa parte: deja al redactor descubrir como ya hace, y automatiza estrictamente lo que hoy ocurre fuera de cualquier sistema (montar payload → ir al GPT → copiar markdown → ajustar).

## Proposed Solution

**Un proyecto Claude Code compartido** (carpeta sincronizada vía OneDrive en MVP, migrable a Git después) que cada redactor abre desde la app de Claude. Tres slash commands operan toda la herramienta:

- `/crear-articulo <url> [medio]` — pipeline principal.
- `/crear-guideline <medio>` — entrevista guiada para crear/actualizar la voz de un medio.
- `/importar-gpt <medio>` — asistente que extrae las instrucciones del GPT personalizado existente y las convierte a `GUIDELINE-{medio}.md`.

La pipeline `/crear-articulo` ejecuta cuatro subagentes en orden, **con un único punto de pausa interactiva** después del `angle-picker` para que el redactor confirme o cambie el ángulo editorial elegido. Esa pausa es deliberada: es donde el redactor siente control y aporta criterio editorial, y es lo que separa "asistente útil" de "panel que decide por mí" (causa raíz #3 del intento previo).

## Architecture

### Estructura del proyecto

```
claude-code-text-agents/
├── CLAUDE.md                              # orquestador principal, contexto global de proyecto
├── README.md                              # qué es el proyecto, cómo usarlo (apunta a onboarding)
├── .claude/
│   ├── agents/
│   │   ├── product-researcher.md          # extrae ficha + reseñas + precio desde URL
│   │   ├── angle-picker.md                # elige ángulo editorial (1 de 6)
│   │   ├── writer.md                      # redacta + humaniza, usa GUIDELINE del medio
│   │   └── editor-in-chief.md             # checklist final + frontmatter + compliance
│   ├── skills/
│   │   ├── crear-articulo/SKILL.md        # comando principal, orquesta subagentes
│   │   ├── crear-guideline/SKILL.md       # entrevista para definir voz por medio
│   │   └── importar-gpt/SKILL.md          # asistente para migrar GPT → guideline
│   └── settings.json                      # permisos (ver § Permisos)
├── guidelines/
│   ├── GUIDELINE-{medio-A}.md             # voz, estructura, compliance del medio A
│   └── GUIDELINE-{medio-B}.md             # ídem
├── knowledge/
│   ├── ejemplos-publicados/{medio}/       # 2-3 artículos ya publicados por medio
│   ├── frases-vetadas.md                  # global, transversal a medios
│   └── politicas-afiliacion.md            # disclaimers obligatorios
├── drafts/
│   └── {medio}/
│       └── 2026-05-08-{slug}.md           # output de la pipeline
└── docs/
    ├── brainstorms/                       # requirements docs (incluye el origen)
    ├── plans/                             # planes de implementación (este archivo)
    └── onboarding-redactores.md           # paso a paso para perfil no técnico
```

### Subagentes — especificación funcional

Cada subagente vive en `.claude/agents/<nombre>.md` con frontmatter `name`, `description` (clave para que Claude principal sepa cuándo invocarlo) y `tools` (acceso restringido a lo necesario).

**`product-researcher`** — Input: URL de oferta. Tools: `WebFetch`, `Read`. Output esperado en formato markdown estructurado con frontmatter (nombre, marca, modelo, ASIN/EAN si existe, precio actual, precio antes si visible, % descuento, descripción corta, especificaciones clave, pros/contras destilados de reseñas, número y media de reseñas, nivel de confianza del descuento). Si `WebFetch` falla por antibot, devuelve un mensaje claro pidiendo al usuario que pegue la ficha o un screenshot.

**`angle-picker`** — Input: ficha del producto + nombre del medio + (opcional) `GUIDELINE-{medio}.md`. Tools: `Read`. Output: ángulo elegido (uno de: `recomendacion-personal`, `liquidacion`, `comparativa`, `precio-psicologico`, `uso-practico`, `tendencia`) + 2 frases de justificación + propuesta de titular tentativo. **Importante**: este agente NO redacta; solo decide el ángulo editorial.

**`writer`** — Input: ficha del producto + ángulo confirmado por el redactor + `GUIDELINE-{medio}.md` + `knowledge/ejemplos-publicados/{medio}/*`. Tools: `Read`, `Write`. Output: el artículo completo en markdown siguiendo la estructura de la guideline, con humanización integrada (sin frases-IA típicas, sin "imperdible/corre/chollazo" salvo que la guideline las permita). Guarda en `drafts/{medio}/{fecha}-{slug}.md`.

**`editor-in-chief`** — Input: el draft generado + `GUIDELINE-{medio}.md` + `knowledge/politicas-afiliacion.md`. Tools: `Read`, `Edit`. Aplica un checklist final: longitud dentro de rango, headings correctos, disclaimer afiliación presente, frases vetadas ausentes, frontmatter completo (medio, url_origen, asin si aplica, fecha, ángulo, estado=`borrador`). Devuelve el draft corregido + un resumen breve al hilo principal: "draft listo en `<ruta>`. Cambios aplicados: [...]".

> Decisión: **4 subagentes consolidados** (no 6-7) porque los artículos de oferta son cortos (600-1200 palabras) y separar `humanizer` y `reviews-summarizer` añade saltos de contexto sin ganancia clara. Si en Fase 2 la calidad de un paso flojea, se separa entonces (ver § Outstanding Questions).

### Slash commands (skills) — especificación funcional

Cada skill vive en `.claude/skills/<nombre>/SKILL.md`. Usar el formato `skills/` (no `commands/`) porque permite `disable-model-invocation`, `argument-hint`, ficheros de soporte, y es la forma vigente recomendada.

**`/crear-articulo`** — `argument-hint: <url> [medio]`. Si no se da `medio`, pregunta interactivamente listando los medios disponibles (lee `guidelines/GUIDELINE-*.md`). Orquesta:
1. Invoca `product-researcher` con la URL.
2. Invoca `angle-picker` con la ficha + medio.
3. **Pausa**: muestra al redactor el ángulo propuesto + justificación + titular tentativo. Pregunta: "¿Confirmas este ángulo, eliges otro de la lista, o lo dictas tú?". Espera respuesta antes de continuar.
4. Invoca `writer` con ángulo confirmado.
5. Invoca `editor-in-chief` para el pase final.
6. Reporta ruta del draft + resumen de qué se generó.

`disable-model-invocation: true` — solo el redactor lo lanza explícitamente, nunca Claude por su cuenta.

**`/crear-guideline`** — `argument-hint: <nombre-medio>`. Entrevista guiada que pregunta uno por uno: tono y registro, longitud objetivo (palabras), estructura H2/H3 esperada, dónde va imagen y CTA, frases preferidas, frases vetadas, formato exacto del disclaimer de afiliación, frontmatter requerido en el draft, URLs de 2-3 artículos ya publicados como ejemplos. Genera o actualiza `guidelines/GUIDELINE-{medio}.md` con el schema definido en § Schema de guideline. Si el archivo ya existe, pregunta si actualizar campo a campo o sobrescribir.

**`/importar-gpt`** — `argument-hint: <nombre-medio>`. Pregunta al redactor que pegue las instrucciones actuales del GPT personalizado y opcionalmente 2-3 URLs/markdown de artículos publicados con ese GPT. Extrae patrones automáticamente (tono, longitud, frases recurrentes) y los rellena en una guideline borrador. Después, lanza la entrevista de `/crear-guideline` solo para los campos que no pudo deducir, marcándolos. Output: `guidelines/GUIDELINE-{medio}.md` listo para revisión humana.

### Schema de `GUIDELINE-{medio}.md`

```markdown
---
medio: medio-A
version: 1
ultima_actualizacion: 2026-05-08
ejemplos_publicados:
  - url: https://...
  - url: https://...
---

# Guideline editorial: {medio-A}

## Voz y tono
- Registro: [cercano-experto / formal / desenfadado / ...]
- Persona narradora: [primera persona singular / plural / impersonal]
- Tratamiento al lector: [tú / usted / impersonal]

## Longitud y estructura
- Palabras objetivo: [rango]
- Estructura esperada:
  - H1: titular del artículo
  - Párrafo de entrada (X palabras)
  - H2 1: [propósito]
  - H2 2: [propósito]
  - ...
- Posición de la imagen principal: [después del H1 / después del primer H2]
- Posición del CTA / botón de compra: [tras descripción / al final / ambos]

## Frases preferidas
- [...]

## Frases vetadas
- [...]

## Compliance afiliación
- Disclaimer obligatorio (texto exacto): "[...]"
- Posición del disclaimer: [primer párrafo / antes del primer link / al final]
- Formato del enlace de afiliación: [...]

## Frontmatter requerido en el draft
```yaml
medio: ...
url_origen: ...
asin: ...
fecha: YYYY-MM-DD
angulo: ...
estado: borrador
```

## Notas adicionales
[Lo que no encaja en otros sitios pero el writer debe respetar]
```

### `CLAUDE.md` orquestador — contenido mínimo

- Quién es el usuario (redactor no técnico vía app Claude).
- Cómo arrancar (referencia a los 3 slash commands).
- Convención de carpetas y para qué sirve cada una.
- Regla operativa: "no inventes datos del producto; si la ficha es incompleta, pide al redactor que pegue lo que falta. No publiques borradores con `[PENDIENTE]` en el frontmatter."
- Idioma: todo en español.
- Política de uso de `WebFetch`: solo sobre URLs pegadas por el redactor; no descubrir ofertas por iniciativa propia.

### Permisos (`.claude/settings.json`)

- Permitir `WebFetch` sobre dominios `amazon.es`, `amazon.com`, `aliexpress.com`, etc., sin pedir permiso por cada URL.
- Permitir `Write` y `Edit` solo dentro de `drafts/` y `guidelines/`.
- `Read` libre dentro del proyecto.
- Bash desactivado por defecto (no se necesita, reduce superficie y baja prompts de permiso al redactor).

## Implementation Phases

### Phase 1 — Foundation (champion único, un medio)

**Objetivo:** validar que un redactor real produce artículos publicables con calidad ≥ a su flujo actual, antes de extender.

**Entregables:**
- `CLAUDE.md` redactado.
- 4 subagentes en `.claude/agents/`.
- Skill `/crear-articulo` con la pausa interactiva del ángulo.
- Skill `/crear-guideline` (entrevista completa).
- `GUIDELINE-{medio-piloto}.md` co-creada con el champion en una sesión guiada.
- 2-3 artículos en `knowledge/ejemplos-publicados/{medio-piloto}/`.
- `docs/onboarding-redactores.md` con screenshots reales del flujo.
- Carpeta del proyecto sincronizada vía OneDrive a la máquina del champion.

**Criterios de éxito de la fase:**
- Champion completa 5 artículos consecutivos siguiendo el flujo end-to-end.
- ≥ 4 de 5 se publican con edición ligera (no reescritura completa).
- El champion declara explícitamente que prefiere este flujo al GPT personalizado.

**Esfuerzo estimado:** 1-2 semanas de construcción + 2 semanas de uso real con champion.

### Phase 2 — Multi-medio

**Objetivo:** cubrir todos los medios donde se publican ofertas, sin sumar usuarios todavía.

**Entregables:**
- Skill `/importar-gpt` para acelerar la creación de guidelines del resto de medios.
- Una `GUIDELINE-{medio}.md` por cada medio activo, validada con el champion o con el redactor de referencia de cada medio.
- `knowledge/ejemplos-publicados/{medio}/` poblado para cada medio.
- Iteración de prompts de subagentes según fallos detectados en Fase 1.

**Criterios de éxito:**
- El champion produce artículos para los N medios sin reescritura completa en ≥ 80% de casos.
- El tiempo medio por artículo es menor que el flujo previo en al menos un 30%.

**Esfuerzo estimado:** 1 semana de construcción + 1-2 semanas de iteración.

### Phase 3 — Multi-redactor

**Objetivo:** abrir a todo el equipo, manteniendo calidad y adopción.

**Entregables:**
- Sesión de onboarding síncrono por redactor (45-60 min) con `docs/onboarding-redactores.md` como guion.
- Migración del proyecto compartido a Git privado si en Fase 1-2 los conflictos de OneDrive son problema (decisión basada en datos, no anticipada).
- Convención: cada redactor "posee" la edición de las guidelines de los medios donde publica; el resto las consulta sin tocar.
- Métrica semanal de uso por redactor (cuántos `/crear-articulo` ha lanzado, cuántos drafts publicados).

**Criterios de éxito:**
- Tras 3 semanas, ≥ 70% de los redactores tienen uso semanal real.
- Si un redactor sigue usando exclusivamente el GPT antiguo a las 3 semanas, se hace entrevista 1-a-1 para identificar la fricción concreta.

**Esfuerzo estimado:** 2-3 semanas de despliegue + soporte continuo.

### Phase 4 — Optimización (condicional)

Solo se ejecuta si Fases 1-3 demuestran valor. Posibles trabajos:
- Separar `humanizer` y `reviews-summarizer` si la calidad de algún paso flojea.
- Añadir control de duplicados (`/published.md` o lectura ligera del Django previo) si aparece como dolor real.
- Extender a artículos SEO long-form reusando `writer`, `editor-in-chief` y `knowledge` (cubre el "diseño extensible" del brainstorm).
- Migración a Git si OneDrive escala mal.

## Technical Decisions (resoluciones de los Deferred to Planning del origen)

- **Descomposición de subagentes (origen R3):** 4 subagentes consolidados, no 6-7. *Rationale:* artículos cortos no justifican más saltos de contexto; mantiene latencia y coste bajo control; deja la separación como optimización posterior con datos.

- **Extracción de datos desde URL (origen R1, R3):** `WebFetch` nativo de Claude Code. Sin scraping propio, sin MCP browser en MVP. *Rationale:* la herramienta más simple que probablemente funciona; cuando falle, el agente pide al redactor que pegue la ficha (degradación graceful, no fallo). Si en uso real Amazon bloquea sistemáticamente, se evalúa MCP Playwright como capa opcional sin reescribir la pipeline.

- **Estructura de `GUIDELINE-{medio}.md` (origen R4):** schema fijo definido arriba. *Rationale:* campos estables permiten que `/crear-guideline`, `/importar-gpt` y `writer` compartan contrato.

- **Sincronización del proyecto compartido (origen R6):** **OneDrive sincronizado en MVP**, migración a Git en Fase 4 si se justifica. *Rationale:* OneDrive es invisible para el redactor (cero fricción técnica), y con un solo champion en Fase 1 los conflictos no son problema. Git añade barrera de entrada que probablemente mata adopción si se exige desde el día 1. La pérdida de versionado se compensa con respaldos OneDrive y, si hace falta, exportes manuales periódicos.

- **Interactividad de la pipeline (origen R3):** **una sola pausa**, después de `angle-picker`. *Rationale:* es el único momento donde la decisión humana cambia materialmente el output. Más pausas convierten la herramienta en un workflow asíncrono pesado; menos pausas reproducen el "panel que decide por mí" del intento previo.

- **Onboarding (origen R7):** documento `docs/onboarding-redactores.md` con screenshots reales, validado leyéndolo *con* un redactor antes de generalizar. *Rationale:* el material de onboarding nunca se valida hasta que un usuario real lo sigue paso a paso; sin esa validación es ficción.

- **Plan de validación con champion (origen Operacional):** Fase 1 con un único redactor durante 2-3 semanas, métrica binaria por artículo (publicado con edición ligera = sí/no), go/no-go al final de la fase. *Rationale:* si un champion motivado no lo adopta, el equipo entero tampoco — es el filtro más rápido y barato.

## System-Wide Impact

- **Interacción con sistema previo (Django):** ninguna. El nuevo proyecto vive en un repo distinto, no lee ni escribe en la BD del Django, no comparte autenticación. Conviven sin acoplarse.
- **Interacción con GPTs personalizados:** los GPTs siguen activos en `chatgpt.com` durante todo el rollout. Se jubilan medio por medio cuando su `GUIDELINE-{medio}.md` produce calidad equivalente. Decisión de jubilación: del champion para el suyo, después de cada redactor para el suyo. Sin fechas duras.
- **Coste API de Claude:** cada `/crear-articulo` invoca 4 subagentes + WebFetch. A 10 artículos/día/redactor × N redactores, validar consumo en Fase 1 con un redactor para extrapolar. Si excede plan, evaluar `model: claude-haiku-*` para `product-researcher` y `editor-in-chief` (tareas más mecánicas).
- **Riesgo en estado del proyecto compartido:** OneDrive puede generar duplicados (`archivo (1).md`) si dos redactores editan a la vez. Mitigación: convención de propiedad por medio + Fase 1 monousuario.

## Acceptance Criteria

### Funcionales (mapeo a R1-R7 del origen)

- [ ] **R1.** `/crear-articulo` acepta una URL como argumento obligatorio y arranca la pipeline sin requerir más metadatos.
- [ ] **R2.** Si no se da medio, `/crear-articulo` muestra los medios disponibles (leídos de `guidelines/`) y pide elegir.
- [ ] **R3.** La pipeline produce un único markdown final en `drafts/{medio}/`. La pausa interactiva del ángulo está activa y el redactor puede confirmar, elegir otro de la lista, o dictar uno propio.
- [ ] **R4.** `/crear-guideline` produce o actualiza un `GUIDELINE-{medio}.md` válido contra el schema, sin requerir intervención técnica.
- [ ] **R5.** Los subagentes leen `knowledge/` cuando aporta (writer consulta `ejemplos-publicados/{medio}`, editor consulta `politicas-afiliacion.md`, todos respetan `frases-vetadas.md`).
- [ ] **R6.** El draft final contiene frontmatter completo (medio, url_origen, asin si aplica, fecha, angulo, estado) y se guarda en `drafts/{medio}/{fecha}-{slug}.md`.
- [ ] **R7.** Un redactor sin experiencia previa con Claude Code completa el flujo end-to-end siguiendo `docs/onboarding-redactores.md` sin intervención técnica adicional.

### No funcionales

- [ ] Tiempo de pipeline end-to-end (sin contar la pausa humana) ≤ 5 minutos por artículo en condiciones normales.
- [ ] Si `WebFetch` falla, el agente pide los datos al redactor de forma clara, sin abortar la sesión.
- [ ] Permisos en `.claude/settings.json` están afinados para no generar prompts de permiso durante el flujo normal.

### Quality gates

- [ ] Champion ha producido ≥ 5 artículos publicables (revisión ligera) consecutivos.
- [ ] Tiempo medio de redactor por artículo (validar oferta + revisar markdown) menor que el flujo actual con GPT personalizado.
- [ ] `docs/onboarding-redactores.md` ha sido leído y seguido por un redactor real distinto al champion sin ayuda.

## Success Metrics

(carry from origin)

- ≥ 80% de markdowns generados se publican con edición ligera.
- Adopción medida en uso semanal real, no en demos.
- Si tras 3 semanas un redactor sigue exclusivamente con el GPT antiguo, se entrevista para identificar fricción concreta antes de presionar.

## Dependencies & Risks

- **Riesgo 1 — Bloqueo antibot Amazon en `WebFetch`.** Probabilidad media. Mitigación: degradación graceful (pedir ficha al redactor); en Fase 4, evaluar MCP Playwright si recurrente.
- **Riesgo 2 — Voz del medio mal capturada en la guideline.** Probabilidad media-alta al inicio. Mitigación: `/importar-gpt` para arrancar desde las instrucciones del GPT existente; iteración con champion antes de generalizar; ejemplos publicados en `knowledge/` como anclaje de estilo.
- **Riesgo 3 — Repetición del fracaso de adopción.** Probabilidad real. Mitigación: champion-first con métrica binaria por artículo, kill-switch a las 3 semanas si no hay adopción real, sin construir Fase 2 en paralelo.
- **Riesgo 4 — Coste API descontrolado a escala.** Probabilidad baja-media. Mitigación: medir en Fase 1 con un solo redactor; modelo Haiku para subagentes mecánicos si excede.
- **Riesgo 5 — Conflictos en OneDrive con múltiples editores.** Probabilidad baja en Fase 1-2 (un solo champion), media en Fase 3. Mitigación: convención de propiedad por medio + migración a Git si se materializa.
- **Dependencia clave — Plan Claude del redactor.** Cada redactor necesita una cuenta Claude con plan que soporte uso diario de subagentes. Validar antes de Fase 3.
- **Dependencia clave — Champion disponible.** Sin un redactor dispuesto a ser primer usuario y co-iterar, Fase 1 no arranca.

## Outstanding Questions (post-planning)

- **[Operacional]** ¿Quién es el champion concreto y desde cuándo está disponible? Sin nombre + agenda, Fase 1 es una intención, no un plan.
- **[Producto]** ¿Cuántos medios están en alcance Fase 2? Determina cuántas guidelines hay que producir.
- **[Técnico]** Validar en una sesión corta que `WebFetch` funciona contra una muestra representativa de URLs de Amazon España y AliExpress antes de dar Phase 1 por viable.
- **[Decisión producto]** Naming exacto de los medios (slugs) para `GUIDELINE-{medio}.md` y `drafts/{medio}/` — necesita confirmación del usuario o del champion.

## Sources & References

### Origin

- **Origin document:** [docs/brainstorms/2026-05-08-agentes-redactores-ofertas-requirements.md](../brainstorms/2026-05-08-agentes-redactores-ofertas-requirements.md). Decisiones clave carry-forward: patrón thruuu como base, reemplazo de GPTs por GUIDELINE.md por medio, input por URL pegada (no descubrimiento), usuario directo redactor vía app Claude, sin control de duplicados en MVP, diseño extensible a SEO long-form.

### Internal references

- Proyecto previo (espejo de qué evitar): `C:\Users\andre\proyectos-IA\Proyecto analizador de ofertas` — replanteamiento del 23/04/2026 confirma que solo se usaba el listado.
- Estructura inspiradora: [github.com/thruuu/thruuu-claude-writer](https://github.com/thruuu/thruuu-claude-writer).

### External references

- Subagentes en Claude Code: [code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents).
- Skills (slash commands): [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills) — especial atención a `disable-model-invocation`, `argument-hint`, `$ARGUMENTS`, `context: fork`, `!\`comando\`` para inyección dinámica.
- Walkthrough conceptual: [thruuu.com/blog/seo-content-agent-claude-code](https://thruuu.com/blog/seo-content-agent-claude-code/).

### Related work

- N/A — proyecto greenfield.

---

## Refinamientos cross-plan (2026-05-08)

Sección añadida tras analizar el plan hermano `Informes Google Ads, GSC y DataforSEO/docs/plans/2026-05-08-001-feat-meta-sistema-skills-informes-plan.md` (que ya pasó por `/deepen-plan` con 5 agentes de revisión). Recoge los patrones operativos de ese plan que aplican a este dominio, **excluyendo explícitamente los hooks de Claude Code** (Stop / SessionStart): se difieren a una fase posterior si el uso real demuestra que los checklists del editor-in-chief no son suficientes.

### 1. Inventario `medios.md` (complemento, no sustitución)

Añadir `medios.md` en raíz del proyecto como **tabla maestra de medios** con datos estructurales:

| Medio | Tipo | Tono | Longitud | Disclaimer afiliación | Última publicación | Estado guideline |
|---|---|---|---|---|---|---|
| medio-A | Ofertas | Cercano-experto | 600-1000 | Primer párrafo | 2026-05-07 | v3 |

**Convive con la Outstanding Question existente** sobre naming/slugs de medios — no la cierra. La Outstanding Question sigue siendo válida (necesita confirmación del usuario/champion sobre slugs exactos); `medios.md` es el **artefacto que materializa la respuesta** cuando llegue, y mientras tanto se va poblando incrementalmente conforme se crean GUIDELINEs.

**Qué no contiene:** narrativa de voz/estilo (eso vive en `GUIDELINE-{medio}.md`), KPIs editoriales, ejemplos. Solo el "qué medios existen y en qué estado".

**Mantenimiento:** se actualiza al crear/actualizar guideline (campo "Estado guideline") y al publicar artículo (campo "Última publicación"). Regla operativa en `CLAUDE.md`.

### 2. Drift checker: `docs/guidelines-check.py`

Script de verificación que cruza estado real vs documentado:

- Medios con drafts en `drafts/{medio}/` pero sin `GUIDELINE-{medio}.md`
- Medios con guideline pero sin `knowledge/ejemplos-publicados/{medio}/`
- Frases vetadas globales (`knowledge/frases-vetadas.md`) duplicadas literalmente dentro de algún GUIDELINE (señala oportunidad de convertir en puntero)
- Filas en `medios.md` sin guideline correspondiente y viceversa

Output legible: `[OK] 3 medios consistentes | [WARN] medio-X tiene drafts sin guideline`. Se ejecuta manualmente; **sin hook automático en MVP** (decisión explícita).

Evita el anti-patrón "documentación que se pudre": el plan hermano lo identificó como riesgo principal de los registries.

### 3. Regla de capas explícita entre subagentes

Documentar en `CLAUDE.md` la jerarquía de inputs por subagente como **regla arquitectónica con justificación**:

```
product-researcher → URL + WebFetch                              (NO lee guideline ni ejemplos)
angle-picker       → ficha + GUIDELINE                           (solo metadatos editoriales)
writer             → ficha + ángulo + GUIDELINE + ejemplos       (lectura completa)
editor-in-chief    → draft + GUIDELINE + frases-vetadas + afiliación
```

**Razón:** evita que el `writer` "alucine" datos del producto modificando la ficha (la ficha es contrato inmutable tras product-researcher), y evita que el `product-researcher` se sesgue por el ángulo editorial antes de extraer hechos. Cada agente declara en su frontmatter `tools` solo lo que necesita para cumplir su capa.

**Acceptance criterion nuevo:** revisar el frontmatter de cada subagente y confirmar que sus `tools` no permiten leer fuera de su capa.

### 4. Golden samples por medio como gate Fase 1 → Fase 2

Antes de cerrar Fase 1 (champion único), capturar **fixtures inmutables** que sirvan como detector de regresión silenciosa al iterar prompts:

- 3 URLs reales → ficha esperada del `product-researcher` (snapshot markdown)
- 3 (ficha + medio) → ángulo elegido por `angle-picker` + justificación
- 3 drafts publicables como referencia visual

Cuando en Fase 2 o Fase 4 se ajusten prompts de subagentes, se rerunnea contra estas entradas y se compara. Si el draft cambia estructuralmente, alerta antes de propagar la regresión a varios medios.

Es la versión técnica del criterio "calidad ≥ flujo actual" que el plan ya pide pero deja en evaluación humana — añade un suelo objetivo y barato.

### 5. Auto-mantenimiento de `GUIDELINE-{medio}.md` durante uso real

Hoy las guidelines solo se actualizan vía `/crear-guideline` o `/importar-gpt`. Pero el champion descubrirá micro-reglas no escritas durante el uso real ("este medio nunca usa paréntesis en H2", "el disclaimer va siempre en cursiva", "evitan la palabra 'imperdible'").

**Bloque "Antes de cerrar" en `/crear-articulo`** (3 líneas, formato checklist al final del flujo):

```markdown
## Antes de cerrar
- ¿Editaste el draft tras el editor-in-chief? Si hay un patrón nuevo → añadir a `GUIDELINE-{medio}.md`.
- ¿La ficha del producto vino incompleta? → registrar el dominio/patrón en notas de degradación.
- ¿Confirmas que `medios.md` refleja la última publicación?
```

Convierte el uso real en aprendizaje persistente del sistema, no solo en outputs desechables.

### 6. "Prefer pointers to copies" en frases vetadas

**Cambio en el schema de `GUIDELINE-{medio}.md`:** la sección "Frases vetadas" deja de ser una lista plana y pasa a ser:

```markdown
## Frases vetadas
- **Globales:** ver `knowledge/frases-vetadas.md` (no duplicar aquí).
- **Adicionales de este medio:**
  - [...]
```

Reduce mantenimiento (la lista global se actualiza una vez), evita drift entre medios, y deja explícito qué es transversal vs específico. El `editor-in-chief` lee ambas fuentes.

Aplica el principio "prefer pointers to copies" del plan hermano: `CLAUDE.md` como punto único de verdad, guidelines como pointers/extensiones.

### 7. Excepciones tipadas para degradación graceful

Formalizar los modos de fallo del flujo como estados conocidos en lugar de "el agente improvisa":

- `URLBlockedError` (antibot) → `product-researcher` pide al redactor pegar ficha o screenshot
- `GuidelineMissingError` → `/crear-articulo` redirige a `/crear-guideline` antes de continuar
- `AmbiguousAngleError` (confianza baja) → `angle-picker` fuerza la pausa interactiva con 3 opciones explícitas en lugar de elegir y dejar al redactor reaccionar

Esto formaliza el "WebFetch falla → pedir ficha" que ya está en el plan, lo extiende a otros puntos de fallo, y le da al redactor mensajes consistentes en lugar de respuestas improvisadas por subagente.

### 8. Métricas como escenarios de regresión concretos

El plan hermano sustituyó "<1 min sesión nueva" por un escenario de regresión concreto. Aplicación aquí:

**Complementar** "≥ 80% de markdowns generados se publican con edición ligera" (que es síntoma agregado y difícil de accionar) con escenarios **reproducibles**:

- *Escenario A:* dado URL X de Amazon, medio Y, ángulo Z confirmado → draft pasa al `editor-in-chief` sin cambios estructurales (solo edición de superficie).
- *Escenario B:* dado URL bloqueada → `product-researcher` muestra mensaje claro y el flujo se pausa esperando input, no aborta.
- *Escenario C:* dado medio sin guideline → `/crear-articulo` redirige a `/crear-guideline`.

Si a las 3 semanas un escenario falla, hay un punto concreto donde mirar (qué subagente, qué prompt) en lugar de un porcentaje agregado.

### Cortes explícitos respecto al plan hermano (qué NO trasplantamos)

| Elemento del plan hermano | Decisión aquí | Razón |
|---|---|---|
| Stop / SessionStart hooks | ❌ no en MVP | El editor-in-chief cubre validación end-of-pipeline; añadir hooks ahora es complejidad prematura. Reevaluar en Fase 4 si la disciplina del agente flojea. |
| Tests unitarios para módulos puros | ❌ no aplica | No hay módulos puros equivalentes a `format_es.py`. Los goldens (#4) cubren mejor el dominio textual. |
| Empaquetado formal (`pyproject.toml`) | ⏸ diferido | Solo relevante si Fase 4 SEO long-form introduce código Python compartido. Anotar como decisión a tomar al entrar en esa fase. |
| Drift checker como hook automático | ⏸ ejecución manual | Ver corte #1: sin hooks en MVP. El script existe (#2), se invoca a mano. |

### Acceptance criteria adicionales

- [ ] Existe `medios.md` en raíz con tabla maestra; convive con la Outstanding Question sobre slugs sin reemplazarla.
- [ ] Existe `docs/guidelines-check.py` que reporta drift y se puede ejecutar manualmente.
- [ ] La regla de capas entre subagentes está documentada en `CLAUDE.md` y los `tools` de cada subagente la respetan.
- [ ] Antes de cerrar Fase 1, hay 3 golden samples capturados (ficha, ángulo, draft) por el medio piloto.
- [ ] El bloque "Antes de cerrar" de 3 líneas está al final de `/crear-articulo`.
- [ ] El schema de `GUIDELINE-{medio}.md` separa "Frases vetadas globales (puntero)" de "Adicionales de este medio".
- [ ] Los modos de fallo del flujo están listados en `CLAUDE.md` como estados conocidos con respuesta definida (URLBlocked, GuidelineMissing, AmbiguousAngle).

### Tiempo estimado adicional

- `medios.md` inicial (vacío + plantilla): 15 min
- `docs/guidelines-check.py`: 30-45 min
- Documentar regla de capas en `CLAUDE.md` + ajustar `tools` de subagentes: 30 min
- Bloque "Antes de cerrar" + ajuste schema GUIDELINE (pointers): 20 min
- Excepciones tipadas en prompts de subagentes: 30 min
- Captura de goldens (al cerrar Fase 1, no al iniciarla): 1 h
- **Total adicional: ~3 h** distribuidas a lo largo de Fase 1 y Fase 2.

### Referencias

- Plan hermano: `Informes Google Ads, GSC y DataforSEO/docs/plans/2026-05-08-001-feat-meta-sistema-skills-informes-plan.md` — sección "Refinamientos tras /deepen-plan (2026-05-08)".
