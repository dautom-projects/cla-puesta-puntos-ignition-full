# Procedimiento de Estandarización de Formularios PAPO — v3

**Versión:** 3.0.0 · **Fecha:** 2026-10-26 · **Autor:** William M.

**Arquitectura:** la lógica vive en el Project Library package `papo_core` (igual que en la v2) y, desde la v3, el diseño y el comportamiento de cada campo viven en los **objetos estándar** `Objects/*` y en las **clases de estilo** `PAPO/`. El formulario solo tiene estructura, wrappers de una línea y parámetros.

Changelog:

| Versión | Fecha | Cambio |
|---|---|---|
| 1 | 2026-07-05 | "Nuevo Embeded" y "Procedimiento de estandarización": estructura Section / FlexContainerGroup y guardado en un solo registro |
| 2 | 2026-07-20 | Toda la lógica en `papo_core`; la vista solo tiene wrappers |
| 3 | 2026-10-26 | Campos como objetos `Objects/*`, diseño por clases `PAPO/`, preguntas desde `papoItemID`, `papoItemID` fijo, botón Guardar con `papo_core.ui.confirmSave()`, herramientas y pipeline de QA |

---

## Qué cambia frente a la v2

| Tema | v2 | v3 |
|---|---|---|
| Campos de respuesta | Componentes nativos (checkbox, numérico, text field, dropdown) con su diseño y su lógica escritos en el campo | Un objeto `Objects/*` por campo: el objeto tiene el diseño, el mapeo Cumple/No Cumple, el color por rango y la respuesta del dropdown |
| Diseño | Colores, bordes y letra escritos en cada campo | Clases `PAPO/Field/*` y `PAPO/Form` en la raíz; la vista solo tiene layout y bindings |
| Texto de la pregunta | Fijo en la etiqueta o en el checkbox | Sale de `papoitem.Description` por el `papoItemID`: editar la base cambia el formulario |
| `papoItemID` | Fijo o calculado en ejecución (`basePapo` + índice, `parent.custom.papoItemID`, etiqueta hermana…) | Siempre fijo en `custom.item` |
| Botón Guardar | `alerts.showAlert(...)` inline | `papo_core.ui.confirmSave()` |
| Legacy | Se eliminaba `custom.answers` | Además se quitan los handlers de guardado legacy (`saveStartRegister-*`, `saveStartShift`…) que nadie envía |
| Prueba | Manual (paso 11) | Pipeline de QA automático (etapas 1–7) + guardado comparado y revisión visual a 1920x1080 (etapas 8–9) |

**Lo que NO cambia** (es la base de la v2 y de la "Ruta de desarrollo"): la estructura `SectionN` / `FlexContainerGroupN` / `FlexContainerSupervisor`, el `custom.item` `{papoItemID, answer, registerTypeID}` en el componente del formulario, `papo_core.register.recopile` y `save`, un solo INSERT "En proceso" por guardado, y las firmas en `Page/Digitalizacion_Template`.

---

## Reglas que no se rompen

1. El `custom.item` se queda en el componente del formulario dentro de `FlexContainerGroupN` (o `FlexContainerSupervisor`). Nunca se mueve adentro del objeto. Los ítems, sus bindings y su orden deben ser idénticos antes y después.
2. `papo_core.register.recopile` / `save` y el flujo de guardado no se modifican.
3. Los formularios no se renombran ni se mueven: `Digitalizacion_Template` los abre por la ruta `Page/Embedded/<área>/Form_<referencia>_<tipo>`.
4. Las firmas (operario y supervisor) viven en `Page/Digitalizacion_Template` y quedan fuera de este procedimiento.
5. `dbConnection` siempre de `view.custom` o `session.custom`; nunca `"papo_db"` escrito. `papo_core` se llama sin `project.`.
6. Los valores de tag (labels con `custom.item` que muestran un tag) quedan nativos, con la clase `PAPO/Field/TagValue`: un objeto en una sección cerrada no se monta y no podría leer el tag.
7. Un campo con lógica propia que el objeto no reproduce igual queda nativo (con su clase `PAPO/Field/*`). Ejemplos: un dropdown cuya respuesta combina otro valor, un numérico con dos rangos válidos, un campo que un script lee o cambia. Un campo que el resto de la vista solo lee en bindings sí pasa a objeto, con el mismo nombre, y esos bindings leen `props.params.value` (papo_objects v2.12).
8. Los `view.json` no se reescriben con `json.dump` (Ignition usa Gson y escapa `'` `=` `<` `>`): ediciones puntuales o las herramientas, que escriben Gson canónico.
9. Los objetos `Objects/*` no se editan a mano: se generan con `build_objects.py`.
10. Los errores que ya tiene el formulario original (ítems repetidos, grupos que no se guardan, plantillas de reporte rotas) se reproducen tal cual y se anotan en el BACKLOG; se corrigen aparte con `/bug`, nunca en el mismo cambio de estandarización.

