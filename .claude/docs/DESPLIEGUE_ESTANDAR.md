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

F&A y General/POLY/Cubiertas no tienen SQL. Un área puede desplegarse sin las demás, pero siempre con su SQL antes que sus formularios.

### Paso 6: formularios

Un commit por familia (`refactor: estándar en <familia>`), así que una familia se despliega o se revierte sola. Orden sugerido, el mismo en que se probaron: Ensamble, F&A, Metalurgia, OREC, General/POLY/Cubiertas.

- Las copias `_PruebaPiloto` son de prueba y el Template no las abre: no hace falta llevarlas
- Las copias `F&A/Form_* D` y `F&A/Form__end` quedan como están (decisión del usuario)
- `Metalurgia/Fundamental Views/Checkbox` ya no la usa ningún formulario (BACKLOG)

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
