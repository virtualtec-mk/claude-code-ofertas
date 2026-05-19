# HANDOFF — Pruebas guidelines v2 (paleta de recetas)

Documento de traspaso entre sesiones de Claude Code. Si eres el Claude que abre por primera vez este proyecto, lee esto entero antes de empezar.

---

## Quien soy y donde estoy

- **Proyecto:** `claude-code-writer-pruebas` (rama `feat/guidelines-v2-paleta-recetas`).
- **Es una copia de:** `git@github.com:virtualtec-mk/claude-code-writer.git`. Esto es un sandbox local para iterar sin tocar `master` ni el repo de produccion.
- **Usuario:** Javi. Castellano sin tildes en conversacion. Es profesional de contenidos, **no programador**: explicale las cosas sin jerga.

---

## Que se cambio en este branch

Hay 4 archivos modificados respecto a `master`:

1. **`guidelines/GUIDELINE-larazon.md`** — Reescritura mayor.
2. **`guidelines/GUIDELINE-mundodeportivo.md`** — Reescritura mayor.
3. **`.claude/agents/writer.md`** — Ajustes quirurgicos.
4. **`.claude/agents/editor-in-chief.md`** — Ajustes quirurgicos.

### El cambio conceptual

En v1 la guideline definia una **estructura fija** (titular → bajada → intro → H2 marca-beneficio → H2 para-quien-es → cierre → disclaimer) y todos los articulos salian iguales.

En v2 la guideline define:

- **Anclajes fijos** (siempre, en orden): titular, bajada, introduccion, primer H2 del cuerpo, disclaimer/cierre obligatorio del medio.
- **Paleta de 10 recetas** para el cuerpo libre entre el primer H2 y el cierre.
- **Mapa orientativo angulo → recetas tipicas** (sugerencia, no ley).
- Reglas de uso: el writer elige **1-3 recetas**, no repite, justifica internamente en una linea, y declara las recetas elegidas en el frontmatter (`recetas: [...]`).

### Las 10 recetas (universales)

`specs-traducidas`, `para-quien-si-para-quien-no`, `comparativa-corta`, `contexto-de-mercado`, `microhistoria-de-uso`, `cuando-no-comprarlo`, `faq-corta`, `vision-de-marca`, `momento-cultural`, `truco-de-experto-integrado` (este ultimo NO cuenta como receta — se integra dentro de otra).

mundodeportivo tiene ademas una receta firma del medio: `criterios-el-recomendador`.

Cada receta esta descrita con 2-3 lineas en la propia guideline para que sea facil de entender al leer.

### Cambios en agentes

- **writer.md:** ya no debe "replicar estructura EXACTA de la guideline". Ahora debe elegir layout + anclajes + recetas, y justificar en una linea por que esas recetas. El frontmatter del draft incluye dos campos nuevos: `recetas: [lista]` y `layout: mono-producto | multi-producto` (solo si la guideline distingue layouts).
- **editor-in-chief.md:** el check #2 ahora valida (a) anclajes fijos presentes y en orden, (b) coherencia entre recetas declaradas en frontmatter y contenido del cuerpo. **No valida orden ni numero de H2 del cuerpo libre.** El check #6 del frontmatter incluye los campos nuevos `recetas` y `layout`.

---

## Como probar (lo que toca ahora)

### Comando

```
/crear-articulo larazon <URL_amazon_o_aliexpress>
```

o

```
/crear-articulo mundodeportivo <URL>
```

### IMPORTANTE: guardar en `pruebas/` no en `drafts/`

El SKILL.md original guarda los drafts en `drafts/{medio}/`. **Para esta fase de validacion**, los drafts generados deben ir a `pruebas/{medio}/` (esta misma carpeta), no a `drafts/`. Cuando ejecutes `/crear-articulo`, sustituye la ruta del Paso 6 del skill (writer) por `pruebas/{medio}/{fecha}-{slug}.md`. Mismo nombre de archivo, distinta carpeta raiz.

Si Javi olvida pedirlo, recuerdaselo antes de invocar al writer.

### Playwright

El plugin Playwright MCP esta instalado globalmente. En esta sesion nueva deberian estar disponibles las tools `browser_navigate`, `browser_snapshot`, `browser_wait_for`, `browser_take_screenshot`, `browser_close`. Si no aparecen al intentar usarlas, ejecuta `/plugins` para verificar que esta activo.