---

## Requisito previo (orden de despliegue)

Se despliega en este orden; **lo que una vista usa se despliega antes que la vista**:

1. [ ] `papo_core` en el Project Library (`ui`, `register`, `sign`, `items` con `getRangeColor` y `getQuestionText`)
2. [ ] Clases de estilo `PAPO/` (`style-classes/PAPO/`)
3. [ ] Objetos `Objects/*` (Checkbox, NumericField, TextField, Dropdown, OptionGroup, DateTime, Label)
4. [ ] Bloque del tema con alcance `PAPO/Form` en `cla-light.css` / `cla-dark.css` del gateway (pide reiniciar el módulo Perspective y F5 en los clientes)
5. [ ] El SQL de preguntas de la familia (`UPDATE papoitem`, con su rollback) en la base
6. [ ] Los formularios, por familia

Cada despliegue lleva su fila en `DEPLOY_INVENTORY.md`.

---

## Estructura final de un formulario

```
root (clases: ... PAPO/Form)
├── títulos (clase text-titles)
├── Section1 + FlexContainerGroup1
│   ├── lista:  un objeto por fila (la pregunta va adentro del objeto)
│   └── grilla: cada celda con su objeto (la pregunta es una etiqueta de la grilla) o el valor de tag nativo
├── Section2 + FlexContainerGroup2
│   └── ...
├── FlexContainerSupervisor → Objects/Dropdown (options = view.custom.supervisorOption)
├── TextField de Observaciones (nativo, clase PAPO/Field/Input)
└── botones Guardar (papo_core.ui.confirmSave) y Cancelar (closeEmbeded)
```

---

# Vista: Form_XXXX_tipo (start, end, 1h, 30min, SKU…)

---

## PASO 1 — Sections y grupos (v2, pasos 1 a 4)

- [ ] Grupos hijos directos de `root`, llamados `FlexContainerGroup1..N`, **consecutivos desde 1**: `register.save` cuenta los grupos y recorre `FlexContainerGroup1..N` por nombre; si falta un número, el último grupo nunca se guarda (pasa en `OREC/Form_CU11-0101_start`, que no tiene `FlexContainerGroup7`)
- [ ] Cada grupo con su `SectionN` (hija directa de `root`, mismo número): `ui.toggleSection` los empareja por nombre
- [ ] Contenedor del supervisor llamado `FlexContainerSupervisor`
- [ ] `SectionN.props.style.classes` → Property Binding a `../FlexContainerGroupN.position.display` con Transform Map: `true` → `"button-questions"`, `false` → `"button-questions-2"`, Fallback → `"button-questions"`
- [ ] `SectionN` → `events.dom.onClick`:

```python
sectionIndex = int(self.meta.name.replace("Section", ""))
self.view.getChild("root").toggleFlexRoot(sectionIndex)
```

- [ ] Eliminar `custom.answers` de cada `FlexContainerGroup` y del supervisor (script reactivo legacy, duplica `answerRecopile`)
- [ ] `custom.baseBasisPx` de cada grupo: es el alto con que `toggleSection` abre la sección. Debe alcanzar para todas sus filas con sus márgenes y el padding del grupo (si no, las filas se comprimen y el final queda cortado)
- [ ] Cada `FlexContainerGroupN` con `shrink: 0`: abierto conserva su alto y el formulario hace scroll (si puede encogerse, el navegador lo achica a lo que se ve)

---

## PASO 2 — view.custom (v2, paso 5)

### Eliminar

- [ ] `answers`, `formato`, `test`, `flexGroupCount`, `flexCount`, `refreshSecond`, `dsTable_v3`, `dsTable_vJ`, `changedRegister`

