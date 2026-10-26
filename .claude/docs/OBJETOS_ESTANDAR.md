# Objetos estándar de PAPO (v2.4)

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
| `question` | input | Texto de la pregunta (el del formulario). Vacío + `papoItemID` = descripción de `papoitem`. Se resuelve una vez en `view.custom.question` |
| `enabled` | input | `false` = campo deshabilitado (solo lectura), como los campos con `enabled: false` del original |
| `fontSize` | input | Tamaño de letra; el formulario lo enlaza a `view.custom.fontSize` |
| `showQuestion`, `questionBasis` | input | Pregunta dentro del objeto (lista) u oculta (grilla, la pregunta es una etiqueta del formulario) |
| `emptyAnswer` | input | Respuesta cuando el valor está vacío (p. ej. `"-"`); vacía (`null`) = el valor tal cual. Misma regla que el transform `return value if value else "-"` de los formularios |

| Objeto | Campo | `answer` | Parámetros propios |
|---|---|---|---|
| `Objects/Checkbox` | checkbox (la pregunta es su texto) | `trueValue` si está marcado, `falseValue` si no | `trueValue` ("Cumple"), `falseValue` ("No Cumple"); `trueText` / `falseText`: texto según el estado en vez de la pregunta (p. ej. ✔ / ✘) |
| `Objects/NumericField` | numérico | el valor | `minValue`, `maxValue` (color por rango con `papo_core.items.getRangeColor`), `placeholder` ("Escriba aqui"), `questionAsPlaceholder` (la pregunta como placeholder) |
| `Objects/TextField` | text field | el texto | `placeholder`, `questionAsPlaceholder` |
| `Objects/Dropdown` | dropdown | la etiqueta de la opción elegida (`answerFrom: "label"`) o su valor (`"value"`) | `options` (fijas o con el mismo binding que tenía el campo), `placeholder` ("Seleccionar"), `showClearIcon` |
| `Objects/OptionGroup` | radio group (una opción entre varias) en una fila, alineado con la pregunta | el texto elegido, o `emptyAnswer` ("-") | `options` (lista de textos). Cada radio lleva `selected` calculado desde `value` (v2.4): el radio de Perspective renderiza `<input name="radio" checked={selected}>` y, sin `selected`, el input quedaba sin controlar y la primera opción podía quedar marcada en el navegador sin estarlo, de modo que el primer clic no hacía nada |
| `Objects/DateTime` | selector de fecha u hora | el valor con `format` (por defecto `h:mm:ss a`, como los formularios) | `pickerType` ("time"), `format` |
| `Objects/Label` | valor de tag (solo lectura) | el valor del tag | `tagPath` |

Diseño interno: cada `Field` usa su clase `PAPO/Field/*`; dentro de un formulario con `PAPO/Form` recibe además el tema corregido. La raíz de cada objeto es `position: relative`: el `<input>` oculto del checkbox y del radio de Perspective es `position: absolute` y, sin un contenedor posicionado, quedaba ubicado respecto a la raíz del Template; en secciones largas, al hacer clic el navegador desplazaba la página hasta él y se veía en blanco (v2.3).

## Condiciones (estudio del 2026-10-24)

1. **Un objeto en una sección cerrada no corre.** El montaje de vistas lo decide el cliente ("The state of what views are mounted is driven by the frontend, not the backend", Carl Gould, Inductive Automation); una sección con `display: false` no monta sus objetos. Por eso:
   - `value` es inout: lo escrito no se pierde al cerrar la sección
   - el formulario guarda una respuesta inicial en `props.params.answer` igual a la que guardaba el campo sin tocar (checkbox: `falseValue`; texto: `""`; dropdown por etiqueta: `""`)
