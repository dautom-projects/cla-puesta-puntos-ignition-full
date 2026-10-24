# Objetos estándar de PAPO

Vistas reutilizables para los campos de los formularios Form_*, en
`cla-project/com.inductiveautomation.perspective/views/Objects/`. Reemplazan las ~123 variantes de bindings con las que hoy se arman checkbox, text field, numeric, dropdown y label (inventario del 2026-10-22: 5,539 campos con `custom.item` en 238 vistas).

Piloto: `Page/Embedded/Ensamble/Form_EA11-0901_1h_PruebaPiloto` (copia de `Form_EA11-0901_1h`, 68 campos como objetos embebidos, 2026-10-24). La adopción va formulario por formulario (ver "Aplicación").

## Contrato común

Cada objeto es una fila (`root` flex, `alignItems: center`). El componente que guarda la respuesta se llama siempre `Field` y tiene `custom.item = {papoItemID, answer, registerTypeID}`.

| Parámetro | Dirección | Default | Uso |
|---|---|---|---|
| `papoItemID` | input | null | Ítem de la pregunta |
| `registerTypeID` | input | null | Tipo de registro del formulario (el `view.custom.registerTypeID` de la vista que lo usa) |
| `fontSize` | input | 17 | Tamaño de letra de pregunta y campo |
| `question` | input | "" | Texto de la pregunta que da el formulario; vacío = descripción de `papoitem` |
| `value` | **inout** | según el objeto | Valor del campo (Checkbox, TextField, NumericField, Dropdown). Queda guardado en el formulario, así que la respuesta no se pierde si la sección se cierra y se vuelve a abrir |
| `item` | **output** | {} | `{papoItemID, answer, registerTypeID}`, enlazado a `/root/Field.custom.item` |

- Texto de la pregunta: `papo_core.items.getQuestionText(value)` con `{papoItemID, question, showQuestion, dbConnection}`. Si `question` trae texto se usa ese; si la pregunta está oculta (`showQuestion` false) no consulta; si no, consulta `papoitem` (sin SQL en la vista). Los textos de `papoitem` no tienen tildes y traen IZQ/DER, setpoints y numeración, así que los formularios pasan su propio texto.
- Conexión: `view.custom.dbConnection` enlazado a `session.custom.dbConnection`.
- Filas con pregunta separada (TextField, NumericField, Dropdown, Label): `showQuestion` (true), `questionBasis` ("450px") y `fieldBasis` ("224px").

## Objetos

| Objeto | Componente `Field` | Respuesta (`item.answer`) | Parámetros propios |
|---|---|---|---|
| `Objects/Checkbox` | `ia.input.checkbox` (la pregunta es su texto) | `trueValue` si está marcado, `falseValue` si no | `trueValue` ("Cumple"), `falseValue` ("No Cumple") |
| `Objects/TextField` | `ia.input.text-field` | `props.text` | `placeholder` ("Escriba aqui") |
| `Objects/NumericField` | `ia.input.numeric-entry-field` | `props.value` | `minValue`, `maxValue` (null = sin rango; colores con `papo_core.items.getRangeColor`), `placeholder` |
| `Objects/Dropdown` | `ia.input.dropdown` | `props.value` | `options` ([{label, value}]), `placeholder` ("Seleccione") |
| `Objects/Label` | `ia.display.label` | `props.text` (valor del tag) | `tagPath` (ruta completa del tag, binding indirecto) |

`trueValue`/`falseValue` existen para que cada formulario guarde exactamente lo mismo que guarda hoy: los reportes PDF dependen de esos textos.

## Uso en un formulario

**Flex Repeater (recomendado)**: un repeater dentro del `FlexContainerGroupN`, con `path` = el objeto y una instancia por pregunta. El objeto escribe `item` de vuelta en cada instancia y `papo_core.register.recopile` lo lee desde `props.instances` (mismo mecanismo que usa hoy `Metalurgia/Fundamental Views/Checkbox` en 61 repeaters).

