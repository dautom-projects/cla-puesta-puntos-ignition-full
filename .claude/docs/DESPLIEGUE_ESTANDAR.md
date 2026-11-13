# Despliegue del estándar de formularios a producción

Orden para llevar a producción (Ignition 8.1.19) lo que se hizo en el repo: wrappers del v2, objetos estándar, clases `PAPO/`, tema corregido, preguntas desde `papoItemID` y los formularios estandarizados. Cada recurso tiene su fila en `DEPLOY_INVENTORY.md` (qué cambió, cómo se verificó y su commit). Se despliega compartiendo el recurso completo, como hasta ahora.

Regla general: **lo que un recurso llama va antes que el recurso**. Si un paso falla, se detiene ahí; los pasos anteriores no dependen de los siguientes.

## Orden

| # | Qué | Dónde (repo → gateway) | Por qué va en ese lugar | Verificar |
|:-:|---|---|---|---|
| 1 | Project Library `papo_core` (y `db`, `sql`) | `cla-project/ignition/script-python/` | Los formularios y objetos llaman `register.recopile` y `save`, `ui.initForm`, `preInsight`, `toggleSection`, `confirmSave`, `getSecurityImage`, `items.getRangeColor`, `getQuestionText` y `sign.supervisorOpt` | Sin errores de script en el log del gateway al abrir un formulario viejo |
| 2 | Clases de estilo `PAPO/Form`, `PAPO/Field/Input`, `Dropdown`, `Checkbox`, `TagValue` | `cla-project/com.inductiveautomation.perspective/style-classes/PAPO/` | Los objetos y los formularios las usan; sin ellas los campos salen sin bordes ni letra | Las clases aparecen en el Designer |
| 3 | Objetos `Objects/Checkbox`, `TextField`, `NumericField`, `Dropdown`, `Label`, `OptionGroup`, `DateTime` | `cla-project/com.inductiveautomation.perspective/views/Objects/` | Los formularios estandarizados los embeben | Abrir cada objeto en el Designer |
| 4 | Tema del gateway `cla-light.css` y `cla-dark.css` | `gateway-themes/` → `data/modules/com.inductiveautomation.perspective/themes/`; guardar antes una copia del tema de producción; reiniciar el módulo Perspective (o el gateway) y F5 en los clientes | Corrige el tema para **todas** las vistas (ver "Tema global"); no depende de los formularios, pero los estandarizados se revisaron con él | El CSS servido (`/data/perspective/themes/cla-light.css`) no tiene `boder-color` ni `width: 150px` |
| 5 | SQL de preguntas en la base de producción | `.claude/docs/sql/` (cada archivo trae su rollback) | Los formularios estandarizados leen la pregunta de `papoitem.Description`; sin el SQL mostrarían el texto viejo | El `SELECT` de los ítems del archivo devuelve el texto nuevo |
| 6 | Formularios por área | `cla-project/com.inductiveautomation.perspective/views/Page/Embedded/<área>/Form_*` | Al final: necesitan todo lo anterior | Abrir y guardar un registro por área (como la etapa 8) |

### Paso 5: archivos SQL, en este orden

1. `2026-10-22_FU10-0202_preguntas.sql` (tildes del papo 1102 y los ítems 12374–12376; idempotente)
2. `2026-10-26_preguntas_pilotos.sql` (11 ítems de EA11-0901)
3. `2026-10-26_preguntas_EA11-0901.sql`
4. `2026-10-26_preguntas_Ensamble.sql` (72 `UPDATE`)
5. `2026-10-26_preguntas_Metalurgia.sql` (4 `UPDATE`)
6. `2026-10-26_preguntas_OREC.sql` (2 `UPDATE`)
7. `2026-10-27_tildes_papoitem.sql` (tildes y símbolos mal codificados: 62 ítems y `registertype` 13; cada `UPDATE` solo cambia el texto si sigue roto, así que puede ir en cualquier momento)

8. `2026-11-13_codificacion_papoitem.sql` (después de los anteriores): diagnóstico, respaldo (`papoitem_bak_20261113`, `registertype_bak_20261113`) y reparación de los símbolos raros (`VerificaciÃ³n` → `Verificación`) que quedan si un script se ejecutó leyendo el UTF-8 como Windows-1252. Al final lista lo que queda para revisar a mano

