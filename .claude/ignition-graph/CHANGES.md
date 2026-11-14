# Cambios desde la corrida anterior

- Nodos nuevos: 6 · eliminados: 75
- Relaciones nuevas: 542 · eliminadas: 140
- Recursos con cambios internos: 192

## Posibles renombres

- Paginas y docks: `dock compartido left:#0` → `dock compartido left:menu` (verificar)

## Nodos nuevos (6)

- Paginas y docks: **dock compartido left:menu** (cla-project)
- Paginas y docks: **page /manageAdministration** (cla-project)
- Clases de estilo: **PAPO/Tablet/Group** (cla-project)
- Clases de estilo: **PAPO/Tablet/ObjectRow** (cla-project)
- Clases de estilo: **PAPO/Tablet/Row** (cla-project)
- Tags referenciados: **[uns]** ((tags))

## Nodos eliminados (75)

- Mensajes: **deleteSch** (cla-project)
- Mensajes: **deleteWO** (cla-project)
- Mensajes: **refresh** (cla-project)
- Mensajes: **refreshRun** (cla-project)
- Mensajes: **refreshTableSch** (cla-project)
- Mensajes: **refreshTableSchedule** (cla-project)
- Mensajes: **refreshTableWO** (cla-project)
- Mensajes: **refreshWorkOrders** (cla-project)
- Mensajes: **updateDatabase** (cla-project)
- Mensajes: **updateSchedule** (cla-project)
- Paginas y docks: **dock compartido left:#0** (cla-project)
- Clases de estilo: **text-subtitle-widget** (cla-project)
- Tags referenciados: **[System]Gateway/SystemName** ((tags))
- Tags referenciados: **[UNS]** ((tags))
- Tags referenciados: **[default]BMS/90BR/AHU/AHU1/AHU1_CFM_Total** ((tags))
- Tags referenciados: **[default]BMS/90BR/AHU/AHU2/AHU2_CFM_Total** ((tags))
- Tags referenciados: **[default]BMS/90BR/vav/_global/request_cool_pct** ((tags))
- Tags referenciados: **[default]BMS/90BR/vav/_global/request_heat_pct** ((tags))
- Tags referenciados: **[default]BMS/90BR/vav/_global/request_peakcool_pct** ((tags))
- Tags referenciados: **[default]BMS/90BR/vav/_global/temp_avg_building** ((tags))
- Tags referenciados: **[default]BMS/90BR/vav/_global/temp_avg_floor1** ((tags))
- Tags referenciados: **[default]BMS/90BR/vav/_global/temp_avg_floor2** ((tags))
- Tags referenciados: **[default]BMS/Blue/hvac/ac1/cntl/building_static_pressure** ((tags))
- Tags referenciados: **[default]BMS/Blue/hvac/ac1/cntl/cond_water_temp** ((tags))
- Tags referenciados: **[default]BMS/Blue/hvac/ac1/cntl/duct_static_pressure** ((tags))
- Tags referenciados: **[default]BMS/Blue/hvac/ac1/cntl/outside_air_temp** ((tags))
- Tags referenciados: **[default]BMS/Blue/hvac/ac1/cntl/return_air_temp** ((tags))
- Tags referenciados: **[default]BMS/Blue/hvac/ac1/cntl/supply_air_temp** ((tags))
- Tags referenciados: **[default]BMS/Blue/hvac/ac1/cntl/supply_static_pressure** ((tags))
- Tags referenciados: **[default]BMS/Blue/hvac/ac1/comp1/status** ((tags))
- ...y 45 mas

## Cambios internos (192)

_Renombres de customs, params, handlers, componentes, funciones de script..._

### Alerts/alert (cla-project, vista)
- customs nuevos: ['sent']

### Objects/DateTime (cla-project, vista)
- params nuevos: ['displayFormat']

### Page/Embedded/Cubiertas/Form_PL11-0101-CA_start (cla-project, vista)
- style_classes nuevos: ['PAPO/Tablet/Group', 'PAPO/Tablet/ObjectRow', 'PAPO/Tablet/Row']

### Page/Embedded/Cubiertas/Form_PL11-0101-CU_start (cla-project, vista)
- style_classes nuevos: ['PAPO/Tablet/Group', 'PAPO/Tablet/ObjectRow', 'PAPO/Tablet/Row']

### Page/Embedded/Cubiertas/Form_PL11-0101-S&A_start (cla-project, vista)
- style_classes nuevos: ['PAPO/Tablet/Group', 'PAPO/Tablet/ObjectRow', 'PAPO/Tablet/Row']

### Page/Embedded/Ensamble/Form_EA11-0901_1h (cla-project, vista)
- style_classes nuevos: ['PAPO/Tablet/Group', 'PAPO/Tablet/ObjectRow', 'PAPO/Tablet/Row']

### Page/Embedded/Ensamble/Form_EA11-0901_1h_PruebaPiloto (cla-project, vista)
- style_classes nuevos: ['PAPO/Tablet/Group', 'PAPO/Tablet/ObjectRow', 'PAPO/Tablet/Row']

### Page/Embedded/Ensamble/Form_EA11-0901_2h (cla-project, vista)
- style_classes nuevos: ['PAPO/Tablet/Group', 'PAPO/Tablet/ObjectRow', 'PAPO/Tablet/Row']

