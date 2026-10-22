# Inventario de despliegue

Registro de cada cambio aplicado a `cla-project/`. Una fila por recurso y cambio; se actualiza en cada ronda.
Backups en `.claude/backups/<fecha>/` con la misma ruta relativa que el archivo original.

| Fecha | Ronda | Recurso | Qué cambió | Verificación visual |
|---|:-:|---|---|---|
| 2026-10-22 | 4 | session-props (`session-props/props.json`) | Transform de `custom.shift`: `system.date.getHour24()` reemplazado por `java.util.Calendar` con TimeZone America/Bogota. Mismos turnos y mismo retorno (string "1"/"2"/"3"). | Sí: `Page/Embedded/F&A/Form_FO10-1701-1_start` → `Label_1` debe mostrar el turno correcto. |
| 2026-10-22 | 4 | session-props (`session-props/props.json`) | Declaradas en `custom` con valor inicial: `adminPermissions: false`, `supervPermissions: false`, `shift: "1"` (los bindings las sobrescriben al iniciar la sesión). | No (solo valor inicial). Confirmar que el árbol de `Docks/Tree_v2` sigue mostrando lo mismo para admin y no admin. **Revertido por el Designer** al guardar session-props (2026-10-22 08:58): no persiste valores estáticos de props con binding. |
| 2026-10-22 | G2 | Gateway Event Scripts (`ignition/event-scripts/data.bin`) | Timer `claude-code-sync` reemplazado desde el Designer por la versión con `system.project.requestScan()`. | No aplica. Sigue fallando en 8.1.19: `system.project.requestScan` no existe en esa versión. |
| 2026-10-22 | 4 | `Page/Embedded/General/Form_PL11-0101-CU_start` | `Label4`: `style.classes` `--cla-text-question` → `text-titles`; `textStyle.color` `#002C36` → `--cla-text-question` (igual a la plantilla). | Sí: el título "FORMULARIO INICIO DE TURNO" toma el estilo `text-titles`; en tema oscuro el color pasa a `#FEFEFE`. |
| 2026-10-22 | 4 | `Page/Embedded/General/Form_PL11-0101-S&A_start` | `Label4`: mismo cambio que CU_start. | Sí: igual que CU_start. |
| 2026-10-22 | 4 | `Page/Embedded/POLY/Form_PL11-0101-CUBIERTA_start` | `Label4`: mismo cambio que CU_start. | Sí: igual que CU_start. |
| 2026-10-22 | 4 | `Page/Digitalizacion_Template` | Quitada la clase inexistente `Page/themes` de `root/FlexContainer_Reports` (1 ocurrencia). | No: la clase no existía, el aspecto no cambia. |
| 2026-10-22 | 4 | `Page/Overview_Papos` | Quitada la clase inexistente `Page/themes` de `FlexContainer_Reports`, `Label_Mill` y `Label_Interval` (3 ocurrencias). | No: la clase no existía, el aspecto no cambia. |
| 2026-10-22 | bug: piloto EC07-0101 barcada | Project Library `papo_core.items` (desplegar primero) | Nuevas `getQuestions(value)` (todas las preguntas del PAPO en una consulta, resuelve `MasterPapoID`) y `getQuestionText(value)` (lee del mapa; consulta individual solo si falta el ítem). | No (sin cambios en funciones existentes). |
| 2026-10-22 | bug: piloto EC07-0101 barcada | Project Library `papo_core.ui` (desplegar primero) | Nueva `getShift(dateTime=None)` con `java.util.Calendar` y America/Bogota. Aún no la usa ninguna vista. | No. |
| 2026-10-22 | bug: piloto EC07-0101 barcada | `Page/Embedded/OREC/Form_EC07-0101_barcada` | Nuevo `view.custom.questions` (binding a `getQuestions`); las 24 etiquetas de pregunta pasan de una consulta cada una a `getQuestionText`; quitado el handler `saveStartShift` sin uso de `Button_Apply` (`"papo_db"` fijo, `ORDER BY ID DESC`); quitada la clave legacy `refreshSecond`. | Sí: los 24 textos de pregunta deben verse igual que antes; guardar un registro y revisar `registerhistory`. |

## Pendientes del plan (ronda 3)

- Cubiertas/ (`Form_PL11-0101-CA_start`, `-CU_start`, `-S&A_start`)
- `Title/Title_0` en `Title_Header` y `Title_Large`
- Clases de UserManagement
- Bloque `params.ds` / yieldCalc (60 vistas)
- Vistas huérfanas y referencias a vistas inexistentes
