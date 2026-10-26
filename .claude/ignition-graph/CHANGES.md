# Cambios desde la corrida anterior

- Nodos nuevos: 0 · eliminados: 14
- Relaciones nuevas: 191 · eliminadas: 152
- Recursos con cambios internos: 62

## Nodos eliminados (14)

- Mensajes: **saveFourHourRegister** (cla-project)
- Mensajes: **saveHourRegister_test** (cla-project)
- Mensajes: **saveStartRegister-2501-2h** (cla-project)
- Mensajes: **saveStartRegister-2501-end** (cla-project)
- Mensajes: **saveStartRegister-4101-1h** (cla-project)
- Mensajes: **saveStartRegister-4101-end** (cla-project)
- Mensajes: **saveStartRegister-4101-sku** (cla-project)
- Mensajes: **saveStartRegister-4101-start** (cla-project)
- Mensajes: **saveStartRegister-4200-1h** (cla-project)
- Mensajes: **saveStartRegister-4200-2h** (cla-project)
- Mensajes: **saveStartRegister-4200-end** (cla-project)
- Mensajes: **saveStartRegister-4200-mid** (cla-project)
- Mensajes: **saveStartRegister-4200-start** (cla-project)
- Mensajes: **saveTwoHourRegister** (cla-project)

## Cambios internos (62)

_Renombres de customs, params, handlers, componentes, funciones de script..._

### Objects/Checkbox (cla-project, vista)
- customs nuevos: ['question']
- params nuevos: ['enabled', 'falseText', 'trueText']
- component_customs nuevos: ['question']

### Objects/DateTime (cla-project, vista)
- customs nuevos: ['question']
- params nuevos: ['enabled', 'startNow']
- component_customs nuevos: ['question']
- n_scripts: 2 → 4

### Objects/Dropdown (cla-project, vista)
- customs nuevos: ['question']
- params nuevos: ['enabled', 'showClearIcon']
- component_customs nuevos: ['question']

### Objects/Label (cla-project, vista)
- customs nuevos: ['question']
- component_customs nuevos: ['question']

### Objects/NumericField (cla-project, vista)
- customs nuevos: ['question']
- params nuevos: ['enabled', 'questionAsPlaceholder']
- component_customs nuevos: ['question']

### Objects/OptionGroup (cla-project, vista)
- customs nuevos: ['question']
- params nuevos: ['enabled']
- component_customs nuevos: ['question']

### Objects/TextField (cla-project, vista)
- customs nuevos: ['question']
- params nuevos: ['enabled', 'questionAsPlaceholder']
- component_customs nuevos: ['question']

### Page/Embedded/Ensamble/Form_EA11-0901_1h (cla-project, vista)
- component_customs quitados: ['borderColor', 'color']
- message_handlers quitados: ['saveFourHourRegister']
- sends quitados: ['refreshPeriodic', 'refreshPreviewTable', 'refreshTable']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Field/TagValue', 'PAPO/Form']
- style_classes quitados: ['dropdown', 'text-data-2']
- transforms: 64 → 15
- n_scripts: 57 → 20

### Page/Embedded/Ensamble/Form_EA11-0901_2h (cla-project, vista)
- component_customs quitados: ['borderColor', 'color']
- message_handlers quitados: ['saveTwoHourRegister']
- sends quitados: ['refreshPeriodic', 'refreshPreviewTable', 'refreshTable']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Field/TagValue', 'PAPO/Form']
- style_classes quitados: ['dropdown', 'text-data-2']
- transforms: 33 → 7
- n_scripts: 21 → 16

### Page/Embedded/Ensamble/Form_EA11-0901_30min (cla-project, vista)
- message_handlers quitados: ['saveHourRegister_test']
- sends quitados: ['refreshPeriodic', 'refreshPreviewTable', 'refreshTable']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- transforms: 5 → 3
- n_scripts: 9 → 8

### Page/Embedded/Ensamble/Form_EA11-0901_4h (cla-project, vista)
- component_customs quitados: ['borderColor', 'color']
- message_handlers quitados: ['saveFourHourRegister']
- sends quitados: ['refreshPeriodic', 'refreshPreviewTable', 'refreshTable']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Field/TagValue', 'PAPO/Form']
- style_classes quitados: ['dropdown', 'text-data-2']
- transforms: 33 → 5
- n_scripts: 17 → 12