### Page/Embedded/Ensamble/Form_EA11-0901_30min (cla-project, vista)
- style_classes nuevos: ['PAPO/Tablet/Group', 'PAPO/Tablet/ObjectRow', 'PAPO/Tablet/Row']

### Page/Embedded/Ensamble/Form_EA11-0901_4h (cla-project, vista)
- style_classes nuevos: ['PAPO/Tablet/Group', 'PAPO/Tablet/ObjectRow', 'PAPO/Tablet/Row']

### Page/Embedded/Ensamble/Form_EA11-0901_end (cla-project, vista)
- style_classes nuevos: ['PAPO/Tablet/Group', 'PAPO/Tablet/ObjectRow', 'PAPO/Tablet/Row']

### Page/Embedded/Ensamble/Form_EA11-0901_start (cla-project, vista)
- component_customs quitados: ['item.papoItemID']
- style_classes nuevos: ['PAPO/Tablet/Group', 'PAPO/Tablet/ObjectRow', 'PAPO/Tablet/Row']

### Page/Embedded/Ensamble/Form_EA11-1101_1h (cla-project, vista)
- component_customs nuevos: ['item_dev.answer']
- style_classes nuevos: ['PAPO/Tablet/Group', 'PAPO/Tablet/ObjectRow', 'PAPO/Tablet/Row']

### Page/Embedded/Ensamble/Form_EA11-1101_start (cla-project, vista)
- style_classes nuevos: ['PAPO/Tablet/Group', 'PAPO/Tablet/ObjectRow']

### Page/Embedded/Ensamble/Form_EA11-1201_1h (cla-project, vista)
- style_classes nuevos: ['PAPO/Tablet/Group', 'PAPO/Tablet/ObjectRow', 'PAPO/Tablet/Row']

### Page/Embedded/Ensamble/Form_EA11-1201_2h (cla-project, vista)
- style_classes nuevos: ['PAPO/Tablet/Group', 'PAPO/Tablet/ObjectRow', 'PAPO/Tablet/Row']

### Page/Embedded/Ensamble/Form_EA11-1201_start (cla-project, vista)
- style_classes nuevos: ['PAPO/Tablet/Group', 'PAPO/Tablet/ObjectRow', 'PAPO/Tablet/Row']

### Page/Embedded/Ensamble/Form_EA11-1501_1h (cla-project, vista)
- style_classes nuevos: ['PAPO/Tablet/Group', 'PAPO/Tablet/ObjectRow', 'PAPO/Tablet/Row']

### Page/Embedded/Ensamble/Form_EA11-1501_2h (cla-project, vista)
- style_classes nuevos: ['PAPO/Tablet/Group', 'PAPO/Tablet/ObjectRow', 'PAPO/Tablet/Row']

### Page/Embedded/Ensamble/Form_EA11-1501_30min (cla-project, vista)
- style_classes nuevos: ['PAPO/Tablet/Group', 'PAPO/Tablet/ObjectRow', 'PAPO/Tablet/Row']

### Page/Embedded/Ensamble/Form_EA11-1501_start (cla-project, vista)
- style_classes nuevos: ['PAPO/Tablet/Group', 'PAPO/Tablet/ObjectRow', 'PAPO/Tablet/Row']

### Page/Embedded/Ensamble/Form_EA11-1601_1h (cla-project, vista)
- style_classes nuevos: ['PAPO/Tablet/Group', 'PAPO/Tablet/ObjectRow', 'PAPO/Tablet/Row']

### Page/Embedded/Ensamble/Form_EA11-1601_2h (cla-project, vista)
- style_classes nuevos: ['PAPO/Tablet/Group', 'PAPO/Tablet/ObjectRow', 'PAPO/Tablet/Row']

### Page/Embedded/Ensamble/Form_EA11-1601_4h (cla-project, vista)
- style_classes nuevos: ['PAPO/Tablet/Group', 'PAPO/Tablet/ObjectRow']

### Page/Embedded/Ensamble/Form_EA11-1601_SKU (cla-project, vista)
- style_classes nuevos: ['PAPO/Tablet/Group', 'PAPO/Tablet/ObjectRow']

### Page/Embedded/Ensamble/Form_EA11-1601_start (cla-project, vista)
- style_classes nuevos: ['PAPO/Tablet/Group', 'PAPO/Tablet/ObjectRow']

### Page/Embedded/Ensamble/Form_EA11-1601_start_PruebaPiloto (cla-project, vista)
- style_classes nuevos: ['PAPO/Tablet/Group', 'PAPO/Tablet/ObjectRow']

### Page/Embedded/Ensamble/Form_EA11-1603_1h (cla-project, vista)
- component_customs nuevos: ['item_dev.answer']
- style_classes nuevos: ['PAPO/Tablet/Group', 'PAPO/Tablet/ObjectRow', 'PAPO/Tablet/Row']

### Page/Embedded/Ensamble/Form_EA11-1603_start (cla-project, vista)
- style_classes nuevos: ['PAPO/Tablet/Group', 'PAPO/Tablet/ObjectRow']

### Page/Embedded/Ensamble/Form_EA11-2201_1h (cla-project, vista)
- style_classes nuevos: ['PAPO/Tablet/Group', 'PAPO/Tablet/ObjectRow', 'PAPO/Tablet/Row']

## Relaciones

- nuevas: llama 2, maneja 1, monta 2, usa estilo 537
- eliminadas: usa tag 52, llama 17, embebe/abre 14, maneja 9, monta 1, envia 9, usa sesion 8, usa estilo 30