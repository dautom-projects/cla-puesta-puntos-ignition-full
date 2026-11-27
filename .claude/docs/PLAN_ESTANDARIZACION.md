# Plan: estandarizar los 239 formularios PAPO con objetos estándar

Terminado (2026-10-28). Copiado aquí el 2026-11-14 desde el plan de la sesión, que pasó a ser el del modo tablet.

## Contexto

El piloto `Page/Embedded/Ensamble/Form_EA11-0901_1h_PruebaPiloto` quedó aprobado: campos como objetos `Objects/*` (diseño + comportamiento en un solo lugar), `custom.item` en el formulario leyendo la salida `answer` del objeto, clases `PAPO/Field/*` y tema corregido con alcance `PAPO/Form`. El objetivo ahora es que **todos los formularios sean iguales** y se mantengan desde los objetos, sin cambiar la recolección del procedimiento v2 (`custom.item` en el componente del formulario dentro de `FlexContainerGroupN`, `papo_core.register` sin cambios, mismo orden).

Estudio (2026-10-25, grafo en modo lectura + análisis de las 239 vistas):
- Estructura de la raíz casi uniforme: títulos → Section/Group → [Supervisor] → Observaciones → botones
- Layout: 102 lista, 64 grilla, 19 repeater (OREC), 54 sin campos en grupos (49 `_end` solo con Observaciones)
- 4,555 campos convertibles hoy; 182 más con dos patrones simples (`"-"` si vacío; checkbox con fallback); 52 necesitan objetos nuevos (26 grupos de opción única, 26 fechas); 4 quedan nativos
- ~90 handlers legacy en los botones (`saveStartRegister-*`, `saveStartShift`…) con `"papo_db"`: verificado que ninguna vista ni script de la Project Library los envía (código muerto; el v2 pide quitarlo)
- Los reportes (`papo_core/report/code.py`) buscan las respuestas por `papoItemID`, no por posición, y comparan el texto exacto ("Cumple", "No Cumple", "no cumple"): hay que conservar cada valor tal cual (p. ej. el fallback "No cumple" de 6 checkboxes)
- Los formularios se abren por ruta dinámica desde `Digitalizacion_Template`: no se renombran ni se mueven

Decisiones del usuario: en listas, **fila completa estándar** (un objeto con la pregunta adentro reemplaza contenedor + etiqueta + campo); en grillas, solo el campo (patrón del piloto); **no se usan repeaters** (2026-10-26): en los 19 formularios de OREC cada instancia pasa a ser una fila del grupo, como en las listas (papo_objects v2.8).

## Estado (2026-10-26)

