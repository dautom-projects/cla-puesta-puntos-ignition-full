# Backlog PAPO

## Horizonte (de CONTEXT_PROYECTO.md del remoto)

- Migración a tablets/móvil: reemplazar la identificación por IP fija con NFC
- Contraseñas de `papo_db_users`: pasar de texto plano a hashing. Evitar BCrypt: no funciona en el Manual Mode DB User Source de Ignition y su import rompe los módulos del Project Library en scope de sesión Perspective
- Limpieza de ClariosAD: nombres con dobles espacios, columna Badge para NFC

## Pendientes del plan de corrección (ronda 3)

| Pendiente | Vistas | Detalle |
|---|:-:|---|
| Cubiertas (`Form_PL11-0101-CA_start`, `-CU_start`, `-S&A_start`) | 3 | Migradas al v2 y estandarizadas el 2026-10-26 (decisión del usuario; no existe el AREA "Cubiertas" en `node` y el Template abre `General/`). Quedan errores del original frente a `General/`: `basePapo: 1010446` (→ `10446`) en CU_start y las filas de 9186/9187 que no tiene CA_start |
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
- ~~`Ensamble/Form_EA11-1601_start` (desde 2026-08-31): `Checkbox_4`/`_5` y `_6`/`_7` de "Estado Termoselladora" tienen el mismo `papoItemID` (11190 y 11191): preguntas repetidas en pantalla y en el registro, y faltan 11192 y 11193~~ corregido el 2026-10-28: 11192 y 11193 sí se guardaban (sección Elementos de Soporte); el que faltaba era 11194 (boquillas). Sale la fila repetida de 11190 y la segunda de 11191 pasa a 11194 (`.claude/docs/qa/EA11-1601-filas.md`)
- ~~`F&A/Form_GR10-0501_start` (desde el checkpoint `1a0ba2b`, 2026-10-22): en `FlexContainerGroup13/S4` las etiquetas de 5997 y 5998 pasaron a numéricos con ID calculado (`basePapo + índice`) que da 5999 y 6000, repetidos; 5981 se repite 35 veces y 6192 dos (ya en julio)~~ corregido el 2026-10-28 junto con S0 y S3, que guardaban en 6191–6194 de TE11-0601 (`.claude/docs/qa/GR10-0501-ids.md`). 6192 ya no se repite. Queda por decidir: 34 etiquetas de tag ocultas con 5981 y 3 en S3 que se siguen recolectando
- `OREC/Form_PO11-0101-2_start`: 5168 se guarda dos veces (ya en septiembre)
- `OREC/Form_PO11-0101-1_start` … `-4_start` (confirmado en la fase 5, 2026-10-27): el contenedor "Antes del arranque o durante el proceso" guarda 5168 con el texto marcado, su `Checkbox` guarda 5168 otra vez (Cumple / No Cumple) y `Checkbox_1` guarda 5169, que no existe en `papoitem`. `Metalurgia/Form_FU11-0101_start` usa esos mismos 5168 y 5169 para "Mantenimiento Predictivo / Correctivo" (su contenedor es 7906). El estándar lo conserva igual
- `Ensamble/Form_EA11-1603_1h`: el script de color de 19 numéricos lee `rang_down` / `rang_up`, que el campo no tiene; el binding fallaba y nunca se pintaban de rojo. Convertidos sin rango (decisión del usuario, 2026-10-27): falta definir esos rangos
- `POLY/Form_PL11-0101-CAJA_start`: el grupo "CAV2" guarda en 9177, que la base describe como "CAV1 (primera) // Verificacion altura troquelado con galga" (¿ID equivocado?). Se dejó el texto corto fijo
- `F&A/Form_FO10-0100_input` y `FO10-0601_input`: la respuesta de `Dropdown_0` es `str(<Dropdown>) + " - " + str(<Dropdown_0>)`, y `Dropdown` tiene `custom.item_dev` (no se guarda). Nunca responde "-" ("None - None"). Queda nativo: un objeto tiene que responder su propio valor
- `OREC/Form_CI11-0101_start` `NumericEntryField_6`: válido en 0 o entre 90 y 150 (dos rangos). Queda nativo (decisión del usuario, 2026-10-27)
- `Ensamble/Form_EA11-0901_2h`: una etiqueta de "Parámetros de operación y control proceso" muestra "null" (igual en el original)
- `OREC/Form_CU11-0101_start`: la sección "Verificacion programa de curado y secado" se abre más baja que su contenido (final cortado) — **corregido por el estándar** (papo_objects v2.9, `fitSections`: la sección conserva su alto y alcanza para sus filas)
- ~~`papoitem.Description` con tildes mal codificadas en la base ("MÃ¡quina" por "Máquina"), p. ej. 11185–11196~~ corregido el 2026-10-27 en cla-db-papo (62 ítems y `registertype` 13; `.claude/docs/sql/2026-10-27_tildes_papoitem.sql`, falta producción). Las palabras escritas sin tilde ("presion", "operacion") no se tocaron
- `OREC/Form_CU11-0101_start`: no existe `FlexContainerGroup7`; `papo_core.register.save` recorre los grupos 1..N y los 4 checkbox de `FlexContainerGroup8` nunca se guardan
- ~~Supervisor guardado con `papoItemID` nulo en `Ensamble/Form_EA11-1601_start` y `Form_EA11-2601_start`~~ corregido el 2026-10-26 (11233 y 11355). Queda `OREC/Form_PO07-0101_start` (`FlexContainer15/TextField`, `papoItemID` nulo)
- `F&A/Form_AC10-0201_start`: "Cubierta sin rayones." aparece dos veces en "Condiciones de operacion" y varias preguntas largas se cortan en su fila (también en el original)
- `custom.insights` de los formularios (original y estándar): `preInsight` usa `initialPapoDateTime` y solo se recalcula cuando cambia el texto de Observaciones; si el operario no escribe nada se guarda el turno y la hora del diseño ("T: 3, H: 14:35" en un registro de las 07:55; en el PDF de PO11-0101 sale "T: 3, H: 14:13")

