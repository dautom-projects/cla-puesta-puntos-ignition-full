# Objetos estándar de PAPO (v2)

Vistas `Objects/*` que encapsulan el diseño y el comportamiento de un campo: el mapeo Cumple/No Cumple, el color por rango, la respuesta del dropdown y el texto de la pregunta. El formulario solo pasa parámetros. Diseño de las clases y el tema: `ESTANDAR_DISENO.md`.

Piloto: `Page/Embedded/Ensamble/Form_EA11-0901_1h_PruebaPiloto` (2026-10-24): 42 campos como objetos (13 checkbox, 27 numéricos, 2 text field) y 26 valores de tag nativos.

## Cómo se recolecta la respuesta (no cambia el v2)

El `custom.item` sigue en el componente del formulario dentro de `FlexContainerGroupN` (procedimiento v2, paso 4). Ese componente ahora es un `ia.display.view`:

- `custom.item`: el mismo `{papoItemID, registerTypeID}` estático del campo original, y sus bindings si los tenía
- `custom.item.answer` ← `this.props.params.answer`: la respuesta que el objeto manda a la vista principal según lo que hizo el operario
- `papo_core.register.recopile` y `save` no cambian: leen `custom.item` igual que antes, en el mismo orden

## Contrato

| Parámetro | Dirección | Uso |
|---|---|---|
| `value` | inout | Valor del campo. Queda guardado en el formulario: si la sección se cierra y se reabre, el objeto vuelve con lo que había |
| `answer` | output | Respuesta que el formulario guarda en `custom.item.answer` |
| `question` | input | Texto de la pregunta (el del formulario). Vacío + `papoItemID` = descripción de `papoitem` |
| `fontSize` | input | Tamaño de letra; el formulario lo enlaza a `view.custom.fontSize` |
| `showQuestion`, `questionBasis` | input | Pregunta dentro del objeto (lista) u oculta (grilla, la pregunta es una etiqueta del formulario) |

| Objeto | Campo | `answer` | Parámetros propios |
|---|---|---|---|
| `Objects/Checkbox` | checkbox (la pregunta es su texto) | `trueValue` si está marcado, `falseValue` si no | `trueValue` ("Cumple"), `falseValue` ("No Cumple") |
| `Objects/NumericField` | numérico | el valor | `minValue`, `maxValue` (color por rango con `papo_core.items.getRangeColor`), `placeholder` |
| `Objects/TextField` | text field | el texto | `placeholder` |
| `Objects/Dropdown` | dropdown | la etiqueta de la opción elegida (`answerFrom: "label"`) o su valor (`"value"`) | `options` (fijas o con el mismo binding que tenía el campo), `placeholder` |
| `Objects/Label` | valor de tag (solo lectura) | el valor del tag | `tagPath` |

Diseño interno: cada `Field` usa su clase `PAPO/Field/*`; dentro de un formulario con `PAPO/Form` recibe además el tema corregido.

## Condiciones (estudio del 2026-10-24)

1. **Un objeto en una sección cerrada no corre.** El montaje de vistas lo decide el cliente ("The state of what views are mounted is driven by the frontend, not the backend", Carl Gould, Inductive Automation); una sección con `display: false` no monta sus objetos. Por eso:
   - `value` es inout: lo escrito no se pierde al cerrar la sección
   - el formulario guarda una respuesta inicial en `props.params.answer` igual a la que guardaba el campo sin tocar (checkbox: `falseValue`; texto: `""`; dropdown por etiqueta: `""`)
2. **Los valores de tag quedan nativos** (componente del formulario con la clase `PAPO/Field/TagValue`): el original guarda el valor del tag aunque la sección no se abra, y un objeto sin montar no puede leerlo
3. **Solo se convierten campos cuya respuesta es el valor del campo** (checkbox con map true/false; dropdown con la búsqueda de etiqueta estándar). Los que tienen lógica propia quedan nativos

## Herramienta

`.claude/skills/papo-design/scripts/papo_objects.py` convierte formularios (simula por defecto, `--apply` escribe con backup). Verifica que las fuentes de respuesta (ítems, sus bindings salvo `answer`, orden) no cambien y que solo se reescriban vistas con Gson canónico.

Simulación sobre los 239 formularios: 238 convertibles, 4,555 campos (2,209 checkbox, 1,604 text field, 594 numéricos con 231 rangos, 148 dropdowns: 125 por etiqueta y 23 por valor). 186 campos quedan nativos por tener lógica propia. Rechazado: `FU10-0202_start` (JSON no canónico).

## Pendiente de verificar en el piloto

- Abrir la sección, llenar, cerrar y reabrir: los valores siguen
- Guardar un registro y compararlo en `registerhistory` con uno de `Form_EA11-0901_1h`
- Numérico fuera de rango en rojo; tiempo de carga de la sección (42 vistas embebidas; en el foro reportan que cada vista con íconos descarga la librería de íconos)
