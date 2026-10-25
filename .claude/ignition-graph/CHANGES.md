# Cambios desde la corrida anterior

- Nodos nuevos: 7 · eliminados: 0
- Relaciones nuevas: 92 · eliminadas: 4
- Recursos con cambios internos: 4

## Nodos nuevos (7)

- Vistas: **Objects/DateTime** (cla-project)
- Vistas: **Objects/OptionGroup** (cla-project)
- Vistas: **Page/Embedded/Ensamble/Form_EA11-1601_start_PruebaPiloto** (cla-project)
- Vistas: **Page/Embedded/F&A/Form_AC10-0201_start_PruebaPiloto** (cla-project)
- Vistas: **Page/Embedded/F&A/Form_GR10-0501_start_PruebaPiloto** (cla-project)
- Vistas: **Page/Embedded/OREC/Form_CU11-0101_start_PruebaPiloto** (cla-project)
- Vistas: **Page/Embedded/OREC/Form_PO11-0101-2_start_PruebaPiloto** (cla-project)

## Cambios internos (4)

_Renombres de customs, params, handlers, componentes, funciones de script..._

### Objects/Dropdown (cla-project, vista)
- params nuevos: ['emptyAnswer']

### Objects/NumericField (cla-project, vista)
- params nuevos: ['emptyAnswer']
- transforms: 3 → 4
- n_scripts: 3 → 4

### Objects/TextField (cla-project, vista)
- params nuevos: ['emptyAnswer']
- transforms: 1 → 2
- n_scripts: 1 → 2

### Page/Embedded/Ensamble/Form_EA11-0901_1h_PruebaPiloto (cla-project, vista)
- message_handlers quitados: ['saveFourHourRegister']
- sends quitados: ['refreshPeriodic', 'refreshPreviewTable', 'refreshTable']
- n_scripts: 21 → 20

## Relaciones

- nuevas: usa tag 3, llama 17, embebe/abre 19, maneja 5, envia 5, usa sesion 7, usa estilo 36
- eliminadas: maneja 1, envia 3