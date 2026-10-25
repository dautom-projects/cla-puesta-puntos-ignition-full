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
| `emptyAnswer` | input | Respuesta cuando el valor está vacío (p. ej. `"-"`); vacía (`null`) = el valor tal cual. Misma regla que el transform `return value if value else "-"` de los formularios |

| Objeto | Campo | `answer` | Parámetros propios |
|---|---|---|---|
| `Objects/Checkbox` | checkbox (la pregunta es su texto) | `trueValue` si está marcado, `falseValue` si no | `trueValue` ("Cumple"), `falseValue` ("No Cumple") |
| `Objects/NumericField` | numérico | el valor | `minValue`, `maxValue` (color por rango con `papo_core.items.getRangeColor`), `placeholder` |
| `Objects/TextField` | text field | el texto | `placeholder` |
| `Objects/Dropdown` | dropdown | la etiqueta de la opción elegida (`answerFrom: "label"`) o su valor (`"value"`) | `options` (fijas o con el mismo binding que tenía el campo), `placeholder` |
| `Objects/OptionGroup` | radio group (una opción entre varias) | el texto elegido, o `emptyAnswer` ("-") | `options` (lista de textos) |
| `Objects/DateTime` | selector de fecha u hora | el valor con `format` (por defecto `h:mm:ss a`, como los formularios) | `pickerType` ("time"), `format` |
| `Objects/Label` | valor de tag (solo lectura) | el valor del tag | `tagPath` |

Diseño interno: cada `Field` usa su clase `PAPO/Field/*`; dentro de un formulario con `PAPO/Form` recibe además el tema corregido.

## Condiciones (estudio del 2026-10-24)

1. **Un objeto en una sección cerrada no corre.** El montaje de vistas lo decide el cliente ("The state of what views are mounted is driven by the frontend, not the backend", Carl Gould, Inductive Automation); una sección con `display: false` no monta sus objetos. Por eso:
   - `value` es inout: lo escrito no se pierde al cerrar la sección
   - el formulario guarda una respuesta inicial en `props.params.answer` igual a la que guardaba el campo sin tocar (checkbox: `falseValue`; texto: `""`; dropdown por etiqueta: `""`)
2. **Los valores de tag quedan nativos** (componente del formulario con la clase `PAPO/Field/TagValue`): el original guarda el valor del tag aunque la sección no se abra, y un objeto sin montar no puede leerlo
3. **Solo se convierten campos cuya respuesta es el valor del campo** (checkbox con map true/false; dropdown con la búsqueda de etiqueta estándar). Los que tienen lógica propia quedan nativos

## Generación

Los objetos se generan con `.claude/skills/papo-design/scripts/build_objects.py` (una sola definición; `--check` muestra qué cambiaría). Para cambiar un objeto se edita el generador y se vuelve a correr; no se editan los `view.json` a mano.

## Herramienta

`.claude/skills/papo-design/scripts/papo_objects.py` (v2.0) convierte formularios (simula por defecto, `--apply` escribe con backup):

- **Fila de lista**: fila = un campo + una etiqueta de pregunta (o el campo es la fila) → un objeto con la pregunta adentro (`showQuestion`), alto estándar 50 px (o el de la fila si era mayor). La pregunta sale del texto fijo o, si la etiqueta consultaba `papoitem`, del mismo `papoItemID`
- **Celda de grilla**: solo el campo; la celda conserva su layout
- **Repeater** (`Fundamental Views/Checkbox`): un objeto por instancia, con `registerTypeID` leído de `papoitem` (SELECT) y la respuesta guardada en la instancia como respuesta inicial
- `--legacy`: quita handlers de guardado legacy que nadie envía y el `custom.answers` reactivo de los grupos y del supervisor (v2, paso 4) si nada lo usa
- `--form-class`: agrega `PAPO/Form` a la raíz
- Conserva el valor inicial de cada campo (los guardados en el Designer) y su respuesta
- No reemplaza un componente que otro componente referencia (`view_refs.py` resuelve `this.`, `parent.`, `../`, `/root/…`, `getChild`), ni uno con otros `custom.item` adentro
- Verifica la recolección (ítems, bindings, orden, contenedor) y que no aparezcan referencias rotas

Simulación completa (papo-design + papo_objects, 2026-10-25), validada con papo-qa contra el original: **234 de 237 formularios pasan** las etapas 1–6; fallan solo los 3 de Cubiertas (sin wrappers del v2, caso manual). Grafo del proyecto convertido: 0 referencias no resueltas nuevas y 17 mensajes desbalanceados menos. Quedan nativos 89 campos (70 referenciados por otro componente, 19 con lógica propia).

Simulación sobre los 239 formularios: 238 convertibles, 4,555 campos (2,209 checkbox, 1,604 text field, 594 numéricos con 231 rangos, 148 dropdowns: 125 por etiqueta y 23 por valor). 186 campos quedan nativos por tener lógica propia. Rechazado: `FU10-0202_start` (JSON no canónico).

## Pendiente de verificar en el piloto

- Abrir la sección, llenar, cerrar y reabrir: los valores siguen
- Guardar un registro y compararlo en `registerhistory` con uno de `Form_EA11-0901_1h`
- Numérico fuera de rango en rojo; tiempo de carga de la sección (42 vistas embebidas; en el foro reportan que cada vista con íconos descarga la librería de íconos)