F&A y General/POLY/Cubiertas no tienen SQL. Un área puede desplegarse sin las demás, pero siempre con su SQL antes que sus formularios.

**Codificación de los scripts (2026-11-13):** todos los `.sql` son solo ASCII: cada tilde va como `NCHAR(n)` (`N'Verificaci' + NCHAR(243) + N'n'`), así que da igual con qué codificación los abra SSMS o sqlcmd. Antes estaban en UTF-8 sin BOM: abiertos como Windows-1252, escribían `VerificaciÃ³n` en `papoitem` (los símbolos raros que se vieron en producción). Un script nuevo se pasa por `python3 .claude/skills/papo-qa/scripts/sql_encoding.py ascii <archivo.sql>` (`papo_objects.py --questions-sql` ya los genera así).

### Paso 6: formularios

Un commit por familia (`refactor: estándar en <familia>`), así que una familia se despliega o se revierte sola. Orden sugerido, el mismo en que se probaron: Ensamble, F&A, Metalurgia, OREC, General/POLY/Cubiertas.

- Las copias `_PruebaPiloto` son de prueba y el Template no las abre: no hace falta llevarlas
- Las copias `F&A/Form_* D` y `F&A/Form__end` quedan como están (decisión del usuario)
- `Metalurgia/Fundamental Views/Checkbox` ya no la usa ningún formulario (BACKLOG)

## Después del estándar: reportes con `build()`, estación y correcciones (2026-10-27 / 28)

Va después de los pasos 1–6 (o junto con ellos, respetando el orden). Filas de cada recurso en `DEPLOY_INVENTORY.md` con fecha 2026-10-27 y 2026-10-28.

| # | Qué | Dónde | Por qué va en ese lugar | Verificar |
|:-:|---|---|---|---|
| 7 | Project Library `papo_core`: `report` v2.8.6, `register` v1.1.1, `ui` v1.3.0, `sign` v1.3.0 (cierre automático; antes de la próxima corrida de 06:10, 14:10 o 22:10), `items` (`getCycleSum` v1.1.0, `getCycleRegisters`, `formatTagTime`); y `Objects/DateTime` v2.7 (`displayFormat`) | `cla-project/ignition/script-python/papo_core/` | Los 65 reportes llaman `papo_core.report.build()` / `monthGrid` / `extractShiftChecklist`; `register` lee el último RegisterCode por `RegisterCode DESC` y `ui` arregla la hora de las observaciones de todos los formularios | 74 tests (`tests/test_report_build.py`) y 9 del cierre automático (`tests/test_auto_close.py`); sin errores de script al abrir un formulario y un PDF |
| 8 | Los 65 reportes | `cla-project/com.inductiveautomation.reporting/reports/` (`data.bin`) | Necesitan el paso 7. Sin estación (Gestión vieja) leen el ciclo por nodo, como antes | El PDF de un ciclo por área desde Gestión; informe `.claude/docs/qa/reportes-build-informe.md` |
| 9 | `Page/Gestion` y `Page/Gestion Gerencia` (con la Project Library `sql`: `papoByArea` y `papoByNode` con las celdas; y en Gestión el fin de los periodos al final del minuto) | `views/Page/` | Pasan `workstationNodeID` al visor (PDF solo de la estación) y la ruta del reporte sin error; los reportes viejos ignoran el parámetro, así que el orden 8 / 9 no rompe nada | Cambiar de fila sin error en el log; el historial del PDF solo con la estación |
| 10 | `Page/Digitalizacion_Template` | `views/Page/` | La vista previa y el último tipo de registro por estación | Una estación no ve el ciclo de otra con el mismo código |
| 11 | Correcciones de formularios | `views/Page/Embedded/`: `Metalurgia/Form_FU10-0202_dia`, `Form_TR11-0102_start`, `Ensamble/Form_EA11-1601_start`, `F&A/Form_GR10-0501_start` (IDs y niveles), `F&A/Form_FO10-0601_input`, `OREC/Form_PO07-0101_start` (fila 15 y etiquetas del PLC), `OREC/Form_CU11-0101_start`, `OREC/Form_RJ07-0101_start`, `Ensamble/Form_EA11-4200_2h`, `Ensamble/Form_EA11-1101_1h`, `F&A/Form_TE11-0601_start` / `_30min` / `_SKU` (etiquetas del PLC a `item_dev`), `F&A/Form_GR10-0501_start` (rotación con fecha, inventario final), `F&A/Form_AC10-0202-SLI_*` (Llena de agua como check), `F&A/Form_FO10-0100_input` (tabla de ingresos del ciclo, total del formulario, horas) | Después de su familia del paso 6 y del paso 7 (`getShift`) | Abrir y guardar un registro de cada uno |
| 12 | Editor de nodos `Page/PopUps/CreateOrEditNode-Clarios` | `views/Page/PopUps/` | Independiente (MES Core) | Crear un nodo CELL de prueba con el Topic vacío |
| 13 | SQL del nodo de la segunda estación de CG10-0101 | `.claude/docs/sql/2026-10-27_nodo_CG10-0101_cell.sql` | Solo si en producción el nodo tiene el mismo ID (1001), `Type = 'Workstation'` y `Topic = 'PC'`: el archivo es idempotente y no toca otro nodo. Confirmar antes con un `SELECT` | El Template abre CG10-0101 en esa estación y Gestión encuentra su reporte |

