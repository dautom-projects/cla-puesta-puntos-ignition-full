# Estándar de diseño de formularios PAPO

Fecha: 2026-10-24. Cómo estandarizar el diseño de las 239 vistas `Form_*` y escalarlo sin tocar la recolección de respuestas.

## Límite

La recolección de respuestas no cambia. Sigue igual el flujo del "Procedimiento de estandarización v2" y de "Ruta de desarrollo": cada campo tiene su `custom.item` en el componente del formulario dentro de `FlexContainerGroupN`, y `papo_core.register.recopile`/`save` lo recolectan con los wrappers estándar. El estándar de diseño solo toca `props.style` y `props.textStyle`.

## Diagnóstico (239 vistas Form_*)

| Rol | Componentes | Variantes de estilo | Con diseño escrito en el campo |
|---|:-:|:-:|:-:|
| Checkbox con `custom.item` | 2,248 | 9 | 58 |
| Text field con `custom.item` | 1,732 | 19 | 1,729 |
| Numérico con `custom.item` | 647 | 16 | 636 |
| Label de tag con `custom.item` | 611 | 12 | 585 |
| Dropdown con `custom.item` | 160 | 8 | 156 |
| Etiquetas dentro de los grupos (preguntas, subtítulos, encabezados) | 4,668 | 59 | 2,033 |
| Títulos y etiquetas fuera de los grupos | 1,287 | 10 | 911 |
| Sections | 390 | 1 | clase por binding (paso 2 del v2) |
| Botones Guardar / Cancelar | 478 | 2 | ya estándar (`button-1`, `button-2`) |

- El mismo campo se dibuja de formas distintas: los inputs usan la clase `dropdown` (bordes de 15 px, ~540 campos) o bordes de 10 px escritos a mano (~1,690); las labels de tag repiten `text-data-2` + `color: #1199C7` + `paddingLeft: 20` en cada campo
- El tamaño de letra ya está parametrizado por vista: `view.custom.fontSize` = 17 en 238 vistas, con 4,669 bindings
- 82 vistas tienen fin de línea CRLF; la serialización Gson canónica reproduce 238 de 239 vistas byte a byte (`FU10-0202_start` no)
- 77 familias de formularios con 1 a 8 variantes (start 78, end 70, 30min 15, SKU 15, 1h 13, mmto 11, 2h 9)
- 19 formularios arman sus checkboxes con un Flex Repeater de una sola vista: `Metalurgia/Fundamental Views/Checkbox` (61 repeaters)

## El estándar: tres capas

1. **Tokens del tema** (gateway, `data/modules/com.inductiveautomation.perspective/themes/cla-light.css` y `cla-dark.css`): colores `--cla-*` (`--cla-text-question`, `--cla-page-bg`, `--cla-button-question`…). Se despliegan aparte del proyecto.
2. **Clases por rol** (proyecto, `style-classes/PAPO/`): definen el diseño una sola vez.
3. **Vista**: solo layout (`position`, ancho, márgenes entre campos) y bindings (respuesta, colores por rango, `fontSize`). Nada de colores, bordes ni tipografía escritos en el campo.

| Clase | Componentes | Diseño |
|---|---|---|
| `PAPO/Field/Input` | numérico, text field y date-time con `custom.item`; TextField de Observaciones | bordes 10 px, fondo `--cla-page-bg`, 17 px, margen 0 |
| `PAPO/Field/Dropdown` | dropdown con `custom.item` | igual que Input (separada para ajustarla sola) |
| `PAPO/Field/Checkbox` | checkbox con `custom.item` | vacía: punto único para darles diseño |
| `PAPO/Field/TagValue` | label con `custom.item` (valor de tag) | Arial 16 px negrita centrado, `#1199C7`, sangría 20 px |

Títulos con la clase `text-titles`: el color `#002C36` escrito en el campo pasa al token `--cla-text-question` (mismo color, ahora sale del tema).

Qué se queda en la vista: `position`, márgenes y paddings entre campos, y todos los bindings. Sin anchos fijos: en una fila el ancho lo da el `basis` del campo; en una columna que estira, el campo ocupa la celda; en una columna alineada al inicio o al centro, el campo lleva `width: 100%` para ocupar la celda (79 campos en todo el proyecto). El `width: 250px` que daba la clase `dropdown` no se conserva. El valor estático de una propiedad que su propio binding sobrescribe se quita (no tiene efecto).

