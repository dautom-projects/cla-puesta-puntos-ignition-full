# Cambios desde la corrida anterior

- Nodos nuevos: 0 · eliminados: 3
- Relaciones nuevas: 263 · eliminadas: 293
- Recursos con cambios internos: 86

## Nodos eliminados (3)

- Mensajes: **resetTable** (cla-project)
- Mensajes: **saveStartRegister-2201-end** (cla-project)
- Mensajes: **saveStartShift** (cla-project)

## Cambios internos (86)

_Renombres de customs, params, handlers, componentes, funciones de script..._

### Page/Embedded/Ensamble/Form_EA11-0901_end (cla-project, vista)
- component_customs quitados: ['refreshSecond']
- n_scripts: 13 → 12

### Page/Embedded/Ensamble/Form_EA11-1601_SKU (cla-project, vista)
- component_customs quitados: ['refreshSecond']
- n_scripts: 15 → 14

### Page/Embedded/Ensamble/Form_EA11-2501_2h (cla-project, vista)
- component_customs quitados: ['answers', 'refreshSecond']
- transforms: 64 → 62
- n_scripts: 73 → 69

### Page/Embedded/Ensamble/Form_EA11-2601_2h (cla-project, vista)
- component_customs quitados: ['answers', 'refreshSecond']
- transforms: 23 → 21
- n_scripts: 32 → 28

### Page/Embedded/Ensamble/Form_EA11-4101_1h (cla-project, vista)
- component_customs quitados: ['refreshSecond']
- n_scripts: 15 → 14

### Page/Embedded/Ensamble/Form_EA11-4101_SKU (cla-project, vista)
- component_customs quitados: ['refreshSecond']
- n_scripts: 15 → 14

### Page/Embedded/Ensamble/Form_EA11-4101_end (cla-project, vista)
- component_customs quitados: ['refreshSecond']
- n_scripts: 15 → 14

### Page/Embedded/Ensamble/Form_EA11-4200_1h (cla-project, vista)
- component_customs quitados: ['refreshSecond']
- n_scripts: 15 → 14

### Page/Embedded/Ensamble/Form_EA11-4200_2h (cla-project, vista)
- component_customs quitados: ['refreshSecond']
- n_scripts: 18 → 16

### Page/Embedded/Ensamble/Form_EA11-4200_mitad (cla-project, vista)
- component_customs quitados: ['refreshSecond']
- n_scripts: 15 → 14

### Page/Embedded/Ensamble/Form_EA11-4200_start (cla-project, vista)
- component_customs quitados: ['refreshSecond']
- n_scripts: 20 → 15

### Page/Embedded/Metalurgia/Form_FU10-0202_dia (cla-project, vista)
- component_customs quitados: ['answers']
- style_classes quitados: ['PAPO/Field/Dropdown']
- transforms: 130 → 46
- n_scripts: 135 → 51

### Page/Embedded/Metalurgia/Form_FU10-0202_hallazgo (cla-project, vista)
- component_customs quitados: ['refreshSecond']
- n_scripts: 17 → 16

### Page/Embedded/Metalurgia/Form_PA11-0301_start (cla-project, vista)
- component_customs quitados: ['refreshSecond']
- n_scripts: 16 → 15

### Page/Embedded/Metalurgia/Form_PA11-0401_start (cla-project, vista)
- component_customs quitados: ['refreshSecond']
- n_scripts: 35 → 34

### Page/Embedded/Metalurgia/Form_RE10-0102_start (cla-project, vista)
- component_customs quitados: ['answers', 'refreshSecond']
- transforms: 53 → 52
- n_scripts: 60 → 57

### Page/Embedded/Metalurgia/Form_RE11-0101_end (cla-project, vista)
- component_customs quitados: ['refreshSecond']
- n_scripts: 95 → 94

### Page/Embedded/Metalurgia/Form_SO02-1006_hallazgo (cla-project, vista)
- component_customs quitados: ['refreshSecond']
- n_scripts: 17 → 16