2. **Los valores de tag quedan nativos** (componente del formulario con la clase `PAPO/Field/TagValue`): el original guarda el valor del tag aunque la sección no se abra, y un objeto sin montar no puede leerlo
3. **Solo se convierten campos cuya respuesta es el valor del campo** (checkbox con map true/false; dropdown con la búsqueda de etiqueta estándar). Los que tienen lógica propia quedan nativos

## Generación

Los objetos se generan con `.claude/skills/papo-design/scripts/build_objects.py` (una sola definición; `--check` muestra qué cambiaría). Para cambiar un objeto se edita el generador y se vuelve a correr; no se editan los `view.json` a mano.

## Herramienta

`.claude/skills/papo-design/scripts/papo_objects.py` (v2.2) convierte formularios (simula por defecto, `--apply` escribe con backup):

- **Fila de lista** (solo en grupos en columna): fila = un campo + una etiqueta de pregunta (o el campo es la fila) → un objeto con la pregunta adentro (`showQuestion`), alto estándar 50 px (o el de la fila si era mayor). La pregunta sale del texto fijo o, si la etiqueta consultaba `papoitem`, del mismo `papoItemID`. Una fila sin pregunta deja el campo a todo el ancho
- **Celda de grilla** (y grupos en fila, como `FlexContainerSupervisor`): solo el campo; la celda conserva su layout
- **Todas las propiedades del campo pasan al objeto**: valor, `enabled`, placeholder, opciones y el texto del checkbox, fijos o con binding. Los textos que consultaban la descripción en `papoitem` pasan como `papoItemID` (la consulta queda en el objeto); el mapa ✔ / ✘ del estado como `trueText` / `falseText`; otro binding se copia al parámetro si resuelve igual desde el objeto. Las variantes de "Escriba aqui" quedan en el placeholder estándar. Si una propiedad no tiene parámetro (p. ej. `inputBounds`) el campo queda nativo
- **Repeater** (`Fundamental Views/Checkbox`): un objeto por instancia, con `registerTypeID` leído de `papoitem` (SELECT) y la respuesta guardada en la instancia como respuesta inicial
- **`papoItemID` fijo en `custom.item`** (v2.4, `--static-ids`): una sola lógica para todos los formularios. Los IDs calculados en ejecución (`basePapo` + índice tomado del nombre, `parent.custom.papoItemID`, la etiqueta hermana, 19 variantes en 2,600 campos) se reemplazan por su valor, calculado con `item_ids.py`, que evalúa los bindings y los scripts de transformación sobre el JSON de la vista. Validado contra la base: coincide exactamente con el último registro de 118 formularios (los 18 que difieren tienen el registro guardado antes del último cambio de la vista) y con los 6 pilotos. Los bindings desactivados (`enabled: false`) se quitan. papo-qa compara la recolección por el ID real, así que un ID fijado con el mismo valor recoge el mismo ítem. Quedan 4 sin calcular (en ejecución dan `null`: supervisores de EA11-1601 y EA11-2601 y dos contenedores)
- **Pregunta siempre desde `papoItemID`** (v2.3): una pregunta fija (texto del checkbox, etiqueta de la fila o del grupo de opción) de un ítem con `papoItemID` conocido pasa a leer `papoitem.Description`; así, editar la base cambia el formulario. Si el texto de la base es distinto, `--questions-sql <archivo>` (en `papo_objects.py` y `simulate_all.py`) escribe el `UPDATE papoitem` con su rollback, que se aplica en cla-db-papo y luego en producción; papo-qa no deja pasar la vista hasta que la base tenga el texto. Los recortes que el formulario hacía sobre la descripción (p. ej. quitar "Tanque de Soda, ") se eliminan. Quedan fijas las etiquetas informativas, las de ítems con ID calculado en ejecución y los encabezados de grilla de valores de tag (EA11-0901: el texto de la base trae setpoint y lado)
- **Alto de la sección**: `papo_core.ui.toggleSection` abre cada grupo con el alto fijo de `custom.baseBasisPx`; si las filas estándar suman más que las originales, ese alto crece lo mismo (si no, el final de la sección queda cortado)
- **Grupo de opción**: la pregunta conserva el ancho de su etiqueta original (`questionBasis`), así las opciones empiezan donde estaban los checkbox
- `--legacy`: quita handlers de guardado legacy que nadie envía y el `custom.answers` reactivo de los grupos y del supervisor (v2, paso 4) si nada lo usa
- `--form-class`: agrega `PAPO/Form` a la raíz
- Conserva el valor inicial de cada campo (los guardados en el Designer) y su respuesta
- No reemplaza un componente que otro componente referencia (`view_refs.py` resuelve `this.`, `parent.`, `../`, `/root/…`, `getChild`), ni uno con otros `custom.item` adentro
- Verifica la recolección (ítems, bindings, orden, contenedor) y que no aparezcan referencias rotas