## Herramienta: papo-design

`.claude/skills/papo-design/` aplica el estándar vista por vista. Simulación por defecto.

Garantías en cada vista (si alguna falla, la vista no se escribe):

- La lista de fuentes de respuesta (`custom.item`, sus bindings y las instancias de repeater, en el orden en que las recorre `recopile`) es idéntica antes y después
- Nada cambia fuera de `props.style` / `props.textStyle`: ni `custom`, ni `propConfig`, ni nombres, ni el árbol
- Solo reescribe vistas cuya serialización Gson es canónica, y conserva CRLF
- Backup antes de escribir y relectura después

Simulación sobre las 239 vistas (2026-10-24): 238 aplicables, 5,902 componentes (2,248 checkbox, 1,730 text field, 647 numéricos, 611 labels de tag, 244 títulos, 238 Observaciones, 158 dropdowns, 26 date-time), todas con la recolección idéntica. Rechazada: `FU10-0202_start` (JSON no canónico). Además, 79 campos en columnas que no estiran reciben `width: 100%`. Quedan en el campo, para revisar a mano: 37 numéricos con un color fijo sin binding y 11 casos aislados (bordes o colores de un checkbox, `textAlign` de 3 labels).

Medición: papo-lint (v1.1.0) reporta `Form_*: campos sin clase de diseño PAPO/Field/*`. Línea base: 188 vistas (el piloto ya en 0).

## Despliegue por fases

1. **Piloto** `Form_EA11-0901_1h_PruebaPiloto`: revisión visual en el Designer contra `Form_EA11-0901_1h`
2. **Familia EA11-0901** (start, 30min, 1h, 2h, 4h, end) y `Metalurgia/Fundamental Views/Checkbox` (cubre los 61 repeaters)
3. **Por área** (Ensamble, Metalurgia, OREC, F&A, General): un commit por área, `git revert` para deshacer una
4. `FU10-0202_start` a mano (o tras guardarla en el Designer, que la deja canónica)

En cada fase: desplegar primero `style-classes/PAPO/` y después las vistas; fila en `DEPLOY_INVENTORY.md`; papo-lint antes y después.

## Objetos estándar v2 (piloto 2026-10-24)

Además de las clases, los campos interactivos del piloto son objetos `Objects/*` que encapsulan diseño y comportamiento. El `custom.item` sigue en el formulario y lee la respuesta que manda el objeto, así que el flujo del v2 no cambia. Contrato, condiciones y simulación: `OBJETOS_ESTANDAR.md`.

## Siguiente nivel (no aplicado)

- **Etiquetas de pregunta, subtítulos y encabezados** (4,668 dentro de los grupos: 3,485 normales, 520 negrita, 499 negrita centrada): clases `PAPO/Text/Question`, `PAPO/Text/Subtitle`, `PAPO/Text/Header`. Antes hay que confirmar en el Designer que una clase en la label (que estila el contenedor) produce lo mismo que `textStyle` (que estila el texto); si es así, la herramienta las agrega con la misma verificación
- **Tokens propios del formulario** en el tema (`--papo-field-radius`, `--papo-tag-value`, `--papo-range-error`): las clases usarían tokens y un cambio de tema ajustaría todo; requiere desplegar el tema del gateway
- **Formularios nuevos desde plantilla**: generar el `view.json` de un PAPO nuevo desde `papoitem` con la estructura del v2 (Sections, `FlexContainerGroupN`, campos con `custom.item`) y las clases `PAPO/` desde el inicio. Con 77 familias y 3.1 variantes de media, generar las variantes de una familia desde una sola definición evita copiar y pegar vistas
- **papo-lint como compuerta**: correrlo antes de cada despliegue y no subir vistas con hallazgos nuevos
- El stylesheet avanzado del proyecto (Tailwind con prefijo `psc-`) sirve para utilidades de layout; el diseño por rol queda en las clases `PAPO/`

## Evaluación: mover el diseño base al tema (2026-10-24)

Producción y PAPOS corren 8.1.19: no hay stylesheet avanzado (llegó en 8.1.22), así que las opciones son clases de estilo del proyecto o el tema del gateway. El Designer de 8.1.19 dibuja con JxBrowser 7.12.1 (Chromium 86).

