# Mapa de dependencias Ignition

- Proyectos: 1 (cla-project)
- Vistas: 351
- Scripts de proyecto: 23
- Eventos (gateway y sesion): 2
- Mensajes: 70
- Tags referenciados: 264
- Paginas y docks: 8
- Clases de estilo: 105
- Session props: 5
- Relaciones: 4780 (usa tag 720, llama 666, embebe/abre 512, maneja 334, monta 8, envia 353, usa sesion 276, usa estilo 1911)
- Validacion de tags: sin definiciones cargadas (8.3: incluye `config/`; 8.1: usa `--tags`)

## Mayor impacto si cambian o se renombran

_Directo = quien lo usa. Transitivo = todo lo que termina afectado en cascada._

### Vistas
- **Alerts/alert** (cla-project) — directo 1, transitivo 270
- **Alerts/alertAndComment** (cla-project) — directo 1, transitivo 270
- **Objects/Checkbox** (cla-project) — directo 154, transitivo 156
- **Objects/TextField** (cla-project) — directo 123, transitivo 125
- **Page/PopUps/Authenticator** (cla-project) — directo 3, transitivo 106
- **Objects/Dropdown** (cla-project) — directo 90, transitivo 92
- **Objects/NumericField** (cla-project) — directo 60, transitivo 62
- **Objects/OptionGroup** (cla-project) — directo 11, transitivo 13
- **Node/MixingDashboard/Mixing Trend/Framework/Pen** (cla-project) — directo 7, transitivo 12
- **Page/Embedded/Title_Header** (cla-project) — directo 5, transitivo 9

### Scripts
- **logging** (cla-project) — directo 8, transitivo 277
- **alerts** (cla-project) — directo 19, transitivo 269
- **papo_core.ui** (cla-project) — directo 245, transitivo 247
- **papo_core.register** (cla-project) — directo 241, transitivo 243
- **papo_core.items** (cla-project) — directo 9, transitivo 186
- **papo_core.sign** (cla-project) — directo 101, transitivo 104
- **mes_core.sql** (cla-project) — directo 4, transitivo 22
- **mes_core.model** (cla-project) — directo 19, transitivo 21
- **mes_core.workOrder** (cla-project) — directo 4, transitivo 7
- **mes_core.schedule** (cla-project) — directo 3, transitivo 7

### Mensajes
- **deleteArea** (cla-project) — directo 6, transitivo 273
- **deleteEquipment** (cla-project) — directo 6, transitivo 273
- **deleteLine** (cla-project) — directo 6, transitivo 273
- **deletePlant** (cla-project) — directo 6, transitivo 273
- **deleteReason** (cla-project) — directo 6, transitivo 273
- **deleteRelation** (cla-project) — directo 6, transitivo 273
- **insertArea** (cla-project) — directo 6, transitivo 273
- **insertEquipment** (cla-project) — directo 6, transitivo 273
- **insertLine** (cla-project) — directo 6, transitivo 273
- **insertPlant** (cla-project) — directo 6, transitivo 273

### Tags
- **[UNS]Clarios/Andina/OREC/Linea 1/UI/EJ11-0101** ((tags)) — directo 62, transitivo 64
- **[UNS]Clarios/Andina/FA/Granja_Acidos/UI/GR10_0501** ((tags)) — directo 14, transitivo 14
- **[UNS]Clarios/Andina** ((tags)) — directo 5, transitivo 10
- **[UNS]Clarios/Andina/FA/Terminado/UI/AC10-0201** ((tags)) — directo 7, transitivo 9
- **[UNS]Clarios/Andina/FA/Formacion/UI/AC10-0202** ((tags)) — directo 8, transitivo 8
- **[UNS]Clarios/Andina/OREC/UI_JCI/EJ07_0101** ((tags)) — directo 8, transitivo 8
- **[uns]VIC/Manufacturing/Electrode Anode/Mixing Anode/ProcessMixing/CmcMixer/CmcWeight/Act_Value** ((tags)) — directo 8, transitivo 8
- **[uns]VIC/Manufacturing/Electrode Cathode/Mixing Cathode/ProcessMixing/SlurryPdMixer/Temperature/Act_Value** ((tags)) — directo 6, transitivo 8
- **[UNS]Clarios/Pacifico/Cubiertas/IMM 15/UI/Schedule/Dataset_excel** ((tags)) — directo 1, transitivo 8
- **[uns]VIC/Manufacturing/Electrode Anode/Mixing Anode/ProcessMixing/SlurryPdMixer1/Temperature/Act_Value** ((tags)) — directo 6, transitivo 7

### Clases de estilo
- **container-borders-dautom-widget** (cla-project) — directo 273, transitivo 285
- **text-description-centered** (cla-project) — directo 11, transitivo 278
- **text-titles** (cla-project) — directo 248, transitivo 274
- **Utilities/m-r-16** (cla-project) — directo 3, transitivo 273
- **Alerts/alertTitle** (cla-project) — directo 2, transitivo 272
- **alert-icons-margin** (cla-project) — directo 2, transitivo 272
- **container-alarms** (cla-project) — directo 2, transitivo 272
- **container-borders-dautom-alert** (cla-project) — directo 2, transitivo 272
- **container-padding-30** (cla-project) — directo 2, transitivo 272
- **text-description** (cla-project) — directo 2, transitivo 272

### Session props
- **session.custom.dbConnection** (cla-project) — directo 269, transitivo 276
- **session.custom.userSource** (cla-project) — directo 2, transitivo 107
- **session.custom.adminPermissions** (cla-project) — directo 3, transitivo 6
- **session.custom.filterOverview** (cla-project) — directo 1, transitivo 2
- **session.custom.shift** (cla-project) — directo 1, transitivo 1