| Fase | Estado | Commits |
|---|---|---|
| 0 Herramientas y objetos | Hecha (objetos v2.5; papo_objects v2.7.1; papo_qa v1.9.2; ui_check v1.3; 26 tests) | varios, hasta `1d00a9c` |
| 1 Pilotos por tipo | Hecha: 6 pilotos con QA 1–7, guardado comparado y PDF | hasta `34c6009` |
| 2 Familia EA11-0901 | Hecha: 6 vistas, etapa 8 en 5 (la `_2h` no tiene botón en la estación de prueba) | `123bf40` |
| 3 Ensamble | Hecha: 10 familias más, 44 vistas, QA 1–7; grafo sin referencias rotas nuevas | `2675d8b`…`8cb09f3` |
| 3 F&A | Hecha: 21 familias, 82 vistas, QA 1–7; etapa 8 en AC10-0201 (5 variantes iguales al original); sin SQL de preguntas | `1898cd8`…`b725bda` |
| 3 Metalurgia | Hecha: 9 familias, 21 vistas; etapa 8 en SO02-1006 (3 variantes); 4 UPDATE de preguntas y 16 textos fijos (PA11-0301); FU10-0202 también (el usuario la guardó en el Designer y quedó canónica; `_dia` deja 42 campos nativos referenciados, en el BACKLOG) | `a05a558`…graph Metalurgia |
| 3 OREC | Hecha: 29 familias, 67 vistas, QA 1–7; 61 repeaters pasados a filas (ninguno queda); etapa 8 en EJ11-0101 (3 variantes iguales al original); 2 UPDATE de preguntas; `RJ07_0101_*` también (el usuario decide qué no se estandariza) | `5c84de4`…graph OREC con RJ07_0101 |
| 3 General/POLY/Cubiertas | Hecha: 8 vistas (3 + 2 + 3), QA 1–7, sin SQL de preguntas; Cubiertas migrada antes al v2 con General como plantilla (decisión del usuario); etapa 8 en General (3 iguales al original) y en la S&A de Cubiertas puesta un momento en la ruta de General | `3dc8d37`…`91c9855` |
| Transversal | Secciones que alcanzan para sus filas (papo_objects v2.9, `fit_sections.py`): 39 vistas ya estandarizadas corregidas | `0bb6573`, `7ab0761`, `2326a1c`, `5bcbd71` |
| 4 Tema global y despliegue | Hecha: parche en todo el tema y sin el bloque `PILOTO PAPO`; en Chrome, 0 diferencias de estilo en 1107 componentes (Overview, Gestión, Template, EJ11-0101, EA11-0901 1 hr); orden de despliegue en `.claude/docs/DESPLIEGUE_ESTANDAR.md`. Sin medir: Designer, hover de botones y tema oscuro | `d87d8ad` |
| 5 Casos manuales | Hecha: de 111 campos nativos pasan a objetos 108 (papo_objects v2.12–2.13, ranges v1.1–1.2, `Objects/NumericField` v2.6 con `inputBounds`; 2 casos a mano: PO11/FU11 y TE11). Quedan nativos a propósito 3: el numérico de dos rangos de CI11 y el `Dropdown_0` de FO10-0100/0601. Etapa 8 en EC07, CA de General, MZ07, PO11-0101-1 y EA11-0901_2h; pruebas en el navegador de EA11-2501_2h, AC10-0201, EA11-1603_1h y TE11-0401 | `7fecfe7`…`7c40ef5` |
| Prueba general (2026-10-27) | Hecha: 69 PAPOs y 209 formularios con el ciclo completo a 1920x1080 y el PDF comparado casilla por casilla. Corregidas 2 regresiones del estándar (scripts que leían `props.value` de objetos; un Guardar que enviaba un handler legacy quitado) y secciones sin `baseBasisPx` (29 vistas); papo_qa v1.14.0 revisa ambas regresiones. Hallazgos de reportes, datos y originales en el BACKLOG. Informe: `.claude/docs/qa/prueba-general-informe.md` | `e9d971a`…`253829d` |
| Reportes con `papo_core.report.build()` (piloto, 2026-10-27) | Hecho el piloto F&A (AC10-0202, AC10-0301, AC10-1101, CA02-2102): `papo_core.report` v2.3.0 con `build()` y filtro por estación (`workstationNodeID`), comparado en sombra en 36 ciclos (`report_shadow.py`) y PDF igual salvo la marca Cumple aprobada. Decisiones del usuario: un formulario por estación; firmas por rol como hoy; ✔ en Cumple de los reprocesados; la tabla "Historial de registros" (última página) también se filtra por estación: lee `RegisterHistoryStation` de `build()`. Gestión ya pasa `workstationNodeID` (PDF por estación, `721a76c`). Segunda familia F&A hecha (AC10-0801, TE11-2601, FO10-0100, FO10-0601, FO10-1701; opción `reprocessedNormalize`). Familia OREC hecha (EJ11-0102, EC11-0101, RJ11-0101, EJ11-0101, EJ07-0101, PO07-0101, SO02-1006) con el estándar de la planta para el turno (decisión del usuario; `papo_core.report` v2.3.1 con `getShift` y `hora_registro`). 2026-10-28: los 49 restantes migrados (5 commits por área) y probados contra el PDF de antes: 25 iguales, 10 con cambios aprobados, 6 explicados (`.claude/docs/qa/reportes-build-informe.md`); `papo_core.report` v2.8.4, 73 tests. Template por estación también (`7aa9287`): vista previa y último tipo de registro por `workstationnodeID` | ver `git log` |

Guía para el equipo: `Procedimiento de estandarizacion v3.md` (Drive, `Pruebas SAT/Desarrollo`; fuente en `.claude/docs/PROCEDIMIENTO_ESTANDARIZACION_V3.md`).

## Lo aprendido en los pilotos (se aplica en adelante)

