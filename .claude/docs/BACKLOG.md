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

- Mecanismo en uso: escaneo periódico del gateway cada 10 s. `data/ignition.conf` tiene `wrapper.java.additional.3=-Dignition.projects.scanFrequency=10` (la propiedad sale de `IgnitionProjectManager`; el valor por defecto es 300 s). Medido el 2026-10-22: un cambio en disco se tomó en 9 s y su reversión en 10 s. Backup del conf en `.claude/backups/2026-10-22/gateway-data/ignition.conf`
- Antes de este ajuste los cambios tardaban hasta 5 minutos (escaneos a las 09:32:35, 09:57:38 y 10:02:39 tras el reinicio de las 09:07), por eso parecía que solo funcionaban al reiniciar o con Update Project
- `system.project.requestScan()` no existe en 8.1.19 (tampoco `getProjectManager().requestScan()` de la API Java) y el endpoint `POST /data/project-scan-endpoint/scan` responde 404 (módulo no instalado)
- Hooks de ignition-cc-sync (`~/.claude/scripts/ignition-cc-sync/`): desde el 2026-10-22 el PreToolUse compara el hash SHA-256 del contenido y no el mtime, porque el escaneo de 10 s reescribe los archivos (mismo contenido, mtime nuevo) y bloqueaba cada segunda edición. Backup de la versión anterior en `backup-2026-10-22/`. La copia original del skill sigue comparando mtime
- El timer `claude-code-sync` ya no hace falta: se puede deshabilitar en el Designer (hoy borra el sentinel y falla con `AttributeError` en cada edición). Los hooks se mantienen: el PreToolUse sigue protegiendo contra pisar cambios guardados desde el Designer
- `resource.json` no hace falta actualizarlo a mano: el gateway firma los recursos nuevos o editados al escanearlos (`Setting LastModification to "external"`)
- Si `data/ignition.conf` se regenera (contenedor nuevo o cambio de imagen), volver a agregar la línea

## Objetos estándar (`Objects/`)

- Aplicar formulario por formulario (un commit por formulario, `git revert` para deshacer); ver `OBJETOS_ESTANDAR.md`
- Agregar a papo-lint el patrón "campos fuera de objetos estándar" para medir la adopción
- Diseño estándar (`ESTANDAR_DISENO.md`, herramienta papo-design): revisar el piloto `Form_EA11-0901_1h_PruebaPiloto` en el Designer; si pasa, desplegar por fases (familia EA11-0901 + `Metalurgia/Fundamental Views/Checkbox`, luego por área). Simulado: 238 de 239 formularios aplicables con la recolección idéntica; `FU10-0202_start` a mano
- Siguiente nivel del diseño: clases para preguntas, subtítulos y encabezados (confirmar antes que una clase en la label equivale a `textStyle`), tokens `--papo-*` en el tema, plantilla para formularios nuevos
- Tema `cla-light`/`cla-dark` roto (`:root` sin cerrar: ~75 reglas que el Designer descarta; selectores de input que no coinciden; `boder-color`; dropdowns a 150 px fijos). Parche propuesto en `.claude/docs/theme/`, sin instalar: probar en PAPOS (reinicio de Perspective) y decidir. Ver "Evaluación" en `ESTANDAR_DISENO.md`. Piloto instalado en PAPOS el 2026-10-24 (bloque con alcance `PAPO/Form`, solo el piloto): revisar Designer contra Chrome y decidir si se aplica el parche global

- Objetos v2 en el piloto (2026-10-24): verificar en sesión que los valores se conservan al cerrar/reabrir la sección, guardar un registro y comparar con el original, medir la carga. Si pasa: `papo_objects.py` simula 238 formularios convertibles (4,555 campos)

## Errores de los formularios originales (encontrados con los pilotos, 2026-10-25)

El estándar los reproduce tal cual; corregirlos aparte con `/bug`:
- `Ensamble/Form_EA11-1601_start` (desde 2026-08-31): `Checkbox_4`/`_5` y `_6`/`_7` de "Estado Termoselladora" tienen el mismo `papoItemID` (11190 y 11191): preguntas repetidas en pantalla y en el registro, y faltan 11192 y 11193
- `F&A/Form_GR10-0501_start` (desde el checkpoint `1a0ba2b`, 2026-10-22): en `FlexContainerGroup13/S4` las etiquetas de 5997 y 5998 pasaron a numéricos con ID calculado (`basePapo + índice`) que da 5999 y 6000, repetidos; 5981 se repite 35 veces y 6192 dos (ya en julio)
- `OREC/Form_PO11-0101-2_start`: 5168 se guarda dos veces (ya en septiembre)
- `OREC/Form_CU11-0101_start`: la sección "Verificacion programa de curado y secado" se abre más baja que su contenido (final cortado)
- `papoitem.Description` con tildes mal codificadas en la base ("MÃ¡quina" por "Máquina"), p. ej. 11185–11196: es el dato, se ve igual en el original
- `OREC/Form_CU11-0101_start`: no existe `FlexContainerGroup7`; `papo_core.register.save` recorre los grupos 1..N y los 4 checkbox de `FlexContainerGroup8` nunca se guardan
- ~~Supervisor guardado con `papoItemID` nulo en `Ensamble/Form_EA11-1601_start` y `Form_EA11-2601_start`~~ corregido el 2026-10-26 (11233 y 11355). Queda `OREC/Form_PO07-0101_start` (`FlexContainer15/TextField`, `papoItemID` nulo)
- `F&A/Form_AC10-0201_start`: "Cubierta sin rayones." aparece dos veces en "Condiciones de operacion" y varias preguntas largas se cortan en su fila (también en el original)
- `custom.insights` de los formularios (original y estándar): `preInsight` usa `initialPapoDateTime` y solo se recalcula cuando cambia el texto de Observaciones; si el operario no escribe nada se guarda el turno y la hora del diseño ("T: 3, H: 14:35" en un registro de las 07:55; en el PDF de PO11-0101 sale "T: 3, H: 14:13")

