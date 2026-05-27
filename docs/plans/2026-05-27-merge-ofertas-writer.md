# Plan: fusionar `claude-code-ofertas` + `claude-code-writer` en un solo repo

**Fecha:** 27/05/2026
**Autor:** Claude (asistido)
**Estado:** propuesto, pendiente de ejecución

## Objetivo

Unificar los repos `virtualtec-mk/claude-code-ofertas` y `virtualtec-mk/claude-code-writer` en un único repo de GitHub (`virtualtec-mk/claude-code-ofertas`) que se clone una sola vez en local y exponga ambas familias de comandos (`/buscar-ofertas`, `/crear-articulo`, `/crear-guideline`, `/importar-gpt`) en la misma sesión de Claude Code. Auto-pull de GitHub al iniciar sesión. `/crear-articulo` que priorice URLs si se pasan; si no, lea del `inbox/` interno.

## Diagnóstico actual

### 1. Estado de `claude-code-ofertas` (local vs GitHub)

- **Local NO es repo git** (sin `.git/`). Trabajaba directamente sobre ficheros.
- **GitHub** (`virtualtec-mk/claude-code-ofertas`) está en commit `839fa31` y tiene mejoras que el local NO tiene:
  - **R4: validación de coherencia título** en `offer-enricher.md` (`StoreMismatchError`, `force_match`, Paso 3.5).
  - `radar-catalog-client.md` reescrito con **WebFetch** (no Bash, más limpio).
  - `buscar-ofertas/SKILL.md` con la pausa interactiva de mismatch.
- **Local** tiene cambios manuales sin pushear:
  - Renombrado de referencias `claude-code-text-agents` → `claude-code-writer` en `CLAUDE.md`, `buscar-ofertas/SKILL.md`, `offer-enricher.md`, `radar-catalog-client.md` (legacy: el hermano fue renombrado).
  - `.env`, `.playwright-mcp/`, `historial/2026-05-27-sesion-1.md`, `changelog/changelog-2026-05-27.txt` (working state de la sesión actual).
- **Resolución de divergencia**: usaremos GitHub HEAD como base de código (tiene R4) y aplicamos encima el working state local. El rename `text-agents → writer` deja de importar porque al aplanar el hermano dentro, las rutas se vuelven internas (`guidelines/`, `inbox/`) y desaparecen.

### 2. Estado de `claude-code-writer` (local vs GitHub)

- **Local SÍ es repo git**, en `master` `c2988f8`, sin cambios trackeados pendientes.
- Tiene untracked: screenshots, `.playwright-mcp/`, `drafts/larazon/`, `drafts/abc/`, `drafts/mundodeportivo/20260519-trio-poco-x8-pro-f8-pro-f8-ultra.md`, `inbox/27-05-2026-xiaomi-smart-air-fryer-4-5l.md` (la que escribimos hoy).
- Sincronizado con `origin/master`.

### 3. Colisiones de carpetas/ficheros entre ambos al aplanar

