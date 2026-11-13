# Estado de migración de vistas Form_* a papo_core

Fuente: `.claude/ignition-graph/impact.json` (corrida del 2026-10-22, 338 vistas en total). Una ✔ indica que la vista llama a ese módulo.

Criterio: **completa** = usa `ui` y `register` (los wrappers que cubre `PROCEDIMIENTO_ESTANDARIZACION.md`); **parcial** = usa solo uno de los dos; **sin migrar** = no usa ninguno. `sign`, `report` y `overview` se muestran pero no cuentan: las firmas viven en Digitalizacion_Template y report/overview no aplican a los formularios.

| Vista | ui | register | sign | report | overview | Estado |
|---|:-:|:-:|:-:|:-:|:-:|---|
| `Page/Embedded/Cubiertas/Form_PL11-0101-CA_start` | ✔ |  |  |  |  | Parcial |
| `Page/Embedded/Cubiertas/Form_PL11-0101-CU_start` | ✔ |  |  |  |  | Parcial |
| `Page/Embedded/Cubiertas/Form_PL11-0101-S&A_start` | ✔ |  |  |  |  | Parcial |
| `Page/Embedded/Ensamble/Form_EA11-0901_1h` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-0901_2h` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-0901_30min` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-0901_4h` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-0901_end` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-0901_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-1101_1h` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-1101_end` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-1101_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-1201_1h` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-1201_2h` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-1201_end` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-1201_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-1501_1h` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-1501_2h` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-1501_30min` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-1501_end` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-1501_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-1601_1h` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-1601_2h` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-1601_4h` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-1601_SKU` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-1601_end` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-1601_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-1603_1h` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-1603_end` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-1603_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-2201_1h` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-2201_2h` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-2201_end` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-2201_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-2501_1h` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-2501_2h` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-2501_30min` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-2501_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-2501_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-2601_1h` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-2601_2h` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-2601_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-2601_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-4101_1h` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-4101_2h` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-4101_SKU` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-4101_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-4101_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-4200_1h` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-4200_2h` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-4200_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-4200_mitad` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/Ensamble/Form_EA11-4200_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0201_30min` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0201_30min D` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0201_SKU` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0201_SKU D` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0201_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0201_mmto` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0201_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0202-HD_30min` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0202-HD_SKU` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0202-HD_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0202-HD_mmto` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0202-HD_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0202-SLI_30min` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0202-SLI_SKU` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0202-SLI_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0202-SLI_mmto` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0202-SLI_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0202_30min` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0202_30min D` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0202_SKU` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0202_SKU D` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0202_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0202_mmto` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0202_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0202_start D` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0301_SKU` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0301_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0301_mmto` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0301_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0501_30min` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0501_SKU` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0501_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0501_mmto` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0501_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0801_30min` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0801_SKU` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0801_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0801_mmto` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-0801_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-1003_30min` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-1003_SKU` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-1003_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-1003_mmto` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-1003_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-1101_30min` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-1101_SKU` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-1101_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-1101_mmto` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-1101_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-1801_30min` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-1801_SKU` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-1801_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-1801_mmto` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-1801_reject` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_AC10-1801_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/F&A/Form_CA02-2102_30min` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_CA02-2102_SKU` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_CA02-2102_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_CA02-2102_mmto` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_CA02-2102_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/F&A/Form_CG10-0101_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_CG10-0101_item` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_CG10-0101_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/F&A/Form_FO10-0100_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_FO10-0100_input` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_FO10-0100_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/F&A/Form_FO10-0601_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_FO10-0601_input` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_FO10-0601_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/F&A/Form_FO10-1701-1_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_FO10-1701-1_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/F&A/Form_FO10-1701_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_FO10-1701_output` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_FO10-1701_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/F&A/Form_GR10-0501_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_GR10-0501_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/F&A/Form_PT11-0104_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_PT11-0104_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/F&A/Form_TE11-0401_defects` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_TE11-0401_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_TE11-0601_30min` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_TE11-0601_SKU` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_TE11-0601_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_TE11-0601_reject` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_TE11-0601_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/F&A/Form_TE11-2601_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/F&A/Form_TE11-2601_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/F&A/Form__end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/General/Form_PL11-0101-CA_start` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/General/Form_PL11-0101-CU_start` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/General/Form_PL11-0101-S&A_start` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/Metalurgia/Form_FU10-0202_dia` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/Metalurgia/Form_FU10-0202_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/Metalurgia/Form_FU10-0202_hallazgo` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/Metalurgia/Form_FU10-0202_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Metalurgia/Form_FU11-0101_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/Metalurgia/Form_FU11-0101_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Metalurgia/Form_PA11-0301_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/Metalurgia/Form_PA11-0301_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Metalurgia/Form_PA11-0401_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/Metalurgia/Form_PA11-0401_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Metalurgia/Form_RE10-0102_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/Metalurgia/Form_RE10-0102_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Metalurgia/Form_RE11-0101_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/Metalurgia/Form_RE11-0101_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Metalurgia/Form_SO02-1006_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/Metalurgia/Form_SO02-1006_hallazgo` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/Metalurgia/Form_SO02-1006_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Metalurgia/Form_SO02-4502_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/Metalurgia/Form_SO02-4502_hallazgo` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/Metalurgia/Form_SO02-4502_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Metalurgia/Form_TR11-0101_dia` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/Metalurgia/Form_TR11-0101_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/Metalurgia/Form_TR11-0101_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/Metalurgia/Form_TR11-0102_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/Metalurgia/Form_TR11-0102_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/OREC/Form_CI11-0101_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_CI11-0101_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/OREC/Form_CU11-0101_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_CU11-0101_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/OREC/Form_EC07-0101_1h` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_EC07-0101_barcada` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_EC07-0101_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_EC07-0101_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/OREC/Form_EC11-0101_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_EC11-0101_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/OREC/Form_EJ07-0101_barcada` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_EJ07-0101_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_EJ07-0101_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/OREC/Form_EJ11-0101_1h` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_EJ11-0101_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_EJ11-0101_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/OREC/Form_EJ11-0102_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_EJ11-0102_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/OREC/Form_MZ07-0101_30min` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_MZ07-0101_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_MZ07-0101_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/OREC/Form_MZ11-0101_4h` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_MZ11-0101_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_MZ11-0101_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/OREC/Form_PO07-0101_paro` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_PO07-0101_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/OREC/Form_PO11-0101-1_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_PO11-0101-1_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/OREC/Form_PO11-0101-2_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_PO11-0101-2_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/OREC/Form_PO11-0101-3_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_PO11-0101-3_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/OREC/Form_PO11-0101-4_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_PO11-0101-4_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/OREC/Form_RJ07-0101_SKU` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_RJ07-0101_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_RJ07-0101_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/OREC/Form_RJ07_0101_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_RJ07_0101_sku` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_RJ07_0101_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/OREC/Form_RJ11-0101-10_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_RJ11-0101-10_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/OREC/Form_RJ11-0101-11_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_RJ11-0101-11_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/OREC/Form_RJ11-0101-12_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_RJ11-0101-12_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/OREC/Form_RJ11-0101-1_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_RJ11-0101-1_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/OREC/Form_RJ11-0101-2_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_RJ11-0101-2_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/OREC/Form_RJ11-0101-3_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_RJ11-0101-3_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/OREC/Form_RJ11-0101-4_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_RJ11-0101-4_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/OREC/Form_RJ11-0101-5_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_RJ11-0101-5_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/OREC/Form_RJ11-0101-6_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_RJ11-0101-6_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/OREC/Form_RJ11-0101-7_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_RJ11-0101-7_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/OREC/Form_RJ11-0101-8_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_RJ11-0101-8_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/OREC/Form_RJ11-0101-9_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_RJ11-0101-9_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/OREC/Form_SO02-4502_end` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_SO02-4502_hallazgo` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/OREC/Form_SO02-4502_start` | ✔ | ✔ | ✔ |  |  | Completa |
| `Page/Embedded/POLY/Form_PL11-0101-CAJA_start` | ✔ | ✔ |  |  |  | Completa |
| `Page/Embedded/POLY/Form_PL11-0101-CUBIERTA_start` | ✔ | ✔ |  |  |  | Completa |

## Totales

- Vistas Form_*: 238
- Completamente migradas: 235
- Parciales: 3
- Sin migrar: 0
- Además usan `sign` (supervisorOpt en onStartup): 94

Parciales: solo llaman a `papo_core.ui.confirmSave()` desde el botón Guardar; les faltan initForm, preInsight, toggleSection, recopile y save.