### Crear / verificar

- [ ] `dbConnection` → binding a `session.custom.dbConnection` (persistente)
- [ ] `initialPapoDateTime` → timestamp (`{"$": ["ts", 192, 0], "$ts": 0}`), se setea en onStartup
- [ ] `registerTypeID` → 7 (start), 8 (end) o el del tipo
- [ ] `insights` → con transform (paso 3)
- [ ] `user`, `sign`, `referencePapo`, `fontSize` (17)
- [ ] Con supervisor: `supervisorOption`

---

## PASO 3 — Wrappers de papo_core (v2, pasos 6 a 9)

- [ ] **onStartup de la vista** (nivel view, no del root):

```python
self.custom.initialPapoDateTime = system.date.now()
papo_core.ui.initForm(self)
```

Con supervisor, agregar antes de `initForm`: `self.custom.supervisorOption = papo_core.sign.supervisorOpt(self)`

- [ ] **`view.custom.insights`**: Property Binding a `/root/TextField.props.text` + transform:

```python
return papo_core.ui.preInsight(self, value)
```

- [ ] **Custom method `toggleFlexRoot`** (param `sectionIndex`): `papo_core.ui.toggleSection(self, sectionIndex)`
- [ ] **Custom method `answerRecopile`** (param `flexContainer`): `return papo_core.register.recopile(flexContainer, self)`
- [ ] **Message handler `saveDataRoot`** (solo page scope: `pageScope: true`, `sessionScope: false`, `viewScope: false`): `papo_core.register.save(self)`

---

## PASO 4 — Botones y legacy

- [ ] **Guardar** (`Button_Apply` / `Button_Apply_0`) → `events.dom.onClick`:

```python
papo_core.ui.confirmSave()
```

Muestra la confirmación estándar ("Guardar registro" — "Esta seguro de que desea guardar el registro?" — Si / No) y, al confirmar, envía `saveDataRoot`. Reemplaza el `alerts.showAlert(...)` inline de la v2.

- [ ] **Cancelar** (`Button_Apply_1`):

```python
system.perspective.sendMessage(messageType="closeEmbeded", payload={"estado": False,}, scope="session")
```

- [ ] Quitar los handlers de guardado legacy del root (`saveStartRegister-*`, `saveStartShift`, versiones viejas de `saveDataRoot`) **solo si ningún script ni vista los envía** (verificarlo en el grafo del proyecto). Si alguno se usa, no se quita y se marca la vista para revisión
- [ ] Ningún `def` inline de recolección o guardado en el root: solo los wrappers

---

## PASO 5 — Diseño

- [ ] Agregar la clase `PAPO/Form` a `root.props.style.classes` (sin quitar las que tenga)
- [ ] Cada campo con `custom.item` es un objeto `Objects/*` (paso 6) o, si queda nativo, tiene su clase:

| Clase | Campo nativo |
|---|---|
| `PAPO/Field/Input` | numérico, text field, date-time; TextField de Observaciones |
| `PAPO/Field/Dropdown` | dropdown |
| `PAPO/Field/Checkbox` | checkbox |
| `PAPO/Field/TagValue` | label que muestra un valor de tag |

- [ ] Nada de colores, bordes ni tipografía escritos en el campo (`props.style` / `props.textStyle`): eso lo da la clase. En la vista solo quedan `position`, márgenes entre campos y bindings
- [ ] Sin anchos fijos en px: en una fila el ancho lo da el `basis`; en una columna que no estira, `width: 100%`
- [ ] Títulos con la clase `text-titles` (el color sale del tema)

---

## PASO 6 — Campos como objetos estándar

El componente del formulario pasa a ser un `ia.display.view` del objeto. **El `custom.item` se queda en ese componente** y su `answer` lee la salida del objeto:

- `custom.item.papoItemID`: fijo (paso 8)
- `custom.item.registerTypeID`: el mismo del original (fijo o con su binding a `view.custom.registerTypeID`)
- `custom.item.answer` ← Property Binding a `this.props.params.answer`
- `props.params.value`: valor inicial del campo (el guardado en el Designer); es **inout**: si la sección se cierra y se reabre, el objeto vuelve con lo que tenía
- `props.params.answer`: la respuesta del campo sin tocar (checkbox: `falseValue`; texto: `""`; numérico: `null`; grupo de opción: `"-"`). Es la que se guarda si el operario nunca abre la sección, porque un objeto en una sección cerrada no se monta
- `props.params.fontSize` ← binding a `view.custom.fontSize`

