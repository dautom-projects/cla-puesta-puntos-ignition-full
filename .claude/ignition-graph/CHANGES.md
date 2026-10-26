# Cambios desde la corrida anterior

- Nodos nuevos: 0 · eliminados: 2
- Relaciones nuevas: 79 · eliminadas: 106
- Recursos con cambios internos: 21

## Nodos eliminados (2)

- Mensajes: **saveEndShift** (cla-project)
- Mensajes: **saveStartRegister-PTARI** (cla-project)

## Cambios internos (21)

_Renombres de customs, params, handlers, componentes, funciones de script..._

### Page/Embedded/Metalurgia/Form_FU11-0101_end (cla-project, vista)
- message_handlers quitados: ['saveStartRegister-2201-end']
- sends quitados: ['refreshPeriodic', 'refreshPreviewTable', 'refreshTable', 'resetTable']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- n_scripts: 13 → 12

### Page/Embedded/Metalurgia/Form_FU11-0101_start (cla-project, vista)
- component_customs quitados: ['answers', 'item.papoItemID', 'key.answer']
- message_handlers quitados: ['saveStartRegister']
- sends quitados: ['refreshPeriodic', 'refreshPreviewTable', 'refreshTable', 'resetTable']
- style_classes nuevos: ['PAPO/Field/Checkbox', 'PAPO/Field/Input', 'PAPO/Field/TagValue', 'PAPO/Form']
- style_classes quitados: ['dropdown', 'text-data-2']
- transforms: 451 → 229
- n_scripts: 403 → 235

### Page/Embedded/Metalurgia/Form_PA11-0301_end (cla-project, vista)
- message_handlers quitados: ['saveStartRegister-2201-end']
- sends quitados: ['refreshPeriodic', 'refreshPreviewTable', 'refreshTable', 'resetTable']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- n_scripts: 13 → 12

### Page/Embedded/Metalurgia/Form_PA11-0301_start (cla-project, vista)
- component_customs quitados: ['answers', 'item.papoItemID']
- message_handlers quitados: ['saveStartRegister-PTARI']
- sends quitados: ['refreshPeriodic', 'refreshPreviewTable', 'refreshTable', 'resetTable']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Field/TagValue', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- transforms: 36 → 11
- n_scripts: 20 → 16

### Page/Embedded/Metalurgia/Form_PA11-0401_end (cla-project, vista)
- message_handlers quitados: ['saveStartRegister-2201-end']
- sends quitados: ['refreshPeriodic', 'refreshPreviewTable', 'refreshTable', 'resetTable']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- n_scripts: 13 → 12

### Page/Embedded/Metalurgia/Form_PA11-0401_start (cla-project, vista)
- component_customs quitados: ['answers', 'item.papoItemID']
- message_handlers quitados: ['saveEndShift']
- sends quitados: ['refreshPeriodic', 'refreshPreviewTable', 'refreshTable']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- transforms: 60 → 27
- n_scripts: 63 → 35

### Page/Embedded/Metalurgia/Form_RE10-0102_end (cla-project, vista)
- message_handlers quitados: ['saveStartRegister-2201-end']
- sends quitados: ['refreshPeriodic', 'refreshPreviewTable', 'refreshTable', 'resetTable']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- n_scripts: 13 → 12

### Page/Embedded/Metalurgia/Form_RE10-0102_start (cla-project, vista)
- component_customs quitados: ['item.papoItemID']
- message_handlers quitados: ['saveStartShift']
- sends quitados: ['refreshPeriodic', 'refreshPreviewTable', 'refreshTable']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- transforms: 142 → 53
- n_scripts: 108 → 60

### Page/Embedded/Metalurgia/Form_RE11-0101_end (cla-project, vista)
- component_customs quitados: ['answers', 'item.papoItemID', 'key.answer']
- message_handlers quitados: ['saveEndShift']
- sends quitados: ['refreshPeriodic', 'refreshPreviewTable', 'refreshTable']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- transforms: 118 → 87
- n_scripts: 120 → 95

