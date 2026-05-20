# Plan: soporte multi-producto y guías de compra en `/crear-articulo`

**Fecha:** 20/05/2026
**Autor:** Sistema (orquestador) + redactor
**Estado:** en implementación

---

## Problema

Cuando el redactor quiere hacer una **guía de compra** o un **artículo longtail con varios productos** (p. ej. tres tablets que comparar, un recopilatorio de ofertas de Amazon, una guía top-5 de smartwatches por presupuesto), el sistema actual asume que cada URL es un artículo independiente y produce N piezas separadas en lugar de **un artículo único multi-producto**.

Esto rompe el flujo del redactor para los formatos:

- Comparativa de 2-N productos del mismo tipo.
- Recopilatorio de ofertas con hilo común.
- Top-N de una categoría.
- Guía por presupuesto o por caso de uso.
- Longtail de marca (catálogo destacado de una marca).

Las tres guidelines ya tienen rastros de soporte multi-producto (Mundo Deportivo distingue `layout: mono-producto` y `multi-producto`; ABC define `modo: recopilatorio` y `longtail-marca`; La Razón distingue mono y multi en la sección "Longitud orientativa") pero **no hay una ruta limpia en el comando** que detecte el escenario, pregunte al redactor y empuje el flujo correcto.

---

## Solución (alto nivel)

1. **Detectar al inicio del flujo** cuántas URLs ha pegado el redactor.
2. **Si hay 1 URL**, comportamiento actual (flujo mono-producto). Sin pregunta extra.
3. **Si hay 2+ URLs**, pausa interactiva nueva con tres opciones:
   - **A)** Una guía/comparativa con todos los productos juntos → flujo **multi-producto** (nuevo).
   - **B)** N artículos separados → ejecutar el flujo mono uno a uno.
   - **C)** Solo uno → el redactor elige cuál y se descarta el resto.
4. En el flujo multi se introduce un nuevo concepto: **`FORMATO_GUIA`**.
5. Cada guideline declara qué `FORMATO_GUIA` admite y cómo se renderiza internamente.

---

## Variables y conceptos nuevos

### `TIPO_ARTICULO`

| Valor | Significado |
|---|---|
| `mono` | 1 producto, 1 artículo. Flujo actual. |
| `multi` | N productos, 1 artículo. Nuevo. |

### `FORMATO_GUIA` (solo cuando `TIPO_ARTICULO=multi`)

Catálogo universal, traducido por cada guideline a sus layouts/modos internos:

| Slug | Descripción universal | Cuándo usarlo |
|---|---|---|
| `comparativa` | 2-N productos del mismo tipo enfrentados. | "Cuál ganaría entre X y Y", "X vs Y vs Z". |
| `recopilatorio` | Lista de ofertas con hilo común (categoría, momento, tienda). | "10 chollos de Amazon hoy", "Las mejores rebajas en zapatillas esta semana". |
| `top-n` | Ranking de los mejores N en una categoría. | "Los 5 mejores smartwatches 2026". |
| `por-presupuesto` | N productos organizados por franjas de precio. | "Tres robots aspirador a 100€, 200€ y 400€". |
| `por-uso` | N productos organizados por casos de uso o perfiles. | "Auriculares según uses gym, oficina o viajes". |
| `longtail-marca` | Catálogo destacado de una marca. | "Por qué Garmin sigue siendo la marca de referencia: estos 4 modelos lo demuestran". |

Cada guideline mapea estos slugs a sus convenciones internas (`layout: multi-producto` en Mundo Deportivo y La Razón; `modo: recopilatorio` / `modo: longtail-marca` en ABC).

---

## Cambios por archivo

### 1. `.claude/skills/crear-articulo/SKILL.md`

**Paso 2.5 NUEVO — Detección y bifurcación multi-producto.** Justo después del `GuidelineMissingError` check (Paso 2):

- Cuenta URLs en `$ARGUMENTS` (admite varias separadas por espacios o saltos de línea).
- Si **1 URL** → `TIPO_ARTICULO=mono`, continúa al Paso 3 sin pregunta.
- Si **2+ URLs** → pausa interactiva con las tres opciones (A: guía única / B: artículos separados / C: solo uno).
- Si elige A → asigna `TIPO_ARTICULO=multi`. Pregunta por `FORMATO_GUIA` filtrado por lo que admite la guideline del medio.
- Si elige B → ejecuta el flujo mono iterativamente, uno por URL.
- Si elige C → pide cuál y se queda con esa URL.

**Paso 3 — product-researcher en lote.** Si `TIPO_ARTICULO=multi`, invocar `product-researcher` **N veces en paralelo**, una por URL. Recolectar la lista de fichas como `FICHAS_PRODUCTOS`. Si alguna URL bloquea, presentar el `URLBlockedError` por URL y seguir con las que sí han funcionado o con los datos manuales que pegue el redactor.

**Paso 4 — angle-picker para multi.** En `TIPO_ARTICULO=multi`, el angle-picker recibe `FICHAS_PRODUCTOS` (lista) + `FORMATO_GUIA` + medio y propone el **ángulo editorial global** (uno solo para todo el artículo, no por producto). El formato ya está fijado por la pausa anterior; el angle-picker puede sugerir reconsiderarlo si detecta un mejor encaje.

