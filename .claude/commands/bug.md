---
description: Corregir un bug de PAPO siguiendo el flujo estándar (checkpoint, impacto, papo_core, lint, commit, inventario)
argument-hint: <descripción del bug>
---

Corrige este bug de PAPO: $ARGUMENTS

Sigue estos pasos en orden y no te saltes ninguno:

1. **Checkpoint.** Ejecuta `git status`. Si hay cambios sin commit, haz primero un commit `chore: checkpoint antes de <bug>` (con un resumen corto del bug en lugar de `<bug>`). Si no hay cambios, no hagas commit.

2. **Ubicar e impacto.** Encuentra la vista o el script afectado. Busca su nodo en `.claude/ignition-graph/impact.json` y revisa `used_by` y `afecta_transitivo` para saber qué más lo usa. Menciona ese impacto antes de editar.

3. **Dónde corregir.**
   - Si el fallo está en lógica compartida, corrígelo en `papo_core` (`cla-project/ignition/script-python/papo_core/<modulo>/code.py`), no en la vista.
   - Si la vista tiene lógica propia que duplica `papo_core`, migrarla a los wrappers estándar es parte de la corrección (ver `.claude/rules/papo-core-wrappers.md` y `.claude/docs/PROCEDIMIENTO_ESTANDARIZACION.md`).

4. **Editar view.json.** Haz un backup en `.claude/backups/<fecha>/` con la ruta relativa. Usa cambios puntuales sobre el texto: nunca reescribas el archivo con `json.dump`. Conserva los finales de línea y el escapado Gson (`=`, `<`, `>`, `&`, `'`). Después de cada edición valida que el JSON parsea.

5. **Lint.** Ejecuta el linter sobre las vistas tocadas:
   ```bash
   python3 .claude/skills/papo-lint/scripts/papo_lint.py --views "<carpeta de cada vista tocada>"
   ```
   Reporta los hallazgos. No dejes hallazgos nuevos introducidos por la corrección.

6. **Commit e inventario.** Agrega las filas a `.claude/docs/DEPLOY_INVENTORY.md` (fecha, ronda "bug: <resumen>", recurso, qué cambió, verificación visual) en orden de despliegue: primero los módulos de la Project Library y después las vistas que los llaman. Luego haz commit `fix: <bug>` con el código y el inventario.

7. **Cierre.** Recuérdale al usuario hacer **Project → Update Project** en el Designer (o reiniciar el contenedor `PAPOS`) para ver el cambio. Si cambiaron relaciones entre recursos (llamadas, vistas embebidas, mensajes, estilos), vuelve a correr el skill `ignition-graph` con salida en `.claude/ignition-graph/`.