### Page/Embedded/Metalurgia/Form_SO02-1006_start (cla-project, vista)
- component_customs quitados: ['refreshSecond']
- n_scripts: 37 → 36

### Page/Embedded/Metalurgia/Form_SO02-4502_hallazgo (cla-project, vista)
- component_customs quitados: ['refreshSecond']
- n_scripts: 17 → 16

### Page/Embedded/Metalurgia/Form_SO02-4502_start (cla-project, vista)
- component_customs quitados: ['refreshSecond']
- n_scripts: 48 → 47

### Page/Embedded/Metalurgia/Form_TR11-0101_start (cla-project, vista)
- component_customs quitados: ['refresh']
- n_scripts: 58 → 57

### Page/Embedded/OREC/Form_CI11-0101_end (cla-project, vista)
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']

### Page/Embedded/OREC/Form_CI11-0101_start (cla-project, vista)
- component_customs quitados: ['answers', 'item.papoItemID']
- message_handlers quitados: ['saveStartShift']
- sends quitados: ['refreshPeriodic', 'refreshPreviewTable', 'refreshTable']
- components nuevos: ['Checkbox', 'Checkbox_0', 'Checkbox_1', 'Checkbox_2', 'Checkbox_3', 'Checkbox_4', 'Checkbox_5', 'Checkbox_6', 'Checkbox_7', 'Checkbox_8', 'Checkbox_9']
- components quitados: ['FlexRepeater']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- transforms: 121 → 65
- n_scripts: 127 → 70

### Page/Embedded/OREC/Form_CU11-0101_end (cla-project, vista)
- message_handlers quitados: ['saveStartRegister-2201-end']
- sends quitados: ['refreshPeriodic', 'refreshPreviewTable', 'refreshTable', 'resetTable']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- n_scripts: 13 → 12

### Page/Embedded/OREC/Form_CU11-0101_start (cla-project, vista)
- component_customs quitados: ['answers', 'borderColor', 'checkboxAnswers', 'checkboxAnswers[0]', 'checkboxAnswers[1]', 'checkboxAnswers[2]', 'color', 'item.papoItemID']
- message_handlers quitados: ['saveStartShift']
- sends quitados: ['refreshPeriodic', 'refreshTable']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- transforms: 99 → 33
- n_scripts: 96 → 38

### Page/Embedded/OREC/Form_EC07-0101_1h (cla-project, vista)
- component_customs quitados: ['item.papoItemID']
- message_handlers quitados: ['saveStartShift']
- sends quitados: ['refreshPeriodic', 'refreshPreviewTable', 'refreshTable']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- transforms: 6 → 4
- n_scripts: 11 → 9

### Page/Embedded/OREC/Form_EC07-0101_barcada (cla-project, vista)
- component_customs quitados: ['item.papoItemID']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Field/TagValue', 'PAPO/Form']
- style_classes quitados: ['dropdown', 'text-data-2']
- transforms: 56 → 46
- n_scripts: 56 → 51

### Page/Embedded/OREC/Form_EC07-0101_end (cla-project, vista)
- component_customs quitados: ['item.papoItemID']
- message_handlers quitados: ['saveStartShift']
- sends quitados: ['refreshPeriodic', 'refreshPreviewTable', 'refreshTable']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- n_scripts: 11 → 10

### Page/Embedded/OREC/Form_EC07-0101_start (cla-project, vista)
- component_customs quitados: ['answers', 'item.papoItemID']
- message_handlers quitados: ['saveStartShift']
- sends quitados: ['refreshPeriodic', 'refreshPreviewTable', 'refreshTable']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- transforms: 9 → 7
- n_scripts: 17 → 14

## Relaciones

- nuevas: embebe/abre 111, usa estilo 152
- eliminadas: llama 1, embebe/abre 19, maneja 45, envia 153, usa estilo 75