### Que evaluar en cada draft

Cuando salga el primer draft, lo importante NO es si la prosa es perfecta — es si **el sistema esta usando la paleta de verdad** o si vuelve a caer en el esqueleto fijo de v1. Cosas a comprobar:

1. **Frontmatter:** ¿el campo `recetas` esta presente y tiene 1-3 entradas validas?
2. **Cuerpo libre:** ¿los H2 entre el primer H2 y el cierre se corresponden con las recetas declaradas?
3. **Variabilidad:** si haces dos `/crear-articulo` seguidos con productos del mismo medio pero distinto angulo, **¿salen articulos con formas distintas?** Si los dos terminan con el mismo esqueleto, algo va mal.
4. **Anclajes fijos:** ¿estan presentes y en orden? En mundodeportivo, ¿aparece el parrafo final OBLIGATORIO literal sin modificar?
5. **Voz:** ¿sigue sonando a larazon / mundodeportivo? La voz no deberia haber cambiado, solo la estructura.

### Iteracion

Si algo no funciona:

- Si el writer ignora la paleta y vuelve al esqueleto fijo → reforzar la instruccion en `writer.md`.
- Si el editor se queja de orden de H2 → revisar el check #2 de `editor-in-chief.md`.
- Si una receta no encaja bien en cierto angulo → ajustar la descripcion de la receta o el mapa orientativo en la guideline correspondiente.
- Si una receta es demasiado vaga o demasiado prescriptiva → reescribir su descripcion (2-3 lineas) en la guideline.

Los ajustes los hacemos en local en esta misma rama. **No pushear** hasta que Javi de el OK explicito.

---

## Como pushear cuando este todo OK

```bash
cd ~/Desktop/JAVI/Proyectos-IA/claude-code-writer-pruebas
git add -A
git commit -m "$(cat <<'EOF'
feat: guidelines v2 con paleta de recetas

Reemplaza la estructura fija (esqueleto unico de articulo) por un modelo de
anclajes fijos + paleta de 10 recetas para el cuerpo libre. El writer ahora
elige 1-3 recetas segun producto + angulo + oferta y las declara en el
frontmatter (campos nuevos `recetas` y `layout`). El editor-in-chief valida
anclajes y coherencia recetas↔contenido, sin imponer orden de H2.

Archivos:
- guidelines/GUIDELINE-larazon.md (v2)
- guidelines/GUIDELINE-mundodeportivo.md (v2)
- .claude/agents/writer.md (instrucciones de seleccion de recetas)
- .claude/agents/editor-in-chief.md (check estructura reformulado)

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
git push -u origin feat/guidelines-v2-paleta-recetas
```

Y abrir PR desde GitHub (o con `gh pr create` si Javi instala `gh`).

---

## Contexto historico (resumen de la sesion anterior)

La sesion anterior ocurrio en otro proyecto (`generador-imagenes-producto`, un proyecto distinto de Javi). Razon: cuando empezamos esto Javi tenia abierto ese proyecto y no nos cambiamos al suyo de `claude-code-writer`. El trabajo se hizo via SSH clone temporal y luego copia durable aqui.

Lo que se diagnostico y se descarto:

- v1 forzaba estructura fija → todos los articulos identicos.
- El writer agente tenia instruccion literal de "replicar EXACTAMENTE" → bloqueador.
- El editor agente validaba "orden y numero de H2 contra guideline" → bloqueador.

Lo que se considero pero NO se hizo:

- Refactorizar el `angle-picker` para que sugiera recetas tambien. Mejora futura.
- Mover la paleta a un archivo compartido en `knowledge/`. Decidido NO: cada guideline auto-contenida es mas legible para Javi.
- Tocar `product-researcher`, `politicas-afiliacion.md`, `frases-vetadas.md`, `medios.md`, skills. No tenian que ver con el cambio.

---

## Si necesitas mas contexto

- Mira el diff completo: `git diff master..feat/guidelines-v2-paleta-recetas`.
- Lee `CLAUDE.md` para la filosofia del sistema.
- Lee `medios.md` para los medios registrados.

Cuando Javi pruebe el primer `/crear-articulo` y traiga feedback, itera aqui en local sobre los 4 archivos. No abandones el branch.