Simulación completa (papo-design + papo_objects v2.1, 2026-10-25), validada con papo-qa v1.2 contra el original (incluida la comparación de lo que ve el operario en cada campo): **234 de 237 formularios pasan** las etapas 1–6; fallan solo los 3 de Cubiertas (sin wrappers del v2, caso manual). 4,986 objetos (2,502 checkbox, 1,724 texto, 609 numéricos, 110 dropdowns, 26 fechas, 15 grupos de opción), 870 filas de lista. Quedan nativos 92 campos (70 referenciados por otro componente, 19 con lógica propia, 3 con propiedades sin parámetro). Grafo del proyecto convertido (v2.0): 0 referencias no resueltas nuevas y 17 mensajes desbalanceados menos.

Simulación de todo el proyecto: `python3 .claude/skills/papo-qa/scripts/simulate_all.py` (lee los originales de git, no escribe nada). Con v2.2: 234 de 237 pasan y 62 secciones crecen de alto.

Corrección v2.1 (revisión del usuario en los pilotos, 2026-10-25): la v2.0 perdía la pregunta de 772 checkbox que la consultaban en `papoitem` y la de los placeholders que mostraban la pregunta (516), no pasaba `enabled: false` (36 campos) ni los bindings de valor a tags (57), y trataba el supervisor como fila de lista (pregunta vacía al 60 %). El radio group no tenía `orientation`/`align`/`radioStyle` y las opciones saltaban de línea.

## Probar el guardado de un piloto

`Digitalizacion_Template` abre cada formulario por una ruta armada desde el PAPO, así que una copia `_PruebaPiloto` nunca se abre en runtime. Para probarla en el flujo real (guardar, firmar, PDF), se intercambia temporalmente en el gateway local:

```bash
python3 .claude/skills/papo-qa/scripts/pilot_swap.py on "Page/Embedded/F&A/Form_AC10-0201_start"
python3 .claude/skills/papo-qa/scripts/pilot_swap.py off --all
```

`on` guarda un backup y pone el contenido del piloto en el `view.json` del original; `off` lo restaura byte a byte (si el Designer guardó la vista mientras estaba intercambiada, deja esa versión aparte). No se renombra nada ni se toca el Template. No commitear con un intercambio activo: `pilot_swap.py status` lo muestra y papo-qa lo avisa.

Simulación sobre los 239 formularios: 238 convertibles, 4,555 campos (2,209 checkbox, 1,604 text field, 594 numéricos con 231 rangos, 148 dropdowns: 125 por etiqueta y 23 por valor). 186 campos quedan nativos por tener lógica propia. Rechazado: `FU10-0202_start` (JSON no canónico).

## Pendiente de verificar en el piloto

- Abrir la sección, llenar, cerrar y reabrir: los valores siguen
- Guardar un registro y compararlo en `registerhistory` con uno de `Form_EA11-0901_1h`
- Numérico fuera de rango en rojo; tiempo de carga de la sección (42 vistas embebidas; en el foro reportan que cada vista con íconos descarga la librería de íconos)