- `F&A/Form_GR10-0501_start` a 1920x1080: filas más bajas que su alto en 10 secciones (Tanque soda 4, Tanque ácido puro 3, Tanques 1–7 y Torres 1 cada una); igual en el original y en el piloto — **corregido por el estándar** (papo_objects v2.9, `fitSections`: la sección conserva su alto y alcanza para sus filas)
- `OREC/Form_EJ11-0101_1h` (también en el original): no guarda nada. Su único ítem (7914 "Referencia", una etiqueta que muestra un tag con color de rango) está en `FlexContainer1`, fuera de un `FlexContainerGroupN`, y sin `custom.item.answer`; los registros de 1 hora solo llevan el comentario
- `OREC/Form_PO07-0101_start` (también en el original, registro 624 de junio): 10 ítems se guardan dos veces (8108–8112, 8124–8128…), el primero `null`; el reporte toma el primero e imprime "None"
- `F&A/Form_FO10-0601_input`: el autocompletado de circuitos por número de mesa no funciona (tampoco en el original): el script de `custom.circuitsOptions` / `custom.tableCombined` y sus bindings buscan `FlexContainerGroup1/FlexContainer1`, que no existe (la mesa y "Mesa combinada" están directo en `FlexContainerGroup1`). Corregir la ruta si se quiere el autocompletado
- `F&A/Form_GR10-0501_start`: 7 checkbox ocultos (`position.display: false`) en "Tanque soda" y "Tanque ácido puro" con `custom.item_dev` (no se recolectan) y un binding de pregunta que lee `custom.item` y falla; no se ven, pero dejan errores en el cliente. Quedan nativos en el estándar. Decidir si se borran
- Numéricos con rango en los originales (AC10, CU11, PO11, GR10, EA11-0901): dentro de rango el texto es gris o gris oscuro; `getRangeColor` del estándar lo deja negro (el rojo fuera de rango es igual)

- `OREC/Form_PO11-0101-2_start`: "Estado - Antes del arranque o Durante el proceso" se abre más baja que sus filas (`custom.baseBasisPx` 417 para 424 px de filas) y una fila queda comprimida; igual en el original. En "Molinos" el original también comprimía una fila; el estándar ya no — **corregido por el estándar** (papo_objects v2.9, `fitSections`: la sección conserva su alto y alcanza para sus filas)