| Carpeta/fichero | Ofertas | Writer | Resolución |
|---|---|---|---|
| `.claude/agents/` | aggregator-scraper, telegram-scraper, offer-enricher, radar-catalog-client | angle-picker, editor-in-chief, headline-generator, product-researcher, writer | Sin colisión. Unión directa. |
| `.claude/skills/` | buscar-ofertas | crear-articulo, crear-guideline, importar-gpt | Sin colisión. Unión directa. |
| `.claude/settings.json` | Permisos del scraping + radar | Permisos del writer (git, bash, etc.) | Fusión manual. Eliminar rutas `../claude-code-writer/**` (ya no aplican). |
| `CLAUDE.md` | Localizador | Writer | Reescritura: nuevo CLAUDE.md unificado con secciones por dominio. |
| `README.md` | Localizador | Writer | Reescritura: README unificado. |
| `knowledge/` | `notas-degradacion.md` | ejemplos-publicados, frases-vetadas, headline-recipes, manifiesto-editorial, naming-productos, personas-redactoras, politicas-afiliacion, posicion-precio-por-angulo | Sin colisión de ficheros. Unión directa. |
| `docs/` | brainstorms, plans, qa, instalacion.txt, configuracion-local-radar.txt, integracion-radar-editorial.txt | docs propio del writer | Verificar: ambos tienen `docs/`. Listar y unir. |
| `inbox/` | — | sí (con la ficha de hoy) | Mover a la raíz. |
| `drafts/` | — | sí | Mover a la raíz. |
| `guidelines/` | — | sí (GUIDELINE-larazon.md etc.) | Mover a la raíz. |
| `medios.md` | — | sí | Mover a la raíz. |
| `watchlists/` | sí | — | Permanece. |
| `fuentes.md` | sí | — | Permanece. |
| `historial/` | sí | — | Permanece. |
| `changelog/` | sí | — | Permanece. |
| `tasks/` | sí (en GitHub remoto) | — | Permanece. |
| `pruebas/` | — | sí | Mover a la raíz. |
| `.env` / `.env.example` | sí | — | Permanece. `.env` queda gitignored. |
| `.gitignore` | sí | sí | Fusionar. |

## Estructura final

```
claude-code-ofertas/                       (= raíz del repo unificado)
├── .claude/
│   ├── settings.json                      ← permisos fusionados
│   ├── agents/                            ← 9 subagentes (4 + 5)
│   │   ├── aggregator-scraper.md
│   │   ├── telegram-scraper.md
│   │   ├── offer-enricher.md
│   │   ├── radar-catalog-client.md
│   │   ├── product-researcher.md
│   │   ├── angle-picker.md
│   │   ├── headline-generator.md
│   │   ├── writer.md
│   │   └── editor-in-chief.md
│   ├── skills/
│   │   ├── buscar-ofertas/SKILL.md
│   │   ├── crear-articulo/SKILL.md        ← modificado: prioridad URL → inbox
│   │   ├── crear-guideline/SKILL.md
│   │   └── importar-gpt/SKILL.md
│   └── hooks/                             ← NUEVO
│       └── session-start-pull.sh          ← git pull --ff-only
├── CLAUDE.md                              ← reescrito, unificado
├── README.md                              ← reescrito, unificado
├── fuentes.md
├── medios.md
├── guidelines/
├── inbox/                                 ← interno
├── drafts/
├── watchlists/
├── historial/
├── changelog/
├── knowledge/
├── docs/
│   ├── brainstorms/
│   ├── plans/
│   ├── qa/
│   ├── instalacion.txt
│   ├── configuracion-local-radar.txt
│   └── integracion-radar-editorial.txt
├── pruebas/
├── tasks/
├── .env.example
├── .env                                   ← gitignored
└── .gitignore
```

## Cambios funcionales además del merge

### A. Hook `SessionStart` para auto-pull

Crear `.claude/hooks/session-start-pull.sh` (chmod +x) y registrarlo en `.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "*",
        "hooks": [{ "type": "command", "command": ".claude/hooks/session-start-pull.sh" }]
      }
    ]
  }
}
```

Contenido del script: `git pull --ff-only` con manejo silencioso si está al día, mensaje claro si hubo cambios o si falló. No bloquea la sesión nunca.

Beneficio: cada vez que abres Claude Code en este repo, se trae lo último de GitHub. Trabajo siempre sobre la versión actualizada.

### B. `/crear-articulo` con prioridad URL → inbox

Modificar `PASO 1` del SKILL para que detecte si `$ARGUMENTS` contiene URLs (`http://` o `https://`):

