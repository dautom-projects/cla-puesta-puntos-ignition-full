---
name: papo-lint
description: Linter de solo lectura para las vistas Perspective de PAPO (cla-project). Reporta por vista "papo_db" hardcodeado, getHour24, último RegisterCode ordenado por Timestamp, prefijo project.papo_core, claves legacy en view.custom y, en vistas Form_*, wrappers de papo_core faltantes (initForm, preInsight, toggleFlexRoot, saveDataRoot, answerRecopile). Úsalo para medir la estandarización, después de editar vistas, o cuando pidan "lint", "revisar estandarización" o "qué vistas no cumplen".
---

# papo-lint

Recorre los `view.json` de `cla-project/com.inductiveautomation.perspective/views/` y reporta los patrones que rompen las convenciones de PAPO. **Solo lee**: nunca modifica vistas.

## Uso

Todo el proyecto (escribe `.claude/docs/LINT_REPORT.md`):

```bash
python3 .claude/skills/papo-lint/scripts/papo_lint.py
```

Solo algunas vistas (imprime el reporte en pantalla, no toca LINT_REPORT.md). Acepta carpetas de vista o rutas a `view.json`:

```bash
python3 .claude/skills/papo-lint/scripts/papo_lint.py --views "cla-project/com.inductiveautomation.perspective/views/Page/Embedded/Ensamble/Form_EA11-1501_30min"
```

Opciones: `--project <carpeta>` (otro proyecto), `--out <archivo>`, `--stdout`.

## Patrones

| Patrón | Qué busca |
|---|---|
| `"papo_db"` en scripts o bindings | Literal `"papo_db"`/`'papo_db'` en `script`, `code`, `expression` o en el `config` de un binding. Los valores persistidos de `view.custom` no cuentan |
| getHour24 | `getHour24(` en scripts o expresiones (los turnos van con `java.util.Calendar` + America/Bogota) |
| Último RegisterCode por Timestamp (o ID) | Consulta cuyo SELECT (no una subconsulta) incluye RegisterCode y cuyo `ORDER BY` empieza por `Timestamp` o `ID` con `DESC` |
| Prefijo `project.papo_core` | Llamadas con el prefijo `project.` |
| Claves legacy | `answers, formato, test, flexGroupCount, flexCount, refreshSecond, dsTable_v3, dsTable_vJ, changedRegister, viewOn` en `view.custom` |
| Form_*: onStartup | Sin `events.system.onStartup` o sin `papo_core.ui.initForm` |
| Form_*: custom.insights | Sin binding o sin transform `preInsight` |
| Form_*: toggleFlexRoot | Ausente o con params distintos de `["sectionIndex"]` |
| Form_*: saveDataRoot / answerRecopile | Ausente o con lógica propia (no llama a `papo_core.register`) |

La plantilla de referencia es `Page/Embedded/Ensamble/Form_EA11-1501_30min` (0 hallazgos).

## Límites

- Solo analiza vistas. No cubre la Project Library, session-props ni los Gateway Event Scripts (binarios en 8.1).
- Detección por texto: una consulta construida dinámicamente o en varias variables puede no detectarse.