## Vistas huerfanas (5)
_Nadie las usa (ni vistas, ni paginas, ni scripts) y no usan nada. Candidatas a limpieza._

- Page/Embedded/Metalurgia/Fundamental Views/Checkbox (cla-project)
- Page/Embedded/Metalurgia/Fundamental Views/Checkbox_Observation (cla-project)
- Page/Template/Breakpoint (cla-project)
- Page/ViewTest (cla-project)
- PowerChart (cla-project)

## Popups sin referentes (2)
_Probablemente se abren con una ruta armada en tiempo de ejecucion. Verificar._

- Page/PopUps/DateAndTime (cla-project)
- Page/PopUps/Test (cla-project)

## Referencias no resueltas (30)
_Algo se usa pero no existe en el proyecto ni en su cadena de herencia: tipico tras un **renombre** o borrado. Estilos y session props pueden venir de fuera (tema CSS, creacion dinamica); verificar antes de corregir._

### Vistas (9)
- `Components/MachineChip` — desde **Node/MixingDashboard/MixerCard**
- `Components/NodeLocation` — desde **Node/MixingDashboard/MixingDashboard**
- `Page/Digitalizacion_EA11-1101` — desde **Page/Digitalizacion_Reportes**
- `Page/Embedded/Widget OEE` — desde **Page/Template/Overview**
- `Page/Embedded/Widget OEE v3` — desde **Page/Template/Overview**
- `Page/PopUps/CreateOrEditSch` — desde **Mes Core/Schedule WO/Emb - ScheduleChart**
- `Page/Template/Breakpoint Embedded` — desde **Page/Template/Breakpoint**
- `UserManagement/Views/Popup_SaveError` — desde **Page/UserManagement/Views/Popups/Popup_SaveError**
- `UserManagement/Views/Popups/Popup_CheckRemoval` — desde **Page/UserManagement/Views/Popups/Popup_CheckRemoval**

### Scripts / modulos (runScript) (3)
- `yieldCalc.report` — desde **Page/Embedded/Ensamble/Form_EA11-1101_1h** (+59)
- `yieldCalc_AB.report` — desde **Page/Embedded/Ensamble/Form_EA11-1101_1h** (+59)
- `yieldCalc_C.report` — desde **Page/Embedded/Ensamble/Form_EA11-1101_1h** (+59)

### Clases de estilo (16)
- `--cla-text-question` — desde **Page/Embedded/Cubiertas/Form_PL11-0101-CU_start** (+1)
- `InputFont` — desde **Page/UserManagement/Views/Home**
- `Page/Page` — desde **Page/UserManagement/Views/AddEditRoles** (+2)
- `Page/Reports/border_1` — desde **Page/Overview_Papos**
- `ScheduleManagement/Headers` — desde **Page/UserManagement/Views/AddEditRoles**
- `ScheduleManagement/InputFont` — desde **Page/UserManagement/Views/AddEditUser**
- `Title/Title_0` — desde **Page/Embedded/Title_Header** (+1)
- `UserManagement/MainFont` — desde **Page/UserManagement/Tools/ContactInformation/Move Selection** (+4)
- `bg-[--neutral-10]gap-2` — desde **Node/MixingDashboard/MixerCard**
- `button-question` — desde **Node/MixingDashboard/Mixing Trend/Framework/LineRepeater**
- `datetime` — desde **Page/Embedded/GenericWidget_4**
- `gauge-fill-blue` — desde **Page/Template/Overview**
- `lg:w-21` — desde **Node/MixingDashboard/MixMetric**
- `some-class` — desde **Page/PopUps/Test**
- `text-title-2` — desde **Node/MixingDashboard/Mixing Trend/Framework/LineRepeater** (+1)
- `w-28` — desde **Node/MixingDashboard/MixerCard**

### Session props no declaradas (2)
- `cla-project: session.custom.adminPermissions` — desde **Docks/Tree_v2** (+2)
- `cla-project: session.custom.shift` — desde **Page/Embedded/F&A/Form_FO10-1701-1_start**

## Mensajes desbalanceados

_Senal fuerte de un messageType renombrado de un solo lado. Los envios con nombre en variable no se detectan, asi que un handler 'sin emisor' puede ser valido._

### Se envian y nadie los maneja (20)
- `confirmAction` (cla-project)
- `filterTable` (cla-project)
- `refreshRun` (cla-project)
- `refreshTable` (cla-project)
- `refreshTableMoldes` (cla-project)
- `refreshTableNode` (cla-project)
- `refreshTableReason` (cla-project)
- `refreshTableRelationLine` (cla-project)
- `refreshTableSKU` (cla-project)
- `refreshTableSKUMolde` (cla-project)
- `refreshTableSchedule` (cla-project)
- `refreshTableStandardRate` (cla-project)
- `refreshTableWO` (cla-project)
- `resetPreviewTable` (cla-project)
- `signatureCancelled` (cla-project)
- `signatureError` (cla-project)
- `signatureException` (cla-project)
- `signatureRoleDenied` (cla-project)
- `signatureTimeout` (cla-project)
- `trends` (cla-project)

### Se manejan y nadie los envia (13)
- `createRelation` (cla-project)
- `deleteSch` (cla-project)
- `deleteWO` (cla-project)
- `logout` (cla-project)
- `refresh` (cla-project)
- `refreshTableSch` (cla-project)
- `saveDataRoot` (cla-project)
- `signOperator` (cla-project)
- `signPapoSup` (cla-project)
- `signSuper` (cla-project)
- `signatureSuccess` (cla-project)
- `testLabel` (cla-project)
- `updateWaste` (cla-project)

## No analizado

- cla-project: 67 reportes, 1 ventanas vision (formato binario o modulo no cubierto)