```json
{"instancePosition": {}, "instanceStyle": {"classes": ""}, "papoItemID": 5134, "registerTypeID": 7}
```

**Vista embebida en la celda** (`ia.display.view`, usada en el piloto): para formularios en grilla (columnas Receta 1/2/3, IZQ/DER). Cada campo se reemplaza por el objeto en la misma posición; las etiquetas y encabezados de la grilla quedan igual.

**El `custom.item` se queda en el componente del formulario** (procedimiento v2, paso 4, y "Ruta de desarrollo": `FlexContainerGroupN > Componente (custom.item)`). `recopile` solo lee `custom.item` del árbol del formulario, así que el `ia.display.view` lleva el `custom.item` estático del campo original, y el objeto toma de ahí `papoItemID` y `registerTypeID` y devuelve la respuesta. No se cambia `papo_core.register`.

```json
{"type": "ia.display.view", "meta": {"name": "NumericEntryField"}, "position": {"basis": "32px"},
 "custom": {"item": {"papoItemID": 11406, "registerTypeID": 1}},
 "props": {"path": "Objects/NumericField", "style": {"width": "100%"},
           "params": {"showQuestion": false, "fieldBasis": "100%", "minValue": 40, "maxValue": 50}},
 "propConfig": {
   "custom.item.answer": {"binding": {"type": "property", "config": {"path": "this.props.params.item.answer"}}},
   "props.params.papoItemID": {"binding": {"type": "property", "config": {"path": "this.custom.item.papoItemID"}}},
   "props.params.registerTypeID": {"binding": {"type": "property", "config": {"path": "this.custom.item.registerTypeID"}}},
   "props.params.fontSize": {"binding": {"type": "property", "config": {"path": "view.custom.fontSize"}}}}}
```

- `custom.item`: el mismo `{papoItemID, registerTypeID}` del campo original; `answer` enlazado a `this.props.params.item.answer`
- `position`: la del campo original
- `style`: `width: 100%` si la celda es una columna; `minHeight: 32px` si es una fila
- Checkbox: `question` = texto que tenía el checkbox; `trueValue`/`falseValue` = salidas del map original
- NumericField: `minValue`/`maxValue` = `custom.rang_down`/`rang_up` o el rango escrito en el transform de color
- Label (tag): `props.params.tagPath` con expresión `{view.custom.path} + "/<Tag>"` (equivale al binding indirecto `{1}/<Tag>`)
- A verificar: una vista embebida dentro de una sección cerrada (`display: false`) probablemente no arranca; si el operario guarda sin abrir la sección, el ítem se guarda igual (está en el `custom.item` del formulario) pero con `answer` nulo (antes, en un checkbox sin marcar, "No Cumple")

## Aplicación

1. Formulario por formulario, en su propio commit `refactor: objetos estándar en Form_X`, para poder deshacer uno solo con `git revert <sha>`.
2. Reemplazar solo los campos; no tocar Sections, FlexContainerGroups ni contenedores (el acordeón y `register.save` dependen de esos nombres).
3. Conservar los mismos `papoItemID` y la misma respuesta guardada (`trueValue`/`falseValue`, formato numérico).
4. Backup, lint (`/bug` paso 5), fila en `DEPLOY_INVENTORY.md`, y verificar en el Designer: aspecto, guardado en `registerhistory` y reporte PDF si aplica.

## Pendiente de verificar

- El gateway carga los objetos y el piloto (log `Setting LastModification to "external"`, 2026-10-24). Falta la revisión visual del piloto en el Designer y un guardado real comparado con `Form_EA11-0901_1h` en `registerhistory`.
- Confirmar en una sesión que el valor se conserva al cerrar y reabrir la sección (parámetro `value` inout).
- `resource.json` está en `.gitignore`: en un clone limpio estos objetos (como el resto de vistas) no traen `resource.json`.