- **Hay URLs**: comportamiento actual.
- **NO hay URLs y SÍ hay otros tokens**: el primero no-URL puede ser `MEDIO`. El siguiente token (si existe) se trata como **filtro de búsqueda en `inbox/`**.
  - Si encuentra 1 ficha → extrae `url_producto` del frontmatter y continúa como si la URL hubiera sido pegada.
  - Si encuentra 0 → muestra menú con todas las fichas de `inbox/` y deja elegir.
  - Si encuentra varias → muestra menú filtrado y deja elegir.
- **Solo MEDIO o nada**: lista `inbox/` completo y deja elegir.

Invocaciones soportadas:

```
/crear-articulo https://es.aliexpress.com/item/123.html larazon       (modo actual)
/crear-articulo larazon                                                (menú inbox completo)
/crear-articulo larazon xiaomi                                         (filtra inbox por "xiaomi")
/crear-articulo larazon                                                (menú si hay ambigüedad)
```

El resto del flujo (product-researcher, angle-picker, etc.) NO se toca. El `inbox/` se usa solo para resolver la URL.

### C. Eliminar referencias a `../claude-code-writer/` y `../claude-code-text-agents/`

En `buscar-ofertas/SKILL.md`, `offer-enricher.md`, `radar-catalog-client.md`, `CLAUDE.md`: sustituir `../claude-code-writer/inbox/` → `inbox/`, `../claude-code-writer/guidelines/` → `guidelines/`, `../claude-code-writer/medios.md` → `medios.md`. Quitar la verificación de "si la carpeta hermana no existe…" (ya no aplica).

### D. Fusionar `CLAUDE.md`

Sección 1: identidad del repo (descubre + redacta).
Sección 2: estructura de carpetas (combinada).
Sección 3: dominio "descubrimiento" (resumen + link a docs/).
Sección 4: dominio "redacción" (resumen + link).
Sección 5: convenciones comunes (fechas, números, idioma).
Sección 6: política de scraping (heredada del localizador).
Sección 7: política editorial (heredada del writer).
Sección 8: errores tipados (unión).

### E. Fusionar `.claude/settings.json`

Permisos:
- `allow`: unión sin duplicados.
- `deny`: unión. Eliminar denies a `../claude-code-writer/**` (ya no existen).
- Añadir `Bash(.claude/hooks/*.sh)` para el hook.

## Plan de ejecución

### Fase 0 — Backup defensivo (reversible)

1. Copiar el local actual a `/tmp/backup-ofertas-2026-05-27/` (carpeta intacta).
2. Copiar `../claude-code-writer/` a `/tmp/backup-writer-2026-05-27/`.

### Fase 1 — Construir el repo unificado en una carpeta de trabajo

3. Crear `/tmp/merge-work/`.
4. Clonar `claude-code-ofertas` de GitHub ahí dentro (base con commit `839fa31`).
5. Añadir el writer como segundo remote y `git fetch`.
6. `git merge --allow-unrelated-histories writer/master -X ours` (preserva ambas historias; `ours` solo aplica al caso teórico de doble fichero con mismo path — no hay).
7. Mover `inbox/`, `drafts/`, `guidelines/`, `medios.md`, `knowledge/*` (los nuevos), `pruebas/` desde donde queden a la raíz (deberían estar ya en raíz tras el merge porque writer las tenía ahí). Confirmar.
8. Borrar referencias `claude-code-writer` / `claude-code-text-agents` de los ficheros del scraping.
9. Reescribir `CLAUDE.md`, `README.md`, `.claude/settings.json`, `.gitignore`.
10. Crear `.claude/hooks/session-start-pull.sh` + chmod +x + registrarlo en `settings.json`.
11. Modificar `.claude/skills/crear-articulo/SKILL.md` (prioridad URL → inbox).
12. `git add` + commit en una sola entrada: `feat: merge claude-code-writer into ofertas; aplanar arquitectura; auto-pull en SessionStart; crear-articulo lee inbox/`.

### Fase 2 — Aplicar working state local