- **Preguntas desde `papoItemID`** (pedido del usuario): una pregunta fija pasa a leer `papoitem.Description`. Si el texto difiere, se genera el SQL del área y se clasifica: solo tildes/puntos/mayúsculas y errores de la base → `UPDATE` con el texto del formulario; recortes del formulario o errores del formulario → se queda el texto de la base (`.claude/docs/sql/preguntas_texto_base.json`). El usuario aprueba la clasificación antes de tocar la base. Un ítem guardado para varias preguntas de la misma vista (207 en EA11-0901_2h/_4h, intencional) conserva cada texto fijo
- **`papoItemID` fijo** en `custom.item` (`--static-ids`): una sola lógica; los IDs calculados se reemplazan por su valor
- **Rango de los numéricos** desde el script de color del original (`ranges.py`); si su rojo no es un rango cerrado (solo un mínimo), el campo queda nativo
- **Numérico sin valor guardado** responde `""` si no se toca (no `None`)
- **Etapa 8 en la primera familia de cada área**: guardar los registros base desde los originales **antes** de convertir (después ya no hay con qué comparar); luego convertir, guardar con los mismos valores (`ui_check.js`) y `--compare-db --exact`
- **Pruebas en el navegador a 1920x1080**; en develop no hay ClariosAD: el supervisor sin opciones es lo esperado y no se toca
- **Gateway local**: relee el disco cada 10 s y reescribe el recurso; esperar ~15 s tras cada cambio. La prueba gratuita vence cada 2 h (el usuario la reinicia)
- **Compuerta de rendimiento**: GR10 (1206 componentes) abre en ~0,3 s contra ~0,2 s del original: sin excepciones
- **Fin de línea**: git normaliza a LF (`eol=lf`); la etapa 1 no lo marca
- **Sin repeaters**: el repeater `Fundamental Views/Checkbox` se reemplaza por sus filas directo en el grupo (sin contenedor intermedio, nombres `Checkbox`, `Checkbox_0`…, 50 px o el alto del elemento); piloto PO11-0101-2 revisado a 1920x1080
- **Estación de prueba**: `Digitalizacion_Template` abre cualquier formulario por URL (`nodeID/<n>/papoID/<p>/workstationID/<w>/workstationnodeID/<wn>/digitalization`, valores de `workstationnode` + `nodepapo`); no hace falta que la estación tenga el formulario asignado
- **Vistas que el Template no abre** (sin referencia en `papo`, área inexistente): se estandarizan igual si el usuario no dice lo contrario; para probar su guardado se ponen un momento en la ruta de una vista equivalente que sí se abre (como `pilot_swap`), se guarda y se restaura antes de commitear
- **Cierre de área**: correr el grafo una sola vez antes del commit (o restaurar `graph.json`/`catalog.json` de HEAD), para que `CHANGES.md` compare contra la corrida commiteada; los hallazgos de papo-lint que vienen de los originales (nativos, `"papo_db"`) se documentan, no cuentan como nuevos
- **Herramienta de familia**: el script que convierte una familia, corre el QA con grafo y commitea está en el scratchpad de la sesión; pasarlo al repo (`papo-qa/scripts`) antes de F&A

## Estándar final de un formulario

```
root (clase PAPO/Form)
├── títulos (clase text-titles)
├── SectionN (clase por binding del v2) + FlexContainerGroupN
│   ├── lista:  un objeto por fila (pregunta adentro), cada uno con su custom.item
│   └── grilla: celdas del formulario; en cada celda el objeto (pregunta afuera) o valor de tag nativo
├── FlexContainerSupervisor → Objects/Dropdown (options = supervisorOption)
├── TextField de Observaciones (nativo, clase PAPO/Field/Input)
└── botones (button-1 / button-2, solo confirmSave y closeEmbeded)
```

## Pipeline de QA (compuerta de cada parte)

Ninguna parte se commitea si el pipeline no pasa. Herramienta nueva `.claude/skills/papo-qa/scripts/papo_qa.py --views <parte> --baseline <commit>`: compara cada vista contra su versión del commit anterior (`git show`) y deja `.claude/docs/qa/<parte>.md`; sale con error si algo falla.