### Page/Embedded/Metalurgia/Form_RE11-0101_start (cla-project, vista)
- component_customs quitados: ['answers', 'item.papoItemID', 'key.answer']
- message_handlers quitados: ['saveStartRegister']
- sends quitados: ['refreshPeriodic', 'refreshPreviewTable', 'refreshTable', 'resetTable']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- transforms: 217 → 95
- n_scripts: 195 → 102

### Page/Embedded/Metalurgia/Form_SO02-1006_end (cla-project, vista)
- message_handlers quitados: ['saveStartRegister-2201-end']
- sends quitados: ['refreshPeriodic', 'refreshPreviewTable', 'refreshTable', 'resetTable']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- n_scripts: 13 → 12

### Page/Embedded/Metalurgia/Form_SO02-1006_hallazgo (cla-project, vista)
- component_customs quitados: ['answers']
- message_handlers quitados: ['saveStartShift']
- sends quitados: ['refreshPeriodic', 'refreshPreviewTable', 'refreshTable']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- transforms: 12 → 9
- n_scripts: 21 → 17

### Page/Embedded/Metalurgia/Form_SO02-1006_start (cla-project, vista)
- component_customs quitados: ['answers', 'item.papoItemID']
- message_handlers quitados: ['saveStartRegister']
- sends quitados: ['refreshPeriodic', 'refreshPreviewTable', 'refreshTable', 'resetTable']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- transforms: 95 → 29
- n_scripts: 83 → 37

### Page/Embedded/Metalurgia/Form_SO02-4502_end (cla-project, vista)
- message_handlers quitados: ['saveStartRegister-2201-end']
- sends quitados: ['refreshPeriodic', 'refreshPreviewTable', 'refreshTable', 'resetTable']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- n_scripts: 13 → 12

### Page/Embedded/Metalurgia/Form_SO02-4502_hallazgo (cla-project, vista)
- component_customs quitados: ['answers']
- message_handlers quitados: ['saveStartShift']
- sends quitados: ['refreshPeriodic', 'refreshPreviewTable', 'refreshTable']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- transforms: 12 → 9
- n_scripts: 21 → 17

### Page/Embedded/Metalurgia/Form_SO02-4502_start (cla-project, vista)
- component_customs quitados: ['answers', 'item.papoItemID']
- message_handlers quitados: ['saveStartShift']
- sends quitados: ['refreshPeriodic', 'refreshPreviewTable', 'refreshTable']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- transforms: 107 → 40
- n_scripts: 84 → 48

### Page/Embedded/Metalurgia/Form_TR11-0101_dia (cla-project, vista)
- component_customs quitados: ['item.papoItemID']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- transforms: 87 → 31
- n_scripts: 78 → 36

### Page/Embedded/Metalurgia/Form_TR11-0101_end (cla-project, vista)
- message_handlers quitados: ['saveStartRegister-2201-end']
- sends quitados: ['refreshPeriodic', 'refreshPreviewTable', 'refreshTable', 'resetTable']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- n_scripts: 9 → 8

### Page/Embedded/Metalurgia/Form_TR11-0101_start (cla-project, vista)
- component_customs quitados: ['answers', 'item.papoItemID']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- transforms: 247 → 52
- n_scripts: 205 → 58

### Page/Embedded/Metalurgia/Form_TR11-0102_end (cla-project, vista)
- message_handlers quitados: ['saveStartRegister-2201-end']
- sends quitados: ['refreshPeriodic', 'refreshPreviewTable', 'refreshTable', 'resetTable']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- n_scripts: 9 → 8

### Page/Embedded/Metalurgia/Form_TR11-0102_start (cla-project, vista)
- component_customs quitados: ['answers', 'item.papoItemID']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- transforms: 103 → 29
- n_scripts: 84 → 34

## Relaciones

- nuevas: embebe/abre 34, usa estilo 45
- eliminadas: maneja 18, envia 66, usa estilo 22