- Vistas que el Template nunca abre (el tipo de la ruta sale de un mapa fijo sin espacios): `F&A/Form_AC10-0201_30min D`, `_SKU D`, `F&A/Form_AC10-0202_30min D`, `_SKU D`, `_start D` y `F&A/Form__end` (sin referencia en el nombre), desde el checkpoint `1a0ba2b`. Se dejan como están, sin estandarizar ni borrar (decisión del usuario, 2026-10-26)
- `Page/Embedded/Metalurgia/Fundamental Views/Checkbox`, la plantilla de los repeaters: desde OREC ninguna vista la usa (huérfana en el grafo). Decidir si se borra

- ~~`Metalurgia/Form_FU10-0202_dia`: sus 42 campos quedaban nativos porque cada fila tenía un `custom.answers` legacy que leía el valor del campo~~ corregido (papo_objects v2.11 quita el recolector de fila; los 42 son `Objects/Dropdown`)

## Errores de los reportes (encontrados al revisar los PDF de los pilotos, 2026-10-26)

- ~~Reporte `Clarios/Andina/Ensamble/EA11-1601`: el PDF falla con error 500 en los dos ciclos de prueba (`java.lang.StackOverflowError` en `RMLinkedText.getXString`, recursión del texto que pagina). Ya pasó el 2026-10-21, antes de los objetos estándar; la plantilla no cambia desde el checkpoint `1a0ba2b` y el original y el piloto guardan el mismo DataAnswer (`--compare-db --exact`). Sospecha: textos con el desborde por defecto en cajas más bajas que una línea (p. ej. "3" + salto de línea en x=346 y=38, 20×10 con letra de 12, y `@twohourN.papoItemID11208@` con salto de línea en cajas de 10 de alto). Revisarlo en el Designer (Overflow → Shrink) y probar el PDF~~ corregido el 2026-10-27 con `report_bin.py`: la causa era "SECCION 1" (`wrap="wrap"`, Calibri 10 en 12 de alto: la línea no cabe y el texto se enlaza sin fin); queda en `shrink` con las 59 cajas en Paginate más bajas que su línea. El PDF sale y coincide con lo guardado
- Reporte `Clarios/Andina/F&A/AC10-0201`: la fila "CUMPLE NIVEL MEDIDO CON GALGA?" (ítem 5840) solo tiene `@register1..4.papoItemID5840@` y una clave `@register.papoItemID5840@` sin número; desde el quinto registro del ciclo la columna sale vacía aunque se guardó "Cumple" (las filas vecinas, 5845 y 6464, van de `register1` a `register12`)
- ~~Reporte `Clarios/Andina/OREC/EJ11-0101`: la caja de "Velocidad de las aspas" (placa estándar) muestra dos valores ("7.0 7.0") en el PDF del ciclo de prueba; el original y el estándar guardan el mismo DataAnswer, así que viene de la plantilla (la casilla repite la clave: `@shift1.papoItemID4574@ @shift1.papoItemID4574@`, confirmado en la prueba general)~~ corregido el 2026-10-27: queda una sola clave (la fila no tiene ítem de placa GN; el 4575 no existe)

## Errores de los reportes (prueba general, 2026-10-27)

El formulario guarda bien en todos estos casos (comparado celda por celda contra el DataAnswer). Los reportes se corrigieron el 2026-10-27 con `.claude/skills/papo-qa/scripts/report_bin.py` (sin el Designer), salvo lo que sigue abierto:

