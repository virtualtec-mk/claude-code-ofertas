# Plan de mejoras: titulares, voz humana y peso del "cuando-no-comprarlo"

- **Fecha:** 19/05/2026
- **Origen:** Sesión de prueba del flujo `/crear-articulo` con La Razón (Blink Outdoor 2K+, pack 3 cámaras).
- **Síntomas detectados por el redactor:**
  1. El titular lo tuvo que aportar él. El sistema solo ofrecía tentativo + alternativo, sin variedad real.
  2. La redacción no suena humana. El writer no usa los ejemplos publicados ni la voz del GPT v1 de La Razón.
  3. El artículo sobrepondera "por qué no comprar". El H2 `cuando-no-comprarlo` ocupa ~25% del cuerpo en una oferta de liquidación.

- **Orden de ejecución acordado:** 3 → 2 → 1.

---

## Bloque 3 — Corregir el mapa de recetas (rápido, arregla el artículo actual)

### Diagnóstico
`GUIDELINE-larazon.md:96` y `GUIDELINE-mundodeportivo.md:155` definen ambos:

```
| `liquidacion` | `contexto-de-mercado` + `cuando-no-comprarlo` |
```

El angle-picker lo siguió al pie de la letra y el writer lo materializó como H2 propio. El resultado en una oferta agresiva descompensa el artículo: el precio queda enterrado bajo un "ojo con esto antes de comprar".

### Acciones

1. **Editar `guidelines/GUIDELINE-larazon.md`:**
   - Línea 96 (mapa): `liquidacion` → `contexto-de-mercado` + `vision-de-marca`. Mantener `cuando-no-comprarlo` como **receta opcional**, no automática.
   - Sección "Recetas disponibles" → en `cuando-no-comprarlo`: añadir aclaración de que, en ángulos donde el precio es la noticia (`liquidacion`, `precio-psicologico`), se aplica como matiz integrado en otra receta (1-2 frases), no como H2 propio. El H2 propio se reserva a `recomendacion-personal` y reviews largos.
   - Sección "Reglas de uso del cuerpo libre" → añadir bala: *"En `liquidacion`, los contras se integran como una frase corta dentro de otra receta. Nunca como sección propia."*

2. **Editar `guidelines/GUIDELINE-mundodeportivo.md`:** mismos cambios en las líneas equivalentes (155 y descripción de `cuando-no-comprarlo`).

3. **Regenerar el artículo actual de La Razón** (`drafts/larazon/20260519-mas-ojos-fuera-de-casa-blink-2k.md`) con las nuevas reglas:
   - Eliminar el H2 "Cuándo no tiene sentido comprarlo".
   - Reducir el matiz de la suscripción a una frase integrada en `contexto-de-mercado` o en el nuevo H2 de specs.
   - Sustituir la receta `cuando-no-comprarlo` del frontmatter por `vision-de-marca` (o `specs-traducidas`).
   - Mantener el titular dictado por el redactor.

### Resultado esperado
El artículo recupera el peso del precio como noticia. La honestidad transaccional se mantiene como frase, no como sección. El mapa deja de empujar a un patrón compositivo desequilibrado.

---

## Bloque 2 — Voz humana, ejemplos publicados y limpieza del writer

### Diagnóstico
1. `knowledge/ejemplos-publicados/larazon/` está vacío. La guideline lista URLs pero ningún ejemplo en local. El writer redacta sin material humano de referencia.
2. `.claude/agents/writer.md` (paso 3) tiene un bloque propio de "tratamiento por ángulo" que **compite** con las recetas y con el GPT v1. Tres fuentes potencialmente contradictorias.
3. El **GPT v1** original de La Razón está enterrado en un `<details>` marcado como "ya no normativo". Si la voz humana del GPT es lo que se quiere preservar, hoy no manda.
4. No existe checklist anti-tono-IA aplicado por el writer antes de guardar.

### Acciones

1. **Descargar ejemplos publicados a local:**
   - Crear `knowledge/ejemplos-publicados/larazon/` (si no existe).
   - Por cada URL listada en el frontmatter de `GUIDELINE-larazon.md`, fetchear el artículo con Playwright MCP y guardarlo como `.md` con frontmatter mínimo (título, URL, fecha de publicación).
   - Replicar para `mundodeportivo` (4 URLs en su guideline).