| Campo original | Objeto | Parámetros propios | Respuesta |
|---|---|---|---|
| Checkbox con map true/false | `Objects/Checkbox` | `trueValue` ("Cumple"), `falseValue` ("No Cumple" o el fallback del map); `trueText` / `falseText` si el texto cambia con el estado (✔ / ✘) | `trueValue` / `falseValue` |
| Numérico | `Objects/NumericField` | `minValue`, `maxValue` (rojo fuera de rango con `papo_core.items.getRangeColor`), `placeholder` ("Escriba aqui"), `questionAsPlaceholder` | el valor |
| Text field | `Objects/TextField` | `placeholder`, `questionAsPlaceholder` | el texto |
| Dropdown | `Objects/Dropdown` | `options` (fijas o con el mismo binding), `answerFrom` (`"label"` o `"value"`), `placeholder` ("Seleccionar"), `showClearIcon` | la etiqueta o el valor elegido |
| Varios checkbox que son una sola opción entre N | `Objects/OptionGroup` | `options` (textos), `questionBasis` (ancho de la pregunta) | el texto elegido o `"-"` |
| Selector de hora / fecha | `Objects/DateTime` | `pickerType` ("time"), `format` ("h:mm:ss a"), `startNow: true` (arranca con la hora en que se abre el formulario, como el campo nativo) | el valor con `format` |

Parámetros comunes: `question`, `papoItemID`, `showQuestion`, `questionBasis`, `enabled` (`false` = solo lectura, como el original), `emptyAnswer` (respuesta cuando el valor está vacío, p. ej. `"-"`).

### Lista o grilla

- [ ] **Lista** (grupo en columna): la fila completa (contenedor + etiqueta de pregunta + campo) se reemplaza por **un objeto con la pregunta adentro** (`showQuestion: true`), alto estándar 50 px (o el de la fila si era mayor), pregunta 60 % / campo 40 %
- [ ] **Grilla** (y grupos en fila, como el supervisor): solo el campo; la celda y la etiqueta de la grilla quedan como estaban (`showQuestion: false`)
- [ ] **Repeater** (`Fundamental Views/Checkbox`, formularios de OREC): **no se usa**. Cada instancia pasa a ser una fila del grupo, igual que una lista: un `Objects/Checkbox` por pregunta con su `custom.item` fijo (`papoItemID` y `registerTypeID`), nombre normal (`Checkbox`, `Checkbox_0`…) y alto de 50 px (o el del elemento del repeater)

### Ejemplo (checkbox de una fila de lista, `F&A/Form_AC10-0201_start`)

```json
{
  "custom": {"item": {"papoItemID": 6746}},
  "meta": {"name": "Checkbox8"},
  "position": {"basis": "141px", "shrink": 0},
  "propConfig": {
    "custom.item.answer": {"binding": {"config": {"path": "this.props.params.answer"}, "type": "property"}},
    "custom.item.registerTypeID": {"binding": {"config": {"path": "view.custom.registerTypeID"}, "type": "property"}},
    "props.params.fontSize": {"binding": {"config": {"path": "view.custom.fontSize"}, "type": "property"}},
    "props.params.papoItemID": {"binding": {"config": {"path": "this.custom.item.papoItemID"}, "type": "property"}}
  },
  "props": {
    "params": {"answer": "No Cumple", "falseValue": "No Cumple", "question": "", "trueValue": "Cumple", "value": false},
    "path": "Objects/Checkbox"
  },
  "type": "ia.display.view"
}
```

### Rango de los numéricos

