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

## Verificaciones pendientes

- `resource.json` con `actor: "external"`: confirmar si el Designer ignora cambios en disco cuando `actor` es `admin` (regla de `.claude/rules/view-json-editing.md`). Afecta a las 7 ediciones de la ronda 4, que no actualizaron `resource.json`
- Timer Script `claude-code-sync`: falla con `AttributeError: ... no attribute 'requestScan'`; reemplazarlo en el Designer por la versión con `system.project.requestScan()`
- Scheduled Script de gateway que llama a `papo_core.sign.autoCloseOpenForms("papo_db")`: conexión hardcodeada