| # | Etapa | Qué valida |
|---|---|---|
| 1 | Estructura | JSON parsea; serialización Gson canónica; finales de línea iguales al baseline (salvo que git los normalice) |
| 2 | Recolección | Mismos `custom.item` (papoItemID, registerTypeID y sus bindings), mismo orden, mismo contenedor (`FlexContainerGroupN` / `FlexContainerSupervisor`); Observaciones e insights intactos |
| 3 | Respuestas | Por campo convertido, el objeto responde lo mismo que el original: salidas del map (incluido el fallback, p. ej. "No cumple"), `emptyAnswer` = transform original, dropdown por etiqueta o valor según su script, y respuesta inicial (sección sin abrir) = la del campo sin tocar; misma pregunta (o la de `papoitem` ya actualizada), placeholder y `enabled`; mismo rojo fuera de rango que el script de color del original |
| 4 | Flujo v2 | Wrappers estándar (initForm, preInsight, toggleFlexRoot, saveDataRoot, answerRecopile) presentes; sin handlers legacy; sin `"papo_db"` nuevo |
| 5 | Diseño | Raíz con `PAPO/Form`; todo campo es objeto o tiene clase `PAPO/Field/*`; ningún ancho fijo en px en campos; toda clase usada existe |
| 6 | Contrato de objetos | Cada `props.params` que pasa el formulario existe en el objeto con la dirección correcta (`value` inout, `answer` output) |
| 7 | Grafo | ignition-graph sin referencias no resueltas ni mensajes desbalanceados nuevos frente al baseline |
| 8 | Datos (por tipo) | Mismos valores guardados desde el original y desde el estandarizado (`ui_check.js`): `--compare-db <nuevo> <original> --exact` exige mismos ítems, orden y respuestas (las horas por formato) |
| 9 | Visual y rendimiento (por tipo) | A 1920x1080: secciones sin cortes, sin saltos al marcar, valores al cerrar/reabrir, textos y Observaciones guardados, rojo fuera de rango igual al original, PDF del ciclo, tiempo de apertura |

Las etapas 1–7 corren automáticas en cada parte; la 8 y la 9 en cada piloto por tipo (fase 1) y en la primera familia de cada área.

## Partes y commits

Cada parte es un commit propio, solo después de pasar el pipeline. Nunca se mezclan herramientas con formularios en el mismo commit.

| Parte | Contenido | Commit |
|---|---|---|
| 0.1 | Pipeline de QA (`papo-qa`) | `feat: pipeline de QA para formularios` |
| 0.2 | Objetos: `emptyAnswer`, fallback del Checkbox, `OptionGroup`, `DateTime` | `feat: objetos estándar v2.1` |
| 0.3 | `papo_objects.py`: modo fila, modo repeater, limpieza legacy | `feat: papo_objects filas, repeaters y legacy` |
| 0.4 | papo-lint: patrones nuevos | `feat: papo-lint patrones de estándar` |
| 1.x | Un piloto por tipo (lista, repeater, supervisor, opción/fecha, rendimiento) | uno por piloto |
| 2 | Familia EA11-0901 (6 variantes) | `refactor: estándar en EA11-0901` |
| 3.x | Una familia por commit, área por área | `refactor: estándar en <familia>` + `chore: ignition-graph <área>` al cerrar el área |
| 4 | Tema global y retiro del alcance `PAPO/Form` | `feat: tema corregido global` |
| 5.x | Casos manuales (al final) | uno por caso |

Cada commit incluye su reporte de QA y su fila en `DEPLOY_INVENTORY.md`. Deshacer una parte = `git revert <commit>`.

## Fases

### Fase 0 — Completar objetos y herramientas (sin tocar formularios)
- `Objects/*`: parámetro `emptyAnswer` (respuesta cuando el valor está vacío; cubre los 158 `"-"`); Checkbox con `falseValue` desde el fallback del map
- Objetos nuevos: `Objects/OptionGroup` (opción única entre N, `options`, respuesta = etiqueta elegida) y `Objects/DateTime` (formato de la respuesta como parámetro)
- `papo_objects.py`:
  - modo **fila** para listas: reemplaza la fila completa (contenedor + etiqueta + campo) por un objeto con `question` = texto de la etiqueta, `showQuestion: true`; el `custom.item` queda en el objeto en la posición de la fila
  - modo **repeater**: cada instancia → objeto con `custom.item` estático (`registerTypeID` leído de `papoitem` con SELECT al convertir) y `question` = descripción de `papoitem`
  - limpieza de handlers legacy solo si ningún script del proyecto envía ese messageType (consulta al grafo); si no, marca el formulario para revisión
  - reporte por formulario: qué se convirtió, qué quedó nativo y por qué
- `papo-lint`: patrones nuevos (campo nativo convertible, handler legacy, formulario sin `PAPO/Form`)
- Pruebas de la herramienta sobre copias: piloto + un formulario de cada tipo

### Fase 1 — Pilotos por tipo (copias `_PruebaPiloto`, como el actual)
Una copia por tipo: lista (F&A), repeater (OREC), con supervisor (Ensamble start), con grupos de opción y fechas. Revisión en el Designer y un registro guardado por copia, comparado con el original.

**Compuerta de rendimiento:** copia de `F&A/Form_GR10-0501_start` (217 objetos; su sección más grande monta 168 a la vez). Medir apertura de la sección en el Designer y en Chrome contra el original. Mediana actual: 11 objetos por formulario; 10 formularios pasan de 100. Si la carga no es aceptable, en esos 10 la fila estándar se arma con componentes nativos + clases (mismo diseño, sin objeto) y se documenta como excepción.