Los reportes no se pueden abrir en develop sin ciclos de prueba; los 8 sin ciclos tienen el mismo script que uno probado (informe de la prueba).

## Prueba de firmas en producción (después del despliegue)

En develop las firmas se probaron con usuarios de prueba de la fuente `default` (ClariosAD solo existe en producción; `verificacion-fa-orec.md`). En producción, con un operario y un supervisor reales de ClariosAD:

1. El operario guarda un registro y el supervisor firma desde el popup **en el PC de la estación**: "Firma Exitosa"
2. El mismo supervisor intenta firmar **desde otro PC**: "Estación no válida"
3. El operario firma; en el PDF desde Gestión salen su nombre en la casilla del operario y el del supervisor en la suya
4. Revisar en `registerhistory` que la hora del "Revisado" del popup sea la del resto del ciclo: desde el 2026-10-29 las tres firmas del supervisor (popup, Template y Gestión) guardan la hora del gateway. El popup es la única que no se pudo probar de punta a punta en develop (sus roles salen de ClariosAD)

## Tema global

Desde el 2026-10-26 el tema no tiene el bloque `PILOTO PAPO` con alcance `.psc-PAPO\/Form`: el parche (`.claude/docs/theme/*.fix.patch`) se aplicó a todo el tema, así que la corrección llega a todas las vistas y el Designer dibuja igual que los navegadores.

- Cierra `:root`, que nunca se cerraba: las reglas de botones, Sections, popup, checkbox, dropdown e inputs dejan de estar anidadas (el Designer y los navegadores sin CSS Nesting las descartaban)
- `boder-color` → `border-color` en los bordes de hover de los botones
- Los dropdowns ya no tienen `width: 150px` fijo: toman el ancho de su contenedor
- La regla de inputs apunta a los componentes reales (text field y `numeric-entry-field`) y sin `!important`, así que no tapa los colores por rango

Las 65 reglas del bloque piloto están en el tema global con las mismas declaraciones. Copia versionada: `gateway-themes/`.

Verificado en PAPOS el 2026-10-27, en Chrome a 1920x1080: foto de los estilos calculados (14 propiedades del componente y de su elemento interno) antes y después de instalar el tema, en Overview, Gestión, el Template de EJ11-0101, EJ11-0101 Inicio (sus 4 secciones) y EA11-0901 1 hr. Son 1107 componentes visibles (1013 etiquetas, 37 numéricos, 29 checkbox, 12 dropdowns, 10 botones, 4 campos de texto y 2 fechas), con **0 diferencias**. Chrome ya aplicaba las reglas anidadas en `:root` (soporta CSS Nesting), así que en los navegadores modernos nada se mueve; lo que cambia es el Designer y los navegadores sin nesting, que ahora las reciben. Sin medir: los bordes de hover de los botones (`boder-color`), el tema oscuro y el Designer.

## Revertir

- Un formulario o familia: `git revert <commit>` y desplegar la vista anterior
- Preguntas: el rollback comentado al final de cada SQL
- Tema: copiar al gateway el de producción guardado antes del paso 4 (o el de `gateway-themes/` del commit anterior a `feat: tema corregido global`) y reiniciar Perspective
- Library, clases y objetos: son nuevos o compatibles con los formularios viejos; no hace falta revertirlos para volver un formulario atrás
