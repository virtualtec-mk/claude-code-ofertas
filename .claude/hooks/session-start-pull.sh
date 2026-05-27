#!/usr/bin/env bash
# Hook SessionStart: trae lo último de GitHub sin bloquear la sesión.
# Se ejecuta al abrir Claude Code en este repo.

set +e

# Solo opera si estamos en un repo git
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  exit 0
fi

# Si hay cambios sin commitear, avisa y no toca nada.
if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
  echo "⚠️  Hay cambios locales sin commitear. Salto el auto-pull para no pisarlos."
  echo "    Cuando los commitees o stashees, en la próxima sesión se actualizará."
  exit 0
fi

OUTPUT=$(git pull --ff-only 2>&1)
STATUS=$?

if [ $STATUS -ne 0 ]; then
  echo "⚠️  No he podido actualizar desde GitHub:"
  echo "$OUTPUT" | head -3
  echo "    Sigo con la versión local. Resuélvelo cuando puedas con: git pull --ff-only"
  exit 0
fi

if echo "$OUTPUT" | grep -q "Already up to date\|Already up-to-date"; then
  echo "✓ Sistema al día."
else
  N=$(echo "$OUTPUT" | grep -E "^\s*[a-f0-9]+\.\.[a-f0-9]+" | wc -l | tr -d ' ')
  echo "✓ Sistema actualizado desde GitHub."
fi

exit 0