13. Copiar a la carpeta de trabajo desde el local actual:
    - `.env` (no se trackea, gitignored).
    - `historial/2026-05-27-sesion-1.md`.
    - `changelog/changelog-2026-05-27.txt`.
    - `.playwright-mcp/` si interesa (probablemente .gitignored).
14. Copiar a la carpeta de trabajo desde `../claude-code-writer/` los untracked relevantes:
    - `inbox/27-05-2026-xiaomi-smart-air-fryer-4-5l.md` (ya generado hoy).
    - `drafts/larazon/`, `drafts/abc/`, `drafts/mundodeportivo/20260519-...` (si el usuario los quiere conservar; verificar primero).
    - Screenshots/snapshots sueltos del writer: `snap-*.md`, `snapshot-*.md`, `*.jpeg`, `*.png` — moverlos a `pruebas/` o eliminarlos (eran working scratch).
15. Commit del working state como segunda entrada: `chore: working state previo al merge (sesion 27/05/2026)`.

### Fase 3 — Verificación local

16. Abrir Claude Code en la carpeta de trabajo, listar skills disponibles, confirmar que aparecen `/buscar-ofertas`, `/crear-articulo`, `/crear-guideline`, `/importar-gpt`.
17. Verificar que el hook `SessionStart` se ejecuta (mensaje en arranque).
18. Smoke test: `/crear-articulo larazon xiaomi` debería listar/encontrar la ficha del inbox.
19. Si todo OK, sustituir el local actual:
    - Mover `/Users/javirosagro/Desktop/JAVI/Proyectos-IA/claude-code-ofertas` a `/tmp/old-ofertas-2026-05-27/`.
    - Mover `/tmp/merge-work/claude-code-ofertas` a `/Users/javirosagro/Desktop/JAVI/Proyectos-IA/claude-code-ofertas`.
    - Dejar `../claude-code-writer/` intacto por ahora (backup vivo, el usuario lo borra cuando confirme).

### Fase 4 — Push a GitHub (IRREVERSIBLE — requiere confirmación del usuario)

20. `git push origin master` desde la nueva carpeta. Si el remoto rechaza por history-rewrite (no debería, porque mergeamos cleanly), usar `git push --force-with-lease`.
21. Opcional: archivar el repo `virtualtec-mk/claude-code-writer` en GitHub (no borrarlo) para preservar historia y trazabilidad. Lo haces tú desde la UI.

## Tabla de riesgos

| Riesgo | Mitigación |
|---|---|
| Pérdida de working state del local actual | Fase 0 (backup). Fase 2 copia explícita. |
| Conflictos en `git merge --allow-unrelated-histories` | No hay rutas en colisión (verificado en diagnóstico). |
| Hook `SessionStart` no se ejecuta | Verificar permisos `chmod +x`. Test manual con `bash .claude/hooks/session-start-pull.sh`. |
| `git pull --ff-only` falla si el usuario tiene cambios locales | El hook avisa y no bloquea. Diseño: `set +e`, mostrar advertencia, continuar. |
| Push a GitHub fallido | Pausa antes del push. Si falla force-with-lease, intervención manual. |
| El writer-repo en GitHub queda huérfano | Archivarlo, no borrarlo. Trazabilidad preservada. |
| `.env` se sube por accidente | Verificar `.gitignore` antes del primer commit. |

## Decisiones tomadas (todas reversibles antes del push)

- **Nombre del repo final**: `claude-code-ofertas` (reutilizar existente, el flujo end-to-end es ofertas → artículo).
- **Base de código para ofertas**: GitHub HEAD `839fa31` (incluye R4).
- **Estrategia de merge**: `--allow-unrelated-histories` preservando ambas historias.
- **Auto-pull**: hook `SessionStart`, no PASO 0 manual.
- **Inbox priority**: URL > filtro en inbox > menú completo.

## Próximos pasos

Si confirmas, ejecuto Fases 0-3 (local, todo reversible) y paro antes de Fase 4 (push) para enseñarte el resultado.