- ~~`F&A/GR10-0501`: la sección "al inicio de cada turno" tiene una columna por turno y su consulta trae los tipos 3, 5, 6, 7 y 8; el Fin cae en el turno de un Inicio y lo reemplaza, así que las respuestas de ese Inicio no salen en el PDF. Además la columna "Tanque 4" usa `register1` tres veces (ítem 6551: `@register1.papoItemID6551@` en x 507, 524 y 540)~~ corregido el 2026-10-27: los registros del mismo turno se suman en la columna (antes el Fin reemplazaba el Inicio) y 40 claves de la plantilla (Tanque 4 con `register2`/`register3`; Ácido filas 311/320/341; Tanque 7 filas 293–341; `651` → `6513`). La casilla única de Torres en y=342 mostraba el 6603: Scrubber y Torres no tienen nivel de tanque (usuario, 2026-10-27), así que la casilla queda vacía como la de Scrubber y el formulario ya no tiene esas dos filas
- ~~`F&A/PT11-0104`: las dos casillas del ítem 6257 usan `@register1.cumplepapoItemID6257@` / `nocumple…` (sin punto) y el script crea `register1.cumple.papoItemID6257`: su marca nunca sale~~ corregido el 2026-10-27 (claves con punto)
- ~~`Metalurgia/TR11-0101`: `rangoReprocesed = list(range(6303, 6350))` deja fuera el 6350 ("Objetivo diario a producir, lo conoce?"), así que su marca Cumple / No cumple no sale; `startShift.papoItemID10949` (Supervisor) no lo llena el script~~ corregido el 2026-10-27 (`range(6303, 6351)` y el Supervisor desde `register1`)
- ~~`Metalurgia/TR11-0102`: la grilla mensual turno × día (`turnoN.diaD`) sale vacía aunque el Inicio del 27 está guardado con 24 "Cumple"; el script llega al final (el comentario sí sale). Revisar con la vista previa del Designer (papoID 1106, nodeID 10, registerCode 1)~~ corregido el 2026-10-27: las claves sí resolvían; las casillas usaban Calibri negrita, sin el glifo ✔, y la más baja no cabía. Las 2325 casillas de la grilla pasan a la fuente Dialog con `shrink`; el día 27 muestra sus 24 ✔
- ~~`Metalurgia/SO02-4502` (grilla semanal día × turno): tres casillas tienen las claves de dos columnas (`@shift6.papoItemID4501@ @shift7.papoItemID4501@`, `@shift1…4509@ @shift5…4509@`, `@shift16…4521@ @shift17…4521@`)~~ corregido el 2026-10-27 (cada casilla con la clave de su columna)
- ~~`OREC/EC07-0101`: la referencia de la barcada (ítem 7931) se corta en la casilla de 26 px ("ZN NEGATI" de "ZN NEGATIVA COM 85X")~~ corregido el 2026-10-27 (`shrink` en las 16 casillas; se lee en dos líneas)
- ~~Valores de tag sin dato (PA11-0301 pH, EJ07-0101 Temp_Horno, EJ11-0102 Temp_Horno / Cantidad_Placas): el script hace `str(None)` y el PDF imprime "None". En develop no hay tags; en producción pasa si el tag está en mala calidad~~ el PDF ya no imprime "None" (`papo_core.report` v2.8.6, 2026-10-28)
- El registro de Fin no tiene sección en varios reportes (CG10-0101, FO10-1701-1, PT11-0104, TE11-2601, TE11-0601, FU10-0202, FU11-0101, PA11-0301/0401, RE10-0102, SO02-1006/4502, TR11-0102, CI11-0101, CU11-0101, EC11-0101, EJ07/EJ11, MZ07/MZ11, PO11-0101-N, RJ11-0101-N); confirmar si es lo esperado
- Textos en vertical (usuario y firma por turno en SO02-1006 / SO02-4502): la herramienta de la prueba no los lee; revisarlos a ojo en el PDF

## Datos y configuración (prueba general, 2026-10-27)

- ~~`nodepapo` 2136 asigna CG10-0101 al nodo 1001 "PC" (tipo `Workstation`): el Template solo saca el área de nodos LINE o CELL y abre `Page/Embedded/None/...` ("View Not Found"). Sus registros anteriores están en las líneas 84 y 85; la prueba se hizo en la 85~~ corregido el 2026-10-27 en cla-db-papo (`.claude/docs/sql/2026-10-27_nodo_CG10-0101_cell.sql`): el nodo 1001 pasa a CELL y su `Topic` a la ruta completa (era 'PC' y Gestión no encontraba el reporte). Ciclo y PDF probados desde la estación. Falta aplicarlo en producción
- ~~El editor de nodos (`Page/PopUps/CreateOrEditNode-Clarios`) no ofrece el tipo CELL y el `Topic` se escribe a mano; Gestión arma la ruta del reporte con sus 3 primeros segmentos, así que un Topic incompleto deja la estación sin PDF~~ corregido el 2026-10-28 (CELL, Topic por defecto del padre y `&` `,` `-` en los segmentos). En develop ninguna página abre el editor (solo el popup de órdenes de MES Core)
- `papo_core.register._getLastRegisterCode` numera los ciclos por (`WorkstationNodeID`, `PapoID`), pero los reportes y Gestión filtran por (`PapoID`, `NodeID`, `RegisterCode`): si un PAPO se llena en el mismo nodo desde dos estaciones, los ciclos se cruzan. Pasa en PO07-0101 (estaciones 22 y 27 con el código 1) y su PDF mezcla registros de junio; en la base de prueba, 36 ciclos de 12 PAPOs. Decidido (usuario, 2026-10-27): un formulario por estación. Hecho: `papo_core.report` v2.3.0 filtra por `workstationNodeID` y el piloto F&A (AC10-0202, AC10-0301, AC10-1101, CA02-2102) usa `build()`. Gestión y Gestión Gerencia ya pasan `workstationNodeID` al visor (en Gestión, AC10-1101 da un PDF por estación). Falta:
  - ~~`Digitalizacion_Template`: la tabla de vista previa y `lastRegisterType` por estación~~ hecho el 2026-10-28
  - ~~Los otros 49 reportes a `build()`~~ hecho el 2026-10-28: los 65 reportes con script usan `build()` (informe en `.claude/docs/qa/reportes-build-informe.md`)