### Page/Embedded/Ensamble/Form_EA11-0901_end (cla-project, vista)
- component_customs quitados: ['answers']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Field/TagValue', 'PAPO/Form']
- style_classes quitados: ['dropdown', 'text-data-2']
- transforms: 6 → 5
- n_scripts: 14 → 13

### Page/Embedded/Ensamble/Form_EA11-0901_start (cla-project, vista)
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- transforms: 40 → 7
- n_scripts: 29 → 13

### Page/Embedded/Ensamble/Form_EA11-1101_1h (cla-project, vista)
- component_customs quitados: ['borderColor', 'color']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Field/TagValue', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- transforms: 27 → 7
- n_scripts: 18 → 14

### Page/Embedded/Ensamble/Form_EA11-1101_end (cla-project, vista)
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']

### Page/Embedded/Ensamble/Form_EA11-1101_start (cla-project, vista)
- component_customs quitados: ['answers', 'item.papoItemID']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- transforms: 25 → 7
- n_scripts: 17 → 15

### Page/Embedded/Ensamble/Form_EA11-1201_1h (cla-project, vista)
- component_customs quitados: ['borderColor', 'color']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- transforms: 82 → 30
- n_scripts: 78 → 36

### Page/Embedded/Ensamble/Form_EA11-1201_2h (cla-project, vista)
- component_customs quitados: ['borderColor', 'color']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- transforms: 89 → 33
- n_scripts: 83 → 39

### Page/Embedded/Ensamble/Form_EA11-1201_end (cla-project, vista)
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']

### Page/Embedded/Ensamble/Form_EA11-1201_start (cla-project, vista)
- component_customs quitados: ['answers', 'borderColor', 'color', 'item.papoItemID']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Field/TagValue', 'PAPO/Form']
- style_classes quitados: ['dropdown', 'text-data-2']
- transforms: 108 → 34
- n_scripts: 94 → 40

### Page/Embedded/Ensamble/Form_EA11-1501_1h (cla-project, vista)
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- transforms: 16 → 8
- n_scripts: 18 → 14

### Page/Embedded/Ensamble/Form_EA11-1501_2h (cla-project, vista)
- component_customs quitados: ['borderColor', 'color', 'item.papoItemID']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- transforms: 80 → 42
- n_scripts: 77 → 48

### Page/Embedded/Ensamble/Form_EA11-1501_30min (cla-project, vista)
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- transforms: 5 → 3

### Page/Embedded/Ensamble/Form_EA11-1501_end (cla-project, vista)
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']

### Page/Embedded/Ensamble/Form_EA11-1501_start (cla-project, vista)
- component_customs quitados: ['answers', 'item.papoItemID']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- transforms: 49 → 5
- n_scripts: 34 → 11

### Page/Embedded/Ensamble/Form_EA11-1601_1h (cla-project, vista)
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- transforms: 23 → 7
- n_scripts: 21 → 13

### Page/Embedded/Ensamble/Form_EA11-1601_2h (cla-project, vista)
- component_customs quitados: ['borderColor', 'color']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- transforms: 111 → 41
- n_scripts: 106 → 48

### Page/Embedded/Ensamble/Form_EA11-1601_4h (cla-project, vista)
- message_handlers quitados: ['saveFourHourRegister']
- sends quitados: ['refreshPeriodic', 'refreshPreviewTable', 'refreshTable']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- transforms: 7 → 5
- n_scripts: 14 → 12

### Page/Embedded/Ensamble/Form_EA11-1601_SKU (cla-project, vista)
- component_customs quitados: ['answers']
- message_handlers quitados: ['saveStartRegister-4101-sku']
- sends quitados: ['refreshPeriodic', 'refreshPreviewTable', 'refreshTable', 'resetTable']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- transforms: 10 → 7
- n_scripts: 18 → 15

### Page/Embedded/Ensamble/Form_EA11-1601_end (cla-project, vista)
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']

## Relaciones

- nuevas: embebe/abre 79, usa estilo 112
- eliminadas: llama 1, maneja 20, envia 75, usa estilo 56