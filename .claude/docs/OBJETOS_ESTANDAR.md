# Objetos estándar de PAPO

Vistas reutilizables para los campos de los formularios Form_*, en
`cla-project/com.inductiveautomation.perspective/views/Objects/`. Reemplazan las ~123 variantes de bindings con las que hoy se arman checkbox, text field, numeric, dropdown y label (inventario del 2026-10-22: 5,539 campos con `custom.item` en 238 vistas).

Ninguna vista usa todavía estos objetos. La adopción va formulario por formulario (ver "Aplicación").

## Contrato común

Cada objeto es una fila (`root` flex, `alignItems: center`). El componente que guarda la respuesta se llama siempre `Field` y tiene `custom.item = {papoItemID, answer, registerTypeID}`.

| Parámetro | Dirección | Default | Uso |
|---|---|---|---|
| `papoItemID` | input | null | Ítem de la pregunta |
| `registerTypeID` | input | null | Tipo de registro del formulario (el `view.custom.registerTypeID` de la vista que lo usa) |
| `fontSize` | input | 17 | Tamaño de letra de pregunta y campo |
| `item` | **output** | {} | `{papoItemID, answer, registerTypeID}`, enlazado a `/root/Field.custom.item` |

- Texto de la pregunta: `papo_core.items.getQuestionText(value)` con `{papoItemID, dbConnection}` (consulta individual a `papoitem`, igual que hoy; sin SQL en la vista).
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

**Vista embebida suelta** (`ia.display.view`): sirve para layouts mezclados, pero hoy `recopile` no lee `props.params.item` de una vista embebida. Usarla requiere primero ese cambio en `papo_core.register` (ver BACKLOG.md).

## Aplicación

1. Formulario por formulario, en su propio commit `refactor: objetos estándar en Form_X`, para poder deshacer uno solo con `git revert <sha>`.
2. Reemplazar solo los campos; no tocar Sections, FlexContainerGroups ni contenedores (el acordeón y `register.save` dependen de esos nombres).
3. Conservar los mismos `papoItemID` y la misma respuesta guardada (`trueValue`/`falseValue`, formato numérico).
4. Backup, lint (`/bug` paso 5), fila en `DEPLOY_INVENTORY.md`, y verificar en el Designer: aspecto, guardado en `registerhistory` y reporte PDF si aplica.

## Pendiente de verificar

- Los objetos se generaron en disco. Su `resource.json` no tiene `lastModificationSignature`; confirmar que el gateway los carga al reiniciar `PAPOS` (y que el Designer los muestra en `Objects/`).
- `resource.json` está en `.gitignore`: en un clone limpio estos objetos (como el resto de vistas) no traen `resource.json`.