**Paso 6 — headline-generator multi.** Recibe `FICHAS_PRODUCTOS` + `FORMATO_GUIA` + ángulo + medio. Genera 30 titulares calibrados para guías (templates específicos: "X productos que…", "Los 5 mejores…", "Comparamos X y Y…").

**Paso 8 — writer multi.** Aplica la plantilla multi-producto definida en la guideline. Cada guideline detalla cómo se estructura su multi (qué anclajes obligatorios, qué bloques por producto, longitud objetivo).

**Paso 9 — editor-in-chief multi.** Checklist con puntos adicionales para multi: hilo conductor coherente, cada producto cumple su mini-ficha, no se repiten patrones de prosa entre bloques, recetas globales aplicadas una sola vez, etc.

### 2. `.claude/agents/product-researcher.md`

Sin cambios estructurales. Se documenta explícitamente que **el orquestador puede invocarlo en paralelo** cuando hay N URLs.

### 3. `.claude/agents/angle-picker.md`

- Nueva sección "Modo multi-producto": cómo razonar el ángulo cuando hay N fichas.
- Output enriquecido en multi: además del ángulo, una línea sobre el **hilo conductor** que va a sostener el artículo.

### 4. `.claude/agents/headline-generator.md`

- Nueva sección "Modo multi-producto / guía de compra": fórmulas de titular específicas para guías (recopilatorios, comparativas, tops, etc.).
- La distribución de estilos puede flexibilizarse en multi (algunos estilos como `review-rapida` o `primera-persona` encajan peor; otros como `seo`, `oferta-directa`, `comparativa` y `uso-concreto` cogen más peso).

### 5. `.claude/agents/writer.md`

- Nueva sección "Modo multi-producto": cómo aplicar la plantilla multi del medio. Recibe `FICHAS_PRODUCTOS` (lista) + `FORMATO_GUIA`.
- Reglas duras: cada bloque de producto debe arrancar con marca, no copiar la misma fórmula de un bloque al siguiente, los precios siguen las mismas reglas relativas que en mono.

### 6. `.claude/agents/editor-in-chief.md`

- Checklist ampliado con bloque "Verificaciones específicas de multi-producto" (longitud por bloque, marca presente en cada bloque, hilo conductor identificable, no repetición de cierres por bloque).

### 7. Guidelines (las tres)

- **`GUIDELINE-larazon.md`** — Sección "Multi-producto" desarrollada: anclajes específicos, longitud por bloque, qué `FORMATO_GUIA` admite, plantilla por bloque de producto.
- **`GUIDELINE-mundodeportivo.md`** — Ya tiene `layout: multi-producto`. Añadir el mapeo `FORMATO_GUIA` → estructura interna y qué formatos admite.
- **`GUIDELINE-abc.md`** — Ya tiene `modo: recopilatorio` y `modo: longtail-marca`. Añadir el mapeo `FORMATO_GUIA` → `modo` y qué formatos admite.

### 8. `CLAUDE.md` y `README.md`

- Documentar la nueva capacidad multi-producto.
- Actualizar la sección de arquitectura del flujo (regla de capas se mantiene; se añade que cada capa puede operar en modo mono o multi según una variable).

### 9. `medios.md`

- Columna nueva "Formatos guía soportados" o nota inline por medio.

### 10. Changelog

- Entrada nueva con fecha 20/05/2026 documentando el cambio.

---

## Tareas

- [x] Diseño y plan (este documento).
- [ ] Actualizar `SKILL.md` con detección multi-producto, pausa interactiva y `FORMATO_GUIA`.
- [ ] Actualizar `product-researcher.md` con nota de paralelización en lote.
- [ ] Actualizar `angle-picker.md` con modo multi.
- [ ] Actualizar `headline-generator.md` con modo multi.
- [ ] Actualizar `writer.md` con modo multi.
- [ ] Actualizar `editor-in-chief.md` con checklist multi.
- [ ] Desarrollar sección multi-producto en `GUIDELINE-larazon.md`.
- [ ] Mapear `FORMATO_GUIA` → layouts en `GUIDELINE-mundodeportivo.md`.
- [ ] Mapear `FORMATO_GUIA` → modos en `GUIDELINE-abc.md`.
- [ ] Actualizar `CLAUDE.md` y `README.md`.
- [ ] Actualizar `medios.md` con formatos guía soportados.
- [ ] Entrada de changelog 20/05/2026.
- [ ] Commit y push a GitHub.

---

## Riesgos y decisiones tomadas

- **No se cambia la regla de capas** entre subagentes. Cada capa sigue operando sobre el mismo set de fuentes; solo se amplía la cardinalidad de la entrada (1 ficha → N fichas) y se introduce la variable `FORMATO_GUIA`.
- **No se rompe el flujo mono actual.** Si el redactor pega 1 URL, no recibe ninguna pregunta nueva y el sistema se comporta exactamente como antes.
- **No se inventan datos cruzados entre productos.** En comparativas, si una spec de un competidor no está en la ficha, no se infiere; se trabaja solo con lo extraído.
- **La opción B (artículos separados) podría implementarse como N invocaciones secuenciales del flujo mono.** En esta primera versión se ofrece como recordatorio al redactor para que lance N llamadas a `/crear-articulo`; iterar internamente queda como mejora futura.