- [ ] El rango (`minValue`, `maxValue`) tiene que pintar de rojo **exactamente los mismos valores** que el script de color del original. Los originales lo escriben de varias formas: `rang_down`..`rang_up`, `start ± rang`, `start · (1 ± porc)`, `getRangeColor` con límites fijos, o el máximo `"9999…"` en texto. La herramienta ejecuta ese script como Jython 2 con valores de prueba y deduce el rango
- [ ] Solo un mínimo (p. ej. "mayor a 12,75"): el máximo es `"9999999999999999999999999"`, como ya lo hacían los formularios (decisión del 2026-10-27)
- [ ] Límites que dependen de otro campo (p. ej. el tamaño de batería): `minValue` y `maxValue` quedan enlazados a ese campo; la QA compara los límites en cada estado
- [ ] Un script que lee un `custom` que el campo no tiene nunca pinta: el objeto queda sin rango. Si el rojo no es un rango cerrado (dos rangos válidos), el campo **queda nativo**
- [ ] Dentro de rango el objeto muestra el texto negro y el borde gris; fuera de rango, texto y borde rojos

### Supervisor

- [ ] `FlexContainerSupervisor` → `Objects/Dropdown` con `answerFrom: "label"` y `options` ← `view.custom.supervisorOption` con el mismo transform que tenía (lista vacía → "No hay supervisores disponibles")
- [ ] En el gateway de desarrollo no hay ClariosAD: la lista queda vacía y es lo esperado (en producción funciona). No se modifica `supervisorOpt` ni el user source para probarlo

---

## PASO 7 — Preguntas desde papoItemID

Para estandarizar, el texto de cada pregunta sale de la base: editar `papoitem.Description` cambia el formulario sin tocar la vista.

- [ ] Pregunta del objeto: `question: ""` + `papoItemID` → el objeto muestra `papoitem.Description` (`papo_core.items.getQuestionText`)
- [ ] Si el texto fijo del formulario es distinto al de la base, se actualiza **la base**: script `UPDATE papoitem SET Description = ...` con su rollback, primero en la base de pruebas y después en producción (antes de desplegar el formulario)
- [ ] Se quitan los recortes que el formulario hacía sobre la descripción (p. ej. quitar "Tanque de Soda, ")
- [ ] Quedan fijas: las etiquetas informativas (no están en `papoitem`), los subtítulos y los encabezados de grilla de valores de tag

---

## PASO 8 — papoItemID fijo

Una sola lógica para todos los formularios: el `papoItemID` es un número fijo en `custom.item`.

- [ ] Reemplazar cada `papoItemID` calculado en ejecución (`basePapo` + índice tomado del nombre, `parent.custom.papoItemID`, el de una etiqueta hermana…) por su valor
- [ ] Quitar los bindings desactivados (`enabled: false`)
- [ ] Verificar que el ID fijo es el que hoy guarda el formulario: compararlo con su último registro en `registerhistory`
- [ ] Un ID que en ejecución da `null` (p. ej. el supervisor de EA11-1601 / EA11-2601 antes de su corrección) es un bug del original: se corrige aparte

---

## PASO 9 — Probar

Se prueba **contra el formulario original**, con los mismos datos. Todo lo visual, a **1920 x 1080** (la resolución para la que está hecha la aplicación).

1. [ ] **QA automático (etapas 1–7)**: estructura, recolección, respuestas, flujo v2, diseño, contrato de objetos y grafo (ver "Pipeline de QA")
2. [ ] **Guardado (etapa 8)**: guardar el mismo registro desde el original y desde el estandarizado con los mismos valores y comparar los dos `DataAnswer`: mismos ítems, mismo orden, mismas respuestas (las horas del día se comparan por formato)
3. [ ] **Visual (etapa 9)**, en el flujo real:
   - [ ] Las secciones abren y cierran, y su final no queda cortado
   - [ ] Marcar un checkbox o elegir una opción no mueve la página; las opciones quedan en una línea
   - [ ] Los valores siguen al cerrar y reabrir la sección
   - [ ] Los textos se escriben y se guardan (también Observaciones)
   - [ ] Numérico fuera de rango en rojo, en los mismos campos que el original
   - [ ] Tiempo de apertura del formulario parecido al original
4. [ ] **Reporte PDF** del registro guardado (Gestión → fila del registro): las columnas del estandarizado y del original salen iguales
5. [ ] Lo que falle por un error del original se anota en el BACKLOG (no se corrige en este cambio)

---

## PASO 10 — Registrar y commitear

