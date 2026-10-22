# Backlog PAPO

## Horizonte (de CONTEXT_PROYECTO.md del remoto)

- Migración a tablets/móvil: reemplazar la identificación por IP fija con NFC
- Contraseñas de `papo_db_users`: pasar de texto plano a hashing. Evitar BCrypt: no funciona en el Manual Mode DB User Source de Ignition y su import rompe los módulos del Project Library en scope de sesión Perspective
- Limpieza de ClariosAD: nombres con dobles espacios, columna Badge para NFC

## Pendientes del plan de corrección (ronda 3)

| Pendiente | Vistas | Detalle |
|---|:-:|---|
| Cubiertas (`Form_PL11-0101-CA_start`, `-CU_start`, `-S&A_start`) | 3 | Guardado inline con `"papo_db"` hardcodeado y `ORDER BY ID DESC`. Confirmar si existe un AREA "Cubiertas" en `node`; si no, retirarlas a favor de `General/` y `POLY/`; si existe, migrarlas tomando `General/Form_PL11-0101-*` como base y corregir `basePapo: 1010446` → `10446` en CU_start |
| `Title/Title_0` en `Page/Embedded/Title_Header` y `Title_Large` | 2 (~9 en cascada) | Reemplazar por la clase de `Title/` que corresponda |
| Clases de UserManagement | 9 | `UserManagement/MainFont`, `Page/Page`, `ScheduleManagement/Headers`, `ScheduleManagement/InputFont`, `InputFont` → renombrar a `UserManagement/*` o crear las que falten |
| Bloque `params.ds` / yieldCalc | 60 | Binding deshabilitado que llama a `yieldCalc*.report` (no existen). Quitar `propConfig.params.ds*` y los params sin uso |
| Vistas huérfanas y vistas inexistentes | 7 | Decidir si se borran (Template/Overview, Template/Breakpoint, Digitalizacion_Reportes, MixingDashboard) o se restauran `Components/*` y `CreateOrEditSch`; agregar `Page/` en los cierres de popup de UserManagement |
| Clases rotas restantes | 8 | Tipeos (`text-title-2`, `button-question`, `datetime`, `bg-[--neutral-10]gap-2`) y clases de vistas de test/huérfanas (`some-class`, `gauge-fill-blue`, `Page/Reports/border_1`, `w-28`, `lg:w-21`) |

## Sync con el gateway local (PAPOS, Ignition 8.1.19)

- `system.project.requestScan()` no existe en 8.1.19 (tampoco `getProjectManager().requestScan()` de la API Java); el timer `claude-code-sync` borra el sentinel y falla con `AttributeError`
- El endpoint `POST /data/project-scan-endpoint/scan` responde 404: el módulo project-scan-endpoint no está instalado
- Mecanismo en uso: manual, con Project → Update Project en el Designer o reiniciando el contenedor `PAPOS`. Retomar el timer si el gateway sube de versión (funciona en 8.1.43 y 8.3.8)
- `resource.json` no hace falta actualizarlo: los cambios de la ronda 4 se cargaron sin tocarlo (verificado tras reiniciar PAPOS el 2026-10-22)

## Mejoras opcionales (fuera de la estandarización básica)

- Preguntas en una consulta por vista: hoy hay ~3,520 bindings que consultan `papoitem` uno por pregunta en 153 vistas. `papo_core.items.getQuestions(value)` y `getQuestionText(value)` ya existen (sin uso); se probaron y revirtieron en el piloto EC07-0101 barcada por no ser parte del estándar
- `papo_core.ui.getShift(dateTime=None)` existe sin uso: reemplazar los cálculos con `getHour24` (ui.preInsight, sign.autoCloseOpenForms, report x2, custom.shift de Metalurgia FU10-0202_dia y TR11-0102_start, que además tiene el bug de turno)

## Verificaciones pendientes

- `papo_core.register._getLastRegisterCode` ordena por `ID DESC` en lugar de `RegisterCode DESC` (la regla del proyecto); en la práctica devuelve lo mismo porque ID es creciente

- Scheduled Script de gateway que llama a `papo_core.sign.autoCloseOpenForms("papo_db")`: conexión hardcodeada
