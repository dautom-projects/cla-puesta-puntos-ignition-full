# Cambios desde la corrida anterior

- Nodos nuevos: 2 · eliminados: 0
- Relaciones nuevas: 9 · eliminadas: 3
- Recursos con cambios internos: 6

## Nodos nuevos (2)

- Clases de estilo: **PAPO/Field/Dropdown** (cla-project)
- Clases de estilo: **PAPO/Form** (cla-project)

## Cambios internos (6)

_Renombres de customs, params, handlers, componentes, funciones de script..._

### Objects/Checkbox (cla-project, vista)
- params nuevos: ['answer', 'question', 'value']
- params quitados: ['item', 'registerTypeID']
- component_customs quitados: ['item.answer', 'item.papoItemID', 'item.registerTypeID']
- style_classes nuevos: ['PAPO/Field/Checkbox']

### Objects/Dropdown (cla-project, vista)
- params nuevos: ['answer', 'answerFrom', 'question', 'value']
- params quitados: ['fieldBasis', 'item', 'registerTypeID']
- component_customs quitados: ['item.answer', 'item.papoItemID', 'item.registerTypeID']
- style_classes nuevos: ['PAPO/Field/Dropdown']
- style_classes quitados: ['dropdown']
- transforms: 1 → 2
- n_scripts: 1 → 2

### Objects/Label (cla-project, vista)
- params nuevos: ['answer', 'question']
- params quitados: ['fieldBasis', 'item', 'registerTypeID']
- component_customs quitados: ['item.answer', 'item.papoItemID', 'item.registerTypeID']
- style_classes nuevos: ['PAPO/Field/TagValue']
- style_classes quitados: ['text-data-2']

### Objects/NumericField (cla-project, vista)
- params nuevos: ['answer', 'question', 'value']
- params quitados: ['fieldBasis', 'item', 'registerTypeID']
- component_customs quitados: ['item.answer', 'item.papoItemID', 'item.registerTypeID']
- style_classes nuevos: ['PAPO/Field/Input']

### Objects/TextField (cla-project, vista)
- params nuevos: ['answer', 'question', 'value']
- params quitados: ['fieldBasis', 'item', 'registerTypeID']
- component_customs quitados: ['item.answer', 'item.papoItemID', 'item.registerTypeID']
- style_classes nuevos: ['PAPO/Field/Input']

### Page/Embedded/Ensamble/Form_EA11-0901_1h_PruebaPiloto (cla-project, vista)
- component_customs quitados: ['borderColor', 'color']
- style_classes nuevos: ['PAPO/Form']
- style_classes quitados: ['PAPO/Field/Checkbox']
- transforms: 64 → 15
- n_scripts: 57 → 21

## Relaciones

- nuevas: embebe/abre 3, usa estilo 6
- eliminadas: usa estilo 3