- [ ] Un commit por familia (`refactor: estándar en <familia>`), solo después de pasar el QA; herramientas y formularios nunca en el mismo commit
- [ ] Reporte de QA en `.claude/docs/qa/` y fila en `DEPLOY_INVENTORY.md`
- [ ] Si hubo guardados desde el Designer sin commit, primero un checkpoint (`chore: checkpoint antes de ...`)
- [ ] Deshacer = `git revert <commit>`

---

# Con las herramientas (camino recomendado)

Las herramientas hacen los pasos 1 a 8 con verificación: si la recolección (ítems, bindings, orden, contenedor) cambia, la vista no se escribe. Simulan por defecto; `--apply` escribe con backup.

```bash
# 1. Diseño (clases PAPO/Field/*): simular y luego aplicar
python3 .claude/skills/papo-design/scripts/papo_design.py --views "<vista>"
python3 .claude/skills/papo-design/scripts/papo_design.py --views "<vista>" --apply

# 2. Objetos, legacy, PAPO/Form, papoItemID fijo y SQL de preguntas
python3 .claude/skills/papo-design/scripts/papo_objects.py --views "<vista>" --legacy --form-class --static-ids --questions-sql <archivo.sql>
python3 .claude/skills/papo-design/scripts/papo_objects.py --views "<vista>" --legacy --form-class --static-ids --questions-sql <archivo.sql> --apply

# 3. QA contra el original (etapas 1–7) y lint
python3 .claude/skills/papo-qa/scripts/papo_qa.py --views "<vista>" --graph
python3 .claude/skills/papo-lint/scripts/papo_lint.py --views "<vista>"
```

El SQL de preguntas se aplica en la base antes de correr el QA: la etapa 3 no deja pasar una pregunta cuyo texto todavía no está en `papoitem`.

### Probar en el flujo real sin tocar el original

```bash
# Copia estandarizada del formulario (_PruebaPiloto), con su reporte de QA
python3 .claude/skills/papo-qa/scripts/make_pilot.py "Page/Embedded/F&A/Form_AC10-0201_start"

# Poner el piloto en la ruta del original (solo en el gateway local) y restaurarlo
python3 .claude/skills/papo-qa/scripts/pilot_swap.py on "Page/Embedded/F&A/Form_AC10-0201_start"
python3 .claude/skills/papo-qa/scripts/pilot_swap.py off --all

# Comparar dos registros guardados (piloto contra original)
python3 .claude/skills/papo-qa/scripts/papo_qa.py --compare-db <ID piloto> <ID original> --exact
```

- No commitear con un intercambio activo (`pilot_swap.py status`)
- Después de `on` / `off`, esperar ~15 s: el gateway relee el disco cada 10 s y reescribe el recurso
- La prueba de UI y guardado en el navegador es `scripts/ui_check.js`: se ejecuta dentro del cliente Perspective, en una página nueva (borrar `perspective-tab-id` de `sessionStorage`), a 1920x1080. Llena todo con valores fijos (checkbox marcados, la última opción de cada grupo, numéricos 7, textos "QA", horas 08:15), guarda por la confirmación estándar y reporta cortes, saltos de página, tiempo de apertura y colores de rango. La misma corrida sobre el original y sobre el piloto da dos registros que deben ser iguales

### Todo el proyecto

```bash
python3 .claude/skills/papo-qa/scripts/simulate_all.py --questions-sql <archivo.sql>
```

Lee los originales de git, aplica el estándar en una carpeta temporal y corre el QA sobre cada formulario; no escribe nada en el proyecto. Resultado al 2026-10-26: 237 formularios simulados, 209 pasan; 25 esperan su SQL de preguntas y 3 son casos manuales (Cubiertas).

---

## Pipeline de QA

| # | Etapa | Qué valida |
|---|---|---|
| 1 | Estructura | JSON parsea, Gson canónico, mismo fin de línea |
| 2 | Recolección | Mismos `custom.item` (por el `papoItemID` real), mismos bindings, orden y contenedor; `custom.insights` y Observaciones intactos |
| 3 | Respuestas | Cada objeto responde igual que el campo original con valores de prueba; misma respuesta sin abrir la sección; misma pregunta, placeholder y `enabled`; mismo rojo fuera de rango |
| 4 | Flujo v2 | Wrappers de `papo_core` presentes, sin `"papo_db"` nuevo, sin handlers legacy |
| 5 | Diseño | `PAPO/Form` en la raíz, todo campo es objeto o tiene `PAPO/Field/*`, sin anchos fijos, las secciones alcanzan para sus filas |
| 6 | Contrato | Cada parámetro que pasa el formulario existe en el objeto (`value` inout, `answer` output) |
| 7 | Grafo | Sin referencias rotas ni mensajes desbalanceados nuevos |
| 8 | Datos | Dos registros guardados con los mismos valores (original y estandarizado) son iguales |
| 9 | Visual | Revisión en el navegador a 1920x1080 y PDF (paso 9) |

