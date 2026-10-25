# PAPO lint

Generado: 2026-10-25 13:48 · Alcance: todo el proyecto · Vistas analizadas: 346

Generado por `.claude/skills/papo-lint/scripts/papo_lint.py` (solo lectura).

## Resumen por patrón

| Patrón | Vistas | Hallazgos |
|---|:-:|:-:|
| "papo_db" escrito en scripts o bindings | 117 | 263 |
| system.date.getHour24 / getHour24 | 5 | 16 |
| Último RegisterCode ordenado por Timestamp (o ID) | 45 | 45 |
| Llamada con prefijo project.papo_core | 0 | 0 |
| Claves legacy en view.custom | 12 | 12 |
| Form_*: onStartup sin papo_core.ui.initForm | 3 | 3 |
| Form_*: custom.insights sin preInsight | 3 | 3 |
| Form_*: toggleFlexRoot con params distintos de [sectionIndex] | 3 | 3 |
| Form_*: saveDataRoot sin papo_core.register | 3 | 3 |
| Form_*: answerRecopile sin papo_core.register | 3 | 3 |
| Form_*: campos sin clase de diseño PAPO/Field/* | 188 | 188 |
| Form_*: campo nativo que puede ser objeto estándar (papo_objects) | 187 | 187 |
| Form_*: message handler fuera del estándar (solo root/saveDataRoot) | 92 | 92 |
| Form_*: raíz sin la clase PAPO/Form | 238 | 238 |

Vistas con al menos un hallazgo: 249

## Detalle por vista

### `Page/Embedded/Metalurgia/Form_TR11-0101_start` (51)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_0/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_1/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_2/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_3/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_4/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_5/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_6/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_7/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_8/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_9/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_10/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_11/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_12/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_13/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_14/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_15/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_16/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_17/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_18/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_19/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_20/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_21/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_22/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_23/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_24/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_25/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_26/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_27/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_28/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_29/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_30/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_31/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_32/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_33/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_34/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_35/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_36/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_37/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_38/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_39/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_40/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_41/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_42/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_43/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_44/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_45/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_46/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_47/FlexContainer/Checkbox · propConfig.props.text.binding.transforms.0.code
- **Form_*: campos sin clase de diseño PAPO/Field/***: 145 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 145 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_TE11-0601_start` (14)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_2/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_2/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_1/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_1/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_1/FlexContainer_2/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_1/FlexContainer_3/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup3/S1/FlexContainer_0/Dropdown · propConfig.props.options.binding.transforms.0.code
- **Form_*: campos sin clase de diseño PAPO/Field/***: 45 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 41 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Cubiertas/Form_PL11-0101-CA_start` (11)

- **"papo_db" escrito en scripts o bindings**: root · scripts.messageHandlers.saveDataRoot.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root · scripts.messageHandlers.saveDataRoot.script
- **Claves legacy en view.custom**: test, refreshSecond
- **Form_*: onStartup sin papo_core.ui.initForm**: sin onStartup
- **Form_*: custom.insights sin preInsight**: binding sin preInsight
- **Form_*: toggleFlexRoot con params distintos de [sectionIndex]**: params ['groupIndex', 'sectionIndex', 'labelsHeight=210']
- **Form_*: saveDataRoot sin papo_core.register**: saveDataRoot con lógica propia
- **Form_*: answerRecopile sin papo_core.register**: answerRecopile con lógica propia
- **Form_*: campos sin clase de diseño PAPO/Field/***: 110 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 108 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Cubiertas/Form_PL11-0101-CU_start` (11)

- **"papo_db" escrito en scripts o bindings**: root · scripts.messageHandlers.saveDataRoot.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root · scripts.messageHandlers.saveDataRoot.script
- **Claves legacy en view.custom**: test, refreshSecond
- **Form_*: onStartup sin papo_core.ui.initForm**: sin onStartup
- **Form_*: custom.insights sin preInsight**: binding sin preInsight
- **Form_*: toggleFlexRoot con params distintos de [sectionIndex]**: params ['groupIndex', 'sectionIndex', 'labelsHeight=210']
- **Form_*: saveDataRoot sin papo_core.register**: saveDataRoot con lógica propia
- **Form_*: answerRecopile sin papo_core.register**: answerRecopile con lógica propia
- **Form_*: campos sin clase de diseño PAPO/Field/***: 102 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 102 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Cubiertas/Form_PL11-0101-S&A_start` (11)

- **"papo_db" escrito en scripts o bindings**: root · scripts.messageHandlers.saveDataRoot.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root · scripts.messageHandlers.saveDataRoot.script
- **Claves legacy en view.custom**: test, refreshSecond
- **Form_*: onStartup sin papo_core.ui.initForm**: sin onStartup
- **Form_*: custom.insights sin preInsight**: binding sin preInsight
- **Form_*: toggleFlexRoot con params distintos de [sectionIndex]**: params ['groupIndex', 'sectionIndex', 'labelsHeight=210']
- **Form_*: saveDataRoot sin papo_core.register**: saveDataRoot con lógica propia
- **Form_*: answerRecopile sin papo_core.register**: answerRecopile con lógica propia
- **Form_*: campos sin clase de diseño PAPO/Field/***: 155 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 155 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0201_start` (11)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_2/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_2/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_1/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_1/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **Form_*: campos sin clase de diseño PAPO/Field/***: 81 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 70 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0202-HD_start` (11)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_2/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_2/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_1/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_1/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **Form_*: campos sin clase de diseño PAPO/Field/***: 52 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 43 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0202-SLI_start` (11)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_2/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_2/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_1/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_1/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **Form_*: campos sin clase de diseño PAPO/Field/***: 51 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 42 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0202_start` (11)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_2/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_2/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_1/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_1/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **Form_*: campos sin clase de diseño PAPO/Field/***: 52 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 43 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0202_start D` (11)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_2/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_2/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_1/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_1/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **Form_*: campos sin clase de diseño PAPO/Field/***: 52 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 43 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0301_start` (10)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_2/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_1/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_1/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **Form_*: campos sin clase de diseño PAPO/Field/***: 36 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 36 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-1003_start` (10)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_2/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_1/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_1/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **Form_*: campos sin clase de diseño PAPO/Field/***: 30 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 30 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-1101_start` (10)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_2/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_1/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_1/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **Form_*: campos sin clase de diseño PAPO/Field/***: 37 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 37 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_GR10-0501_start` (10)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_2/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_1/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_1/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **Form_*: campos sin clase de diseño PAPO/Field/***: 284 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 217 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0501_start` (9)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_1/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_1/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **Form_*: campos sin clase de diseño PAPO/Field/***: 39 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 39 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0801_start` (9)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_1/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_1/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **Form_*: campos sin clase de diseño PAPO/Field/***: 35 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 35 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-1801_start` (9)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_2/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_1/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **Form_*: campos sin clase de diseño PAPO/Field/***: 64 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 49 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_CA02-2102_start` (9)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_1/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_1/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **Form_*: campos sin clase de diseño PAPO/Field/***: 50 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 50 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_FO10-0100_start` (9)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_1/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_1/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **Form_*: campos sin clase de diseño PAPO/Field/***: 14 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 14 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_FO10-0601_start` (9)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_0/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_1/FlexContainer_0/Image · propConfig.props.source.binding.transforms.0.code
- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer4/FlexContainer_1/FlexContainer_1/Image · propConfig.props.source.binding.transforms.0.code
- **Form_*: campos sin clase de diseño PAPO/Field/***: 13 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 13 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Gestion` (7)

- **system.date.getHour24 / getHour24**: (view) · propConfig.custom.endTime.binding.transforms.0.code
- **Último RegisterCode ordenado por Timestamp (o ID)**: (view) · propConfig.custom.signature.binding.transforms.0.code
- **system.date.getHour24 / getHour24**: (view) · propConfig.custom.startTime.binding.transforms.0.code
- **system.date.getHour24 / getHour24**: root/Filters/DateTimeInput_StartTime · events.system.onStartup.config.script
- **system.date.getHour24 / getHour24**: root/Filters/DateTimeInput_StartTime · propConfig.props.maxDate.binding.transforms.0.code
- **system.date.getHour24 / getHour24**: root/Filters/DateTimeInput_EndTime · events.system.onStartup.config.script
- **system.date.getHour24 / getHour24**: root/Filters/DateTimeInput_EndTime · propConfig.props.maxDate.binding.transforms.0.code

### `Page/Gestion Gerencia` (7)

- **Último RegisterCode ordenado por Timestamp (o ID)**: (view) · propConfig.custom.dataReports.binding.transforms.0.code
- **system.date.getHour24 / getHour24**: (view) · propConfig.custom.endTime.binding.transforms.0.code
- **system.date.getHour24 / getHour24**: (view) · propConfig.custom.startTime.binding.transforms.0.code
- **system.date.getHour24 / getHour24**: root/Filters/DateTimeInput_StartTime · events.system.onStartup.config.script
- **system.date.getHour24 / getHour24**: root/Filters/DateTimeInput_StartTime · propConfig.props.maxDate.binding.transforms.0.code
- **system.date.getHour24 / getHour24**: root/Filters/DateTimeInput_EndTime · events.system.onStartup.config.script
- **system.date.getHour24 / getHour24**: root/Filters/DateTimeInput_EndTime · propConfig.props.maxDate.binding.transforms.0.code

### `Page/Embedded/Ensamble/Form_EA11-4200_1h` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartRegister-4200-1h.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartRegister-4200-1h.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 26 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 22 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-4200-1h en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Metalurgia/Form_FU10-0202_hallazgo` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartShift.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartShift.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 2 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 2 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartShift en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Metalurgia/Form_FU10-0202_start` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartRegister.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartRegister.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 4 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 4 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Metalurgia/Form_FU11-0101_start` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartRegister.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartRegister.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 170 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 168 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Metalurgia/Form_PA11-0301_start` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartRegister-PTARI.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartRegister-PTARI.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 39 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 38 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-PTARI en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Metalurgia/Form_PA11-0401_start` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveEndShift.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveEndShift.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 19 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 19 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveEndShift en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Metalurgia/Form_RE10-0102_start` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartShift.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartShift.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 45 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 45 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartShift en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Metalurgia/Form_RE11-0101_end` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveEndShift.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveEndShift.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 77 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 77 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveEndShift en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Metalurgia/Form_RE11-0101_start` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartRegister.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartRegister.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 91 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 91 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Metalurgia/Form_SO02-1006_hallazgo` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartShift.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartShift.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 2 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 2 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartShift en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Metalurgia/Form_SO02-1006_start` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartRegister.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartRegister.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 43 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 43 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Metalurgia/Form_SO02-4502_hallazgo` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartShift.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartShift.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 2 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 2 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartShift en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Metalurgia/Form_SO02-4502_start` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartShift.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartShift.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 33 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 33 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartShift en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_CI11-0101_start` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartShift.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartShift.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 15 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 15 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartShift en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_CU11-0101_start` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartShift.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartShift.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 25 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 25 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartShift en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_EC07-0101_1h` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartShift.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartShift.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 1 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 1 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartShift en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_EC07-0101_end` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartShift.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartShift.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 4 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 4 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartShift en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_EC07-0101_start` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartShift.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartShift.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 1 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 1 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartShift en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_MZ07-0101_start` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartShift.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartShift.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 11 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 9 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartShift en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_MZ11-0101_4h` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply_0 · scripts.messageHandlers.saveStartShift.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply_0 · scripts.messageHandlers.saveStartShift.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 5 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 5 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartShift en Button_Apply_0
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_PO11-0101-1_start` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartShift.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartShift.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 12 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 11 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartShift en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_PO11-0101-2_start` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartShift.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartShift.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 12 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 11 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartShift en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_PO11-0101-3_start` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartShift.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartShift.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 12 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 11 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartShift en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_PO11-0101-4_start` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartShift.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartShift.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 12 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 11 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartShift en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_RJ11-0101-10_start` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply_0 · scripts.messageHandlers.saveStartShift.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply_0 · scripts.messageHandlers.saveStartShift.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 16 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 16 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartShift en Button_Apply_0
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_RJ11-0101-11_start` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply_0 · scripts.messageHandlers.saveStartShift.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply_0 · scripts.messageHandlers.saveStartShift.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 16 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 16 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartShift en Button_Apply_0
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_RJ11-0101-12_start` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply_0 · scripts.messageHandlers.saveStartShift.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply_0 · scripts.messageHandlers.saveStartShift.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 16 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 16 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartShift en Button_Apply_0
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_RJ11-0101-1_start` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply_0 · scripts.messageHandlers.saveStartShift.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply_0 · scripts.messageHandlers.saveStartShift.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 16 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 11 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartShift en Button_Apply_0
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_RJ11-0101-2_start` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply_0 · scripts.messageHandlers.saveStartShift.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply_0 · scripts.messageHandlers.saveStartShift.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 16 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 11 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartShift en Button_Apply_0
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_RJ11-0101-3_start` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply_0 · scripts.messageHandlers.saveStartShift.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply_0 · scripts.messageHandlers.saveStartShift.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 16 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 11 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartShift en Button_Apply_0
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_RJ11-0101-4_start` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply_0 · scripts.messageHandlers.saveStartShift.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply_0 · scripts.messageHandlers.saveStartShift.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 16 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 11 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartShift en Button_Apply_0
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_RJ11-0101-5_start` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply_0 · scripts.messageHandlers.saveStartShift.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply_0 · scripts.messageHandlers.saveStartShift.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 16 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 9 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartShift en Button_Apply_0
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_RJ11-0101-6_start` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply_0 · scripts.messageHandlers.saveStartShift.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply_0 · scripts.messageHandlers.saveStartShift.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 16 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 11 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartShift en Button_Apply_0
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_RJ11-0101-7_start` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply_0 · scripts.messageHandlers.saveStartShift.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply_0 · scripts.messageHandlers.saveStartShift.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 16 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 11 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartShift en Button_Apply_0
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_RJ11-0101-8_start` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply_0 · scripts.messageHandlers.saveStartShift.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply_0 · scripts.messageHandlers.saveStartShift.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 16 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 11 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartShift en Button_Apply_0
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_RJ11-0101-9_start` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply_0 · scripts.messageHandlers.saveStartShift.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply_0 · scripts.messageHandlers.saveStartShift.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 16 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 11 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartShift en Button_Apply_0
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_SO02-4502_hallazgo` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartShift.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartShift.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 2 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 2 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartShift en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_SO02-4502_start` (6)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartShift.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartShift.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 33 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 33 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartShift en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-0901_1h` (5)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveFourHourRegister.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 68 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 42 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveFourHourRegister en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-0901_2h` (5)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveTwoHourRegister.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 59 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 46 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveTwoHourRegister en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-0901_30min` (5)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply_0 · scripts.messageHandlers.saveHourRegister_test.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 2 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 2 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveHourRegister_test en Button_Apply_0
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-0901_4h` (5)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveFourHourRegister.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 63 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 48 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveFourHourRegister en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-1601_4h` (5)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveFourHourRegister.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 1 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 1 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveFourHourRegister en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-1601_SKU` (5)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-4101-sku.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 1 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 1 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-4101-sku en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-2501_2h` (5)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartRegister-2501-2h.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 25 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 25 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-2501-2h en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-2601_2h` (5)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartRegister-2501-2h.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 25 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 25 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-2501-2h en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-4101_1h` (5)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-4101-1h.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 2 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 2 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-4101-1h en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-4101_2h` (5)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-4101-1h.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 20 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 18 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-4101-1h en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-4101_SKU` (5)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-4101-sku.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 1 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 1 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-4101-sku en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-4101_end` (5)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-4101-end.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 1 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 1 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-4101-end en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-4101_start` (5)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-4101-start.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 20 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 20 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-4101-start en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-4200_2h` (5)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-4200-2h.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 34 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 26 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-4200-2h en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-4200_mitad` (5)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-4200-mid.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 1 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 1 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-4200-mid en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-4200_start` (5)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-4200-start.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 51 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 47 campos convertibles
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-4200-start en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_EJ11-0101_1h` (5)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartShift.script
- **Último RegisterCode ordenado por Timestamp (o ID)**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveStartShift.script
- **Form_*: campos sin clase de diseño PAPO/Field/***: 1 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartShift en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_CG10-0101_item` (4)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/S1/FlexContainer_0/Dropdown · propConfig.props.options.binding.transforms.0.code
- **Form_*: campos sin clase de diseño PAPO/Field/***: 8 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 8 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_FO10-1701_output` (4)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/FlexContainer_3/Dropdown · propConfig.props.options.binding.transforms.0.code
- **Form_*: campos sin clase de diseño PAPO/Field/***: 18 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 18 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_TE11-0601_30min` (4)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/S1/FlexContainer_0/Dropdown · propConfig.props.options.binding.transforms.0.code
- **Form_*: campos sin clase de diseño PAPO/Field/***: 20 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 16 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_TE11-0601_SKU` (4)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainerGroup1/S1/FlexContainer_0/Dropdown · propConfig.props.options.binding.transforms.0.code
- **Form_*: campos sin clase de diseño PAPO/Field/***: 20 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 16 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Metalurgia/Form_FU10-0202_dia` (4)

- **system.date.getHour24 / getHour24**: (view) · propConfig.custom.shift.binding.transforms.0.code
- **Form_*: campos sin clase de diseño PAPO/Field/***: 42 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 42 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Metalurgia/Form_TR11-0102_start` (4)

- **system.date.getHour24 / getHour24**: (view) · propConfig.custom.shift.binding.transforms.0.code
- **Form_*: campos sin clase de diseño PAPO/Field/***: 25 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 25 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_EJ11-0101_start` (4)

- **Claves legacy en view.custom**: refreshSecond
- **Form_*: campos sin clase de diseño PAPO/Field/***: 20 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 18 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_EJ11-0102_start` (4)

- **Claves legacy en view.custom**: refreshSecond
- **Form_*: campos sin clase de diseño PAPO/Field/***: 5 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 2 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-0901_end` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 3 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 2 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-0901_start` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 22 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 20 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-1101_1h` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 41 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 25 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-1101_start` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 17 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 17 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-1201_1h` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 18 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 18 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-1201_2h` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 20 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 20 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-1201_start` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 31 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 29 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-1501_1h` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 4 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 4 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-1501_2h` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 24 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 24 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-1501_30min` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 2 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 2 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-1501_start` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 22 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 22 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-1601_1h` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 8 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 8 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-1601_2h` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 30 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 30 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-1601_start` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 23 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 23 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-1603_1h` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 33 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 33 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-1603_start` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 17 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 17 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-2201_1h` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 31 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 12 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-2201_2h` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 24 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 24 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-2201_start` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 9 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 9 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-2501_1h` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 4 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 4 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-2501_30min` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 2 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 2 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-2501_end` (3)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-2501-end.script
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-2501-end en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-2501_start` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 22 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 22 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-2601_1h` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 15 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 13 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-2601_end` (3)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-2501-end.script
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-2501-end en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-2601_start` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 19 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 19 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-4200_end` (3)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-4200-end.script
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-4200-end en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0201_30min` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 36 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 25 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0201_30min D` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 48 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 37 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0201_SKU` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 36 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 25 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0201_SKU D` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 48 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 37 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0201_end` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 5 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 5 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0201_mmto` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 38 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 27 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0202-HD_30min` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 20 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 11 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0202-HD_SKU` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 20 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 11 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0202-HD_end` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 5 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 5 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0202-HD_mmto` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 29 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 21 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0202-SLI_30min` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 20 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 11 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0202-SLI_SKU` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 20 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 11 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0202-SLI_end` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 5 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 5 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0202-SLI_mmto` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 29 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 21 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0202_30min` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 20 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 11 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0202_30min D` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 30 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 22 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0202_SKU` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 20 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 11 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0202_SKU D` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 30 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 22 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0202_end` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 5 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 5 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0202_mmto` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 30 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 22 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0301_SKU` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 13 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 13 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0301_end` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 5 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 5 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0301_mmto` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 13 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 13 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0501_30min` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 17 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 17 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0501_SKU` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 17 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 17 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0501_end` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 5 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 5 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0501_mmto` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 17 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 17 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0801_30min` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 15 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 15 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0801_SKU` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 15 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 15 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0801_end` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 6 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 6 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-0801_mmto` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 15 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 15 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-1003_30min` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 11 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 11 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-1003_SKU` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 11 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 11 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-1003_end` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 5 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 5 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-1003_mmto` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 11 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 11 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-1101_30min` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 15 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 15 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-1101_SKU` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 15 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 15 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-1101_end` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 5 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 5 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-1101_mmto` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 15 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 15 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-1801_30min` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 49 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 35 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-1801_SKU` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 49 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 35 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-1801_end` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 5 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 5 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-1801_mmto` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 51 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 37 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_AC10-1801_reject` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 4 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 4 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_CA02-2102_30min` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 30 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 30 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_CA02-2102_SKU` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 30 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 30 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_CA02-2102_end` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 5 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 5 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_CA02-2102_mmto` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 30 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 30 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_CG10-0101_start` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 1 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 1 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_FO10-0100_end` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 5 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 5 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_FO10-0100_input` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 19 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 8 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_FO10-0601_end` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 6 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 5 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_FO10-0601_input` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 21 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 12 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_FO10-1701-1_end` (3)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-2201-end.script
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-2201-end en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_FO10-1701-1_start` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 9 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 8 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_FO10-1701_end` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 5 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 5 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_FO10-1701_start` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 13 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 13 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_GR10-0501_end` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 5 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 5 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_PT11-0104_end` (3)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-2201-end.script
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-2201-end en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_PT11-0104_start` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 37 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 36 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_TE11-0401_defects` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 3 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 2 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_TE11-0401_end` (3)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-2201-end.script
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-2201-end en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_TE11-0601_end` (3)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-2201-end.script
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-2201-end en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_TE11-0601_reject` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 4 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 4 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_TE11-2601_end` (3)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-2201-end.script
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-2201-end en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_TE11-2601_start` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 44 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 39 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form__end` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 5 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 5 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/General/Form_PL11-0101-CA_start` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 112 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 110 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/General/Form_PL11-0101-CU_start` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 102 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 102 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/General/Form_PL11-0101-S&A_start` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 155 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 155 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Metalurgia/Form_FU10-0202_end` (3)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-2201-end.script
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-2201-end en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Metalurgia/Form_FU11-0101_end` (3)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-2201-end.script
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-2201-end en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Metalurgia/Form_PA11-0301_end` (3)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-2201-end.script
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-2201-end en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Metalurgia/Form_PA11-0401_end` (3)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-2201-end.script
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-2201-end en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Metalurgia/Form_RE10-0102_end` (3)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-2201-end.script
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-2201-end en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Metalurgia/Form_SO02-1006_end` (3)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-2201-end.script
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-2201-end en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Metalurgia/Form_SO02-4502_end` (3)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-2201-end.script
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-2201-end en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Metalurgia/Form_TR11-0101_dia` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 28 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 28 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Metalurgia/Form_TR11-0101_end` (3)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-2201-end.script
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-2201-end en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Metalurgia/Form_TR11-0102_end` (3)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-2201-end.script
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-2201-end en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_CU11-0101_end` (3)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-2201-end.script
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-2201-end en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_EC07-0101_barcada` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 24 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 23 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_EC11-0101_end` (3)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-2201-end.script
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-2201-end en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_EC11-0101_start` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 19 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 18 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_EJ07-0101_barcada` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 19 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 18 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_EJ07-0101_start` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 1 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 1 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_EJ11-0101_end` (3)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-2201-end.script
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-2201-end en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_EJ11-0102_end` (3)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-2201-end.script
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-2201-end en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_MZ07-0101_30min` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 25 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 14 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_MZ07-0101_end` (3)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-2201-end.script
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-2201-end en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_MZ11-0101_end` (3)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-2201-end.script
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-2201-end en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_MZ11-0101_start` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 17 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 17 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_PO07-0101_paro` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 12 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 12 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_PO07-0101_start` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 72 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 42 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_RJ07-0101_SKU` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 7 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 7 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_RJ07-0101_end` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 4 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 2 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_RJ07-0101_start` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 64 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 56 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_RJ07_0101_end` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 4 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 4 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_RJ07_0101_start` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 48 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 41 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_RJ11-0101-10_end` (3)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-2201-end.script
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-2201-end en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_RJ11-0101-11_end` (3)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-2201-end.script
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-2201-end en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_RJ11-0101-12_end` (3)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-2201-end.script
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-2201-end en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_RJ11-0101-1_end` (3)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-2201-end.script
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-2201-end en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_RJ11-0101-2_end` (3)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-2201-end.script
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-2201-end en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_RJ11-0101-3_end` (3)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-2201-end.script
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-2201-end en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_RJ11-0101-4_end` (3)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-2201-end.script
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-2201-end en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_RJ11-0101-5_end` (3)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-2201-end.script
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-2201-end en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_RJ11-0101-6_end` (3)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-2201-end.script
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-2201-end en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_RJ11-0101-7_end` (3)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-2201-end.script
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-2201-end en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_RJ11-0101-8_end` (3)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-2201-end.script
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-2201-end en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_RJ11-0101-9_end` (3)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-2201-end.script
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-2201-end en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_SO02-4502_end` (3)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer/Button_Apply · scripts.messageHandlers.saveStartRegister-2201-end.script
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveStartRegister-2201-end en Button_Apply
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/POLY/Form_PL11-0101-CAJA_start` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 115 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 113 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/POLY/Form_PL11-0101-CUBIERTA_start` (3)

- **Form_*: campos sin clase de diseño PAPO/Field/***: 97 campos sin clase PAPO/Field/* (papo-design)
- **Form_*: campo nativo que puede ser objeto estándar (papo_objects)**: 97 campos convertibles
- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Overview_Papos` (3)

- **system.date.getHour24 / getHour24**: root/FlexContainer_Reports/FlexContainer_main/FlexContainer_Menu/DateTimeInput_StartTime · events.system.onStartup.config.script
- **system.date.getHour24 / getHour24**: root/FlexContainer_Reports/FlexContainer_main/FlexContainer_Menu/DateTimeInput_EndTime · events.system.onStartup.config.script
- **Claves legacy en view.custom**: viewOn

### `Page/Digitalizacion_Template` (2)

- **Último RegisterCode ordenado por Timestamp (o ID)**: root · scripts.messageHandlers.signOperator.script
- **Claves legacy en view.custom**: refreshSecond, changedRegister, viewOn

### `Page/Embedded/Ensamble/Form_EA11-0901_1h_PruebaPiloto` (2)

- **"papo_db" escrito en scripts o bindings**: root/FlexContainer_0/Button_Apply · scripts.messageHandlers.saveFourHourRegister.script
- **Form_*: message handler fuera del estándar (solo root/saveDataRoot)**: saveFourHourRegister en Button_Apply

### `Mes Core/Dashboard Line/Emb - NodeState` (1)

- **Claves legacy en view.custom**: viewOn

### `Mes Core/Dashboard Line/Vw - Main` (1)

- **Claves legacy en view.custom**: viewOn

### `Page/CP-pk` (1)

- **Claves legacy en view.custom**: viewOn

### `Page/Embedded/Embedded_PAPO` (1)

- **Claves legacy en view.custom**: viewOn

### `Page/Embedded/Ensamble/Form_EA11-1101_end` (1)

- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-1201_end` (1)

- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-1501_end` (1)

- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-1601_end` (1)

- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-1603_end` (1)

- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/Ensamble/Form_EA11-2201_end` (1)

- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/F&A/Form_CG10-0101_end` (1)

- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_CI11-0101_end` (1)

- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_EJ07-0101_end` (1)

- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_PO11-0101-1_end` (1)

- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_PO11-0101-2_end` (1)

- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_PO11-0101-3_end` (1)

- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_PO11-0101-4_end` (1)

- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/OREC/Form_RJ07_0101_sku` (1)

- **Form_*: raíz sin la clase PAPO/Form**: sin PAPO/Form

### `Page/Embedded/test` (1)

- **"papo_db" escrito en scripts o bindings**: root/Label · propConfig.props.text.binding.transforms.0.code

### `Page/Template/Overview` (1)

- **Claves legacy en view.custom**: viewOn
