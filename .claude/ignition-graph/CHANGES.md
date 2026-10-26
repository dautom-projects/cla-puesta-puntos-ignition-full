# Cambios desde la corrida anterior

- Nodos nuevos: 0 · eliminados: 1
- Relaciones nuevas: 12 · eliminadas: 18
- Recursos con cambios internos: 4

## Nodos eliminados (1)

- Mensajes: **saveStartRegister** (cla-project)

## Cambios internos (4)

_Renombres de customs, params, handlers, componentes, funciones de script..._

### Page/Embedded/Metalurgia/Form_FU10-0202_dia (cla-project, vista)
- component_customs quitados: ['item.papoItemID']
- style_classes nuevos: ['PAPO/Field/Dropdown', 'PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']

### Page/Embedded/Metalurgia/Form_FU10-0202_end (cla-project, vista)
- message_handlers quitados: ['saveStartRegister-2201-end']
- sends quitados: ['refreshPeriodic', 'refreshPreviewTable', 'refreshTable', 'resetTable']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- n_scripts: 13 → 12

### Page/Embedded/Metalurgia/Form_FU10-0202_hallazgo (cla-project, vista)
- component_customs quitados: ['answers']
- message_handlers quitados: ['saveStartShift']
- sends quitados: ['refreshPeriodic', 'refreshPreviewTable', 'refreshTable']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- transforms: 12 → 9
- n_scripts: 21 → 17

### Page/Embedded/Metalurgia/Form_FU10-0202_start (cla-project, vista)
- component_customs quitados: ['answers', 'item.papoItemID']
- message_handlers quitados: ['saveStartRegister']
- sends quitados: ['refreshPeriodic', 'refreshPreviewTable', 'refreshTable', 'resetTable']
- style_classes nuevos: ['PAPO/Field/Input', 'PAPO/Form']
- style_classes quitados: ['dropdown']
- transforms: 7 → 4
- n_scripts: 15 → 11

## Relaciones

- nuevas: embebe/abre 3, usa estilo 9
- eliminadas: maneja 3, envia 11, usa estilo 4