- `F&A/Form_GR10-0501_start` a 1920x1080: filas más bajas que su alto en 10 secciones (Tanque soda 4, Tanque ácido puro 3, Tanques 1–7 y Torres 1 cada una); igual en el original y en el piloto
- `F&A/Form_GR10-0501_start` (original): 7 checkbox de "Tanque soda" y "Tanque ácido puro" muestran el error de su binding de pregunta; en el piloto la pregunta sale de `papoItemID` y no falla
- Numéricos con rango en los originales (AC10, CU11, PO11, GR10, EA11-0901): dentro de rango el texto es gris o gris oscuro; `getRangeColor` del estándar lo deja negro (el rojo fuera de rango es igual)

## Errores de los reportes (encontrados al revisar los PDF de los pilotos, 2026-10-26)

- Reporte `Clarios/Andina/Ensamble/EA11-1601`: el PDF falla con error 500 en los dos ciclos de prueba (`java.lang.StackOverflowError` en `RMLinkedText.getXString`, recursión del texto que pagina). Ya pasó el 2026-10-21, antes de los objetos estándar; la plantilla no cambia desde el checkpoint `1a0ba2b` y el original y el piloto guardan el mismo DataAnswer (`--compare-db --exact`). Sospecha: textos con el desborde por defecto en cajas más bajas que una línea (p. ej. "3" + salto de línea en x=346 y=38, 20×10 con letra de 12, y `@twohourN.papoItemID11208@` con salto de línea en cajas de 10 de alto). Revisarlo en el Designer (Overflow → Shrink) y probar el PDF
- Reporte `Clarios/Andina/F&A/AC10-0201`: la fila "CUMPLE NIVEL MEDIDO CON GALGA?" (ítem 5840) solo tiene `@register1..4.papoItemID5840@` y una clave `@register.papoItemID5840@` sin número; desde el quinto registro del ciclo la columna sale vacía aunque se guardó "Cumple" (las filas vecinas, 5845 y 6464, van de `register1` a `register12`)

## Preguntas desde papoitem (fases 2 y 3)

- Simulación del 2026-10-26 (`simulate_all.py --questions-sql`): 246 preguntas fijas de 192 ítems pasan a `papoItemID`; 121 necesitan `UPDATE papoitem` y hay 1 conflicto (mismo ítem con textos distintos). Generar y aplicar el SQL con cada familia, antes de su commit

## Mejoras opcionales (fuera de la estandarización básica)

- Preguntas en una consulta por vista: hoy hay ~3,520 bindings que consultan `papoitem` uno por pregunta en 153 vistas. `papo_core.items.getQuestions(value)` y `getQuestionText(value)` ya existen (sin uso); se probaron y revirtieron en el piloto EC07-0101 barcada por no ser parte del estándar
- `papo_core.ui.getShift(dateTime=None)` existe sin uso: reemplazar los cálculos con `getHour24` (ui.preInsight, sign.autoCloseOpenForms, report x2, custom.shift de Metalurgia FU10-0202_dia y TR11-0102_start, que además tiene el bug de turno)

## Verificaciones pendientes

- `papo_core.register._getLastRegisterCode` ordena por `ID DESC` en lugar de `RegisterCode DESC` (la regla del proyecto); en la práctica devuelve lo mismo porque ID es creciente

- Scheduled Script de gateway que llama a `papo_core.sign.autoCloseOpenForms("papo_db")`: conexión hardcodeada

- `Page/Gestion`, `custom.signature` (`now(60000)`): cada minuto y en cada sesión abierta consulta todo el historial e inserta una firma tipo 10 "Revisado" con usuario `NA` en los ciclos "En proceso" de más de 180 min (origen de las firmas "NA NA"). Escribe en la base desde un binding de vista, duplica a `autoCloseOpenForms`, puede insertar dos veces si hay dos sesiones abiertas y su llave de ciclo no incluye `WorkstationNodeID`. Decidir si se elimina y se deja solo el cierre automático del gateway