Una vista no se commitea si no pasa las etapas 1–7.

---

# Vista: Overview_Papos, Embedded_PAPO y reportes (sin cambios desde la v2)

- **Overview_Papos**, binding de la lista filtrada → `return papo_core.overview.getPapoListFiltered(value)`
- **Embedded_PAPO**, binding del path → `return papo_core.overview.getCardPath(value)`
- **Reporte**, Data Source Script → `papo_core.report.extractReportDataAuto(data)` (o `extractReportData(data, sections)` cuando el reporte agrupa por secciones). Hoy solo 6 de las 54 plantillas de Andina lo llaman; el resto todavía tiene su propio script (pendiente, fuera de este procedimiento). Los reportes buscan cada respuesta por `papoItemID` y comparan el texto exacto ("Cumple", "No Cumple"): por eso el estándar conserva cada respuesta tal cual

---

## Resumen de wrappers

| Ubicación | Wrapper |
|---|---|
| Section → onClick | `toggleFlexRoot(sectionIndex)` |
| view → onStartup | `initialPapoDateTime` + `papo_core.ui.initForm(self)` (+ `supervisorOpt` si aplica) |
| view.custom.insights → transform | `papo_core.ui.preInsight(self, value)` |
| root → toggleFlexRoot | `papo_core.ui.toggleSection(self, sectionIndex)` |
| root → answerRecopile | `papo_core.register.recopile(flexContainer, self)` |
| root → saveDataRoot | `papo_core.register.save(self)` |
| Botón Guardar → onClick | `papo_core.ui.confirmSave()` |
| Botón Cancelar → onClick | `sendMessage("closeEmbeded", scope="session")` |
| Campo → `custom.item.answer` | `this.props.params.answer` (salida del objeto) |
| Overview filtrado → transform | `papo_core.overview.getPapoListFiltered(value)` |
| Embedded_PAPO path → transform | `papo_core.overview.getCardPath(value)` |
| Reporte → data source | `papo_core.report.extractReportDataAuto(data)` |

---

## Casos manuales

- `Cubiertas/Form_PL11-0101-CA_start`, `-CU_start`, `-S&A_start`: sin los wrappers de la v2 (su `answerRecopile` tiene lógica propia); se estandarizan a mano
- `Metalurgia/Form_FU10-0202_start`: JSON no canónico; guardarlo en el Designer para normalizarlo y luego aplicar las herramientas
- Los campos que quedan nativos se revisan uno por uno (fase 5, 2026-10-27: de 111 quedan 3 campos nativos a propósito: el numérico de dos rangos de CI11-0101 y el `Dropdown_0` de FO10-0100 y FO10-0601; ver `DEPLOY_INVENTORY.md`)

---

## Documentos de referencia (repositorio)

- `OBJETOS_ESTANDAR.md`: contrato de cada objeto y condiciones
- `ESTANDAR_DISENO.md`: clases `PAPO/`, tema y despliegue por fases
- `CONTEXT_AUTOMATIZACION_JSON.md`: JSON exacto de cada wrapper
- `BACKLOG.md`: errores de los formularios originales y de los reportes encontrados con los pilotos
- `DEPLOY_INVENTORY.md`: qué se cambió y en qué orden desplegarlo
- Pilotos (uno por tipo de formulario, probados contra su original): `Ensamble/Form_EA11-0901_1h` (grilla y valores de tag), `Ensamble/Form_EA11-1601_start` (lista con supervisor), `F&A/Form_AC10-0201_start` (lista, grupo de opción y rangos), `F&A/Form_GR10-0501_start` (horas y rendimiento, 217 objetos), `OREC/Form_CU11-0101_start` (grupos de opción), `OREC/Form_PO11-0101-2_start` (numéricos y campo deshabilitado)