### Estado del tema actual (`cla-light.css`, `cla-dark.css`)

1. `:root{` (línea 4) nunca se cierra. Las ~75 reglas de componentes de las líneas 36 a 579 (botones `button-*`, `button-questions` de las Sections, popup, checkbox, dropdown, inputs) quedan anidadas dentro de `:root`, y la llave suelta de la línea 581 cierra el bloque. Un navegador sin CSS Nesting (el Chromium 86 del Designer, Chrome anterior a 112) descarta esas reglas; uno moderno las aplica (las que empiezan con `div[...]` solo desde Chrome 120). El Designer y los clientes pueden verse distinto
2. La regla de inputs no coincide con ningún componente: el text field dibuja el `<input>` como raíz (no hay un `div` con `data-component`) y el numérico es `ia.input.numeric-entry-field`, no `ia.input.numeric-entry` (verificado en el bundle de Perspective 8.1.19)
3. `boder-color` (12 veces) no es una propiedad CSS: los bordes de hover de los botones nunca aplicaron
4. `.ia_dropdown { width: 150px !important }` fuerza todos los dropdowns a 150 px en navegadores modernos, contra el estándar sin anchos fijos
5. La regla de inputs usa `!important` en `color` y `border`: si llegara a aplicar, taparía los colores por rango que los formularios ponen con bindings
6. `cla-dark.css` tiene los mismos colores que `cla-light.css`: no es un tema oscuro
7. Un cambio de tema solo se ve tras reiniciar el gateway o el módulo Perspective (y F5 en los clientes), y afecta a todos los proyectos del gateway que usan ese tema

### Qué puede hacer cada capa en 8.1.19

| | Clase de estilo del proyecto | Tema del gateway |
|---|---|---|
| Dónde vive | En el proyecto, en git; se despliega con las vistas | En el gateway, fuera de git; copia manual y reinicio |
| Qué alcanza | El elemento raíz del componente | Cualquier selector: partes internas (ícono del checkbox, input interno del numérico, opciones del dropdown, placeholder) y estados (`:hover`, `:focus`, `:disabled`) |
| Prioridad | Pierde contra `props.style` del campo | Pierde contra `props.style`, salvo con `!important` |
| Aplicar a un tipo sin tocar campos | No | Sí |

### Recomendación

- **No mover el diseño base al tema.** Bordes, fondo y letra de los campos siguen en las clases `PAPO/Field/*`: papo-design las pone sin costo, viajan con el proyecto y no piden reinicio. Así el diseño de un formulario vive en un solo lugar
- **Usar el tema solo para lo que una clase no alcanza**: partes internas, estados y los tokens de color
- **Antes, corregir el tema.** Propuesta lista, sin instalar: `theme/cla-light.fix.patch` y `theme/cla-dark.fix.patch` (cierran `:root`, quitan la llave suelta, corrigen `boder-color` y los selectores de input, quitan `!important` del input base y el `width: 150px` de los dropdowns). Efecto: el Designer y todos los navegadores pasan a ver lo mismo. En navegadores modernos cambian los dropdowns (sin 150 px fijos), el borde base de los inputs y los bordes de hover de los botones
- **Versionar el tema**: copiar `data/modules/com.inductiveautomation.perspective/themes/cla-*.css` al repo y registrar su despliegue en `DEPLOY_INVENTORY.md` como un recurso más

**Piloto en PAPOS (2026-10-24).** En lugar del parche global, el tema lleva al final un bloque `PILOTO PAPO` con las 57 reglas de formularios (botones, Sections, checkbox, dropdown, inputs) ya corregidas y con alcance `.psc-PAPO\/Form`. Solo las vistas con la clase `PAPO/Form` en la raíz lo reciben; hoy, únicamente el piloto. El resto del gateway queda igual. Para extenderlo a otro formulario basta con agregarle `PAPO/Form` en la raíz; para revertir, se borra el bloque.

Qué probar: comparar el Designer y Chrome en el piloto (Sections, botones, checkbox, dropdown, numéricos fuera de rango en rojo) y en una vista de otro módulo (`Node/MixingDashboard`, `Alerts`).