2. **Limpiar `.claude/agents/writer.md`:**
   - Eliminar el bloque "Cada ángulo tiene un tratamiento diferente" del paso 3 (líneas ~60-72). Esta normativa se duplica con la paleta de recetas y crea ruido.
   - Dejar la guideline del medio como **única fuente** de tratamiento por ángulo (vía recetas).
   - Añadir referencia explícita a que el writer DEBE leer los ejemplos publicados si existen.

3. **Decidir el peso del GPT v1 de La Razón:**
   - Opción recomendada: **B — extraer las pautas de voz vivas del GPT v1** (Reglas de Oro, registro, fórmulas) y subirlas a primer plano de la guideline. Dejar el resto del prompt en `<details>` como referencia histórica.
   - Alternativa: Opción A — declarar el GPT v1 normativo y reconciliarlo con el modelo v2 de recetas. Más invasivo.

4. **Añadir un mini-pase de auto-revisión "anti-IA" al writer** (paso 7 nuevo, antes de guardar):
   - Checklist corto en el agent: conectores explicativos típicos de IA ("lo que en términos cotidianos significa", "que es exactamente lo que…", "no solo X sino también Y"), traducción mecánica de specs ("X gramos → ligera para llevar"), frases-resumen de cierre de párrafo.
   - El writer reescribe localmente cualquier coincidencia antes del Write final.

### Resultado esperado
El writer trabaja con material humano real (ejemplos publicados) en lugar de inventar voz. La guideline manda sin competencia de instrucciones internas del agent. Las frases-puente típicas de IA se filtran antes de llegar al editor.

---

## Bloque 1 — Sistema de titulares multi-candidato

### Diagnóstico
- `angle-picker.md` entrega 1 titular tentativo + 1 alternativo. Sin variedad real.
- No existe manual de fórmulas de titulares.
- La pausa interactiva del skill (Paso 5) ofrece A/B/C/D abstractos, no candidatos concretos.

### Acciones

1. **Crear `knowledge/headline-recipes.md`:**
   - Fórmulas globales reutilizables: factual descuento, cita entrecomillada + dos puntos, beneficio cotidiano + cifra, pregunta retórica, comparativa rápida, urgencia honesta.
   - Límites de caracteres por canal (Discover ~70-95, Twitter ~90).
   - Lista corta de verbos preferidos por movimiento de precio (rebaja, desploma, pone, baja, hunde, deja).
   - Patrones que NO usar (clickbait, "no creerás", "atención", exclamaciones).

2. **Añadir bloque "Recetas de titular preferidas" a cada `GUIDELINE-{medio}.md`:**
   - Por medio: 2-3 fórmulas del manual global que mejor encajan con su voz, con un ejemplo real publicado al lado.

3. **Cambiar el output del `angle-picker`:**
   - Generar **4 candidatos de titular**, etiquetando cada uno con la fórmula usada.
   - Cada candidato lleva: titular, fórmula aplicada, longitud en caracteres.
   - El campo "titular alternativo" actual desaparece (lo reemplaza la lista).

4. **Editar el skill `crear-articulo` (Paso 5):**
   - Mostrar los 4 candidatos numerados.
   - Opciones: elegir uno tal cual, editar uno, dictar otro, pedir 3 candidatos nuevos.

### Resultado esperado
El redactor recibe 4 titulares variados antes de cualquier pausa manual. Solo dicta si ninguno le convence, no como vía por defecto.

---

## Riesgos y notas

- Los cambios al mapa de recetas tienen efecto inmediato en todo nuevo artículo. Drafts existentes no se tocan automáticamente.
- Si se baja el GPT v1 a primer plano y entra en conflicto con alguna receta v2, gana la guideline v2 por compatibilidad con el editor-in-chief (que valida por recetas).
- Los ejemplos publicados son contenido de terceros. Se guardan solo como referencia interna, nunca se republican.

## Done criteria

- Bloque 3: artículo de Blink regenerado sin H2 `cuando-no-comprarlo`. Mapas de ambas guidelines actualizados.
- Bloque 2: 3 ejemplos de La Razón + 4 de Mundo Deportivo guardados en `knowledge/ejemplos-publicados/`. Writer.md limpio. Guideline de La Razón con pautas del GPT v1 visibles. Checklist anti-IA en el writer.
- Bloque 1: `headline-recipes.md` creado, ambas guidelines actualizadas, angle-picker entregando 4 candidatos, Paso 5 del skill rediseñado.