- Tabla "Historial de registros" (última página de los PDF) de los reportes migrados: lee la lista `RegisterHistoryStation` que arma `build()` (la misma consulta más el filtro por estación; usuario, 2026-10-27). La consulta `RegisterHistory` sigue en el reporte sin uso
- ~~`Page/Gestion` (`custom.path`): "'...script' object has no attribute 'split'" en el log al cambiar de fila (el path llega como objeto y `unwrap` solo maneja dict); el PDF sale igual~~ corregido el 2026-10-28 (Gestión y Gerencia)

## Preguntas desde papoitem (fases 2 y 3)

- Simulación del 2026-10-26 (`simulate_all.py --questions-sql`): 246 preguntas fijas de 192 ítems pasan a `papoItemID`; 121 necesitan `UPDATE papoitem` y hay 1 conflicto (mismo ítem con textos distintos). Generar y aplicar el SQL con cada familia, antes de su commit

## Mejoras opcionales (fuera de la estandarización básica)

- Preguntas en una consulta por vista: hoy hay ~3,520 bindings que consultan `papoitem` uno por pregunta en 153 vistas. `papo_core.items.getQuestions(value)` y `getQuestionText(value)` ya existen (sin uso); se probaron y revirtieron en el piloto EC07-0101 barcada por no ser parte del estándar
- `papo_core.ui.getShift(dateTime=None)` existe sin uso: reemplazar los cálculos con `getHour24` (ui.preInsight, sign.autoCloseOpenForms, report x2, custom.shift de Metalurgia FU10-0202_dia y TR11-0102_start, que además tiene el bug de turno)

## Verificaciones pendientes

- Producción (export de F&A del 2026-10-27 10:32): los dropdowns nuevos de `AC10-0201_start` y `_mmto` tienen guardado "Hubo" y el de `AC10-1801_30min` 101; si el operario no elige, el registro guarda ese valor. En develop ya están limpios (`9f05d29`); se corrige en producción al desplegar estas vistas

- Base de prueba: ningún ítem de EA11-0901 (papo 1) tiene el tipo 2 en `papoitem_registertype`, así que el Template nunca muestra el botón "2 hr". La `_2h` se probó puesta un momento en la ruta de `_1h` (2026-10-27); confirmar en producción que el botón existe

- `papo_core.register._getLastRegisterCode` ordena por `ID DESC` en lugar de `RegisterCode DESC` (la regla del proyecto); en la práctica devuelve lo mismo porque ID es creciente

- Scheduled Script de gateway que llama a `papo_core.sign.autoCloseOpenForms("papo_db")`: conexión hardcodeada

- `Page/Gestion`, `custom.signature` (`now(60000)`): cada minuto y en cada sesión abierta consulta todo el historial e inserta una firma tipo 10 "Revisado" con usuario `NA` en los ciclos "En proceso" de más de 180 min (origen de las firmas "NA NA"). Escribe en la base desde un binding de vista, duplica a `autoCloseOpenForms`, puede insertar dos veces si hay dos sesiones abiertas y su llave de ciclo no incluye `WorkstationNodeID`. Decidir si se elimina y se deja solo el cierre automático del gateway
