# Cambios desde la corrida anterior

- Nodos nuevos: 0 · eliminados: 0
- Relaciones nuevas: 1 · eliminadas: 4
- Recursos con cambios internos: 8

## Cambios internos (8)

_Renombres de customs, params, handlers, componentes, funciones de script..._

### Page/Digitalizacion_Template (cla-project, vista)
- style_classes quitados: ['Page/themes']

### Page/Embedded/General/Form_PL11-0101-CU_start (cla-project, vista)
- style_classes quitados: ['--cla-text-question']

### Page/Embedded/General/Form_PL11-0101-S&A_start (cla-project, vista)
- style_classes quitados: ['--cla-text-question']

### Page/Embedded/OREC/Form_EC07-0101_barcada (cla-project, vista)
- customs quitados: ['refreshSecond']
- component_customs nuevos: ['questions']
- message_handlers quitados: ['saveStartShift']
- sends quitados: ['refreshPeriodic', 'refreshPreviewTable', 'refreshTable']
- transforms: 56 → 57

### Page/Embedded/POLY/Form_PL11-0101-CUBIERTA_start (cla-project, vista)
- style_classes quitados: ['--cla-text-question']

### Page/Overview_Papos (cla-project, vista)
- style_classes quitados: ['Page/themes']

### papo_core.items (cla-project, script)
- nombres nuevos: ['getQuestionText', 'getQuestions']

### papo_core.ui (cla-project, script)
- nombres nuevos: ['getShift']

## Relaciones

- nuevas: llama 1
- eliminadas: maneja 1, envia 3