Fila estándar de lista: alto 50 px (el más común hoy: 48–50 px en ~1,600 filas), pregunta 60 % / campo 40 %.

### Fase 2 — Familia EA11-0901 completa (6 variantes)

### Fase 3 — Por área, un commit por familia
Ensamble (hecha) → F&A → Metalurgia → OREC → General/POLY/Cubiertas. En cada formulario: papo-design + papo_objects (`--legacy --form-class --static-ids`) + `PAPO/Form`.

Pasos de cada área (como se hizo en Ensamble):
1. Checkpoint si hay guardados del Designer (`chore: checkpoint antes de ...`)
2. `simulate_all.py --views <área> --questions-sql <archivo>`: qué pasa, qué falla y el SQL de preguntas
3. Clasificar los `UPDATE` (tildes/puntos, errores de la base, recortes, errores del formulario) y pedir la aprobación del usuario; aplicar en cla-db-papo; los que conservan la base van a `preguntas_texto_base.json`; commit `chore: preguntas del área <área> en papoitem` con el SQL y su rollback
4. Primera familia del área: registros base desde los originales (etapa 8), convertir, guardar de nuevo, comparar y PDF; commit
5. Resto de familias con la herramienta de familia (convierte, QA 1–7 con grafo contra HEAD, fila de inventario y commit; se detiene si algo falla)
6. Cerrar el área: `chore: ignition-graph <área>` (sin referencias rotas nuevas) y papo-lint del área en 0

Reglas: backup en `.claude/backups/<fecha>/`; simulación antes de `--apply`; fila en `DEPLOY_INVENTORY.md`; commit `refactor: estándar en <familia>` (se deshace con `git revert`); los errores de los originales van al BACKLOG y no se corrigen en el mismo commit. No se renombra ni se mueve ningún formulario.

### Fase 4 — Tema y despliegue
Tema corregido global (parche de `.claude/docs/theme/`) cuando todos los formularios automáticos tengan `PAPO/Form`; luego se quita el alcance. Orden de despliegue: `papo_core` (Project Library) → clases `PAPO/` → `Objects/*` → tema del gateway (con reinicio de Perspective) → SQL de preguntas del área en producción → formularios por familia.

### Fase 5 — Casos manuales (al final)
Lo que las herramientas no convierten solas, cada uno con su commit y el mismo pipeline de QA:
- ~~`Metalurgia/Form_FU10-0202_start` (JSON no canónico: guardarlo en el Designer para normalizarlo y luego convertirlo)~~ (hecho en la fase 3)
- ~~Los campos que quedan nativos (lógica propia, referenciados por otro componente, propiedades sin parámetro o un rojo que no es un rango cerrado): revisar los de cada familia en `DEPLOY_INVENTORY.md` (Ensamble: 53)~~ (hecho el 2026-10-27: 108 de 111 a objetos)
- ~~Los 3 formularios de Cubiertas sin wrappers del v2~~ (hecho el 2026-10-26, con la fase 3)
- ~~Variantes que no se pudieron abrir desde la estación de prueba (`EA11-0901_2h`): probar el guardado donde tengan botón~~ (2026-10-27: ninguna estación tiene el botón en la base de prueba; se probó en la ruta de `_1h`, mismo DataAnswer)
- Los formularios marcados por la limpieza legacy, si hubo (la compuerta de rendimiento no marcó ninguno)

## Archivos críticos
- `cla-project/com.inductiveautomation.perspective/views/Objects/*/view.json` (contrato v2)
- `.claude/skills/papo-design/scripts/papo_objects.py`, `papo_design.py`, `rules.json`
- `.claude/skills/papo-lint/scripts/papo_lint.py`
- `cla-project/com.inductiveautomation.perspective/style-classes/PAPO/`
- `gateway-themes/cla-light.css`, `cla-dark.css`
- Docs: `OBJETOS_ESTANDAR.md`, `ESTANDAR_DISENO.md`, `DEPLOY_INVENTORY.md`, `BACKLOG.md`

## Verificación
El pipeline de QA es la verificación: etapas 1–7 en cada parte antes del commit; 8–9 en los pilotos por tipo y en la primera familia de cada área. El pipeline se prueba primero contra el piloto actual (debe pasar) y contra una copia con un error sembrado por etapa (debe fallar), para confirmar que detecta lo que promete.
