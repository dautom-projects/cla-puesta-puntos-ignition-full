# Procedimiento de estandarización — vistas Form_* a papo_core

Plantilla: `cla-project/com.inductiveautomation.perspective/views/Page/Embedded/Ensamble/Form_EA11-1501_30min/view.json` (sin firma). Variante con `supervisorOpt`: `Page/Embedded/Ensamble/Form_EA11-0901_1h`. Extraído el 2026-10-22.

**Alcance:** solo vistas `Form_*`, módulos `papo_core.ui` y `papo_core.register`. Las firmas de operario y supervisor viven en `Page/Digitalizacion_Template` y quedan **fuera** de este procedimiento.

Estado actual: ver `MIGRATION_STATUS.md`. Estructura JSON de cada pieza para inyección en lote: `CONTEXT_AUTOMATIZACION_JSON.md`.

## 0. Antes de empezar

1. Backup del `view.json` (p. ej. `view.json.bak-AAAAMMDD`).
2. Abrir la plantilla `Page/Embedded/Ensamble/Form_EA11-1501_30min` como referencia.
3. Confirmar que el package `papo_core` (ui, register) ya está desplegado en el gateway: **el módulo se despliega antes que la vista que lo llama**.

## 1. Requisitos de estructura (los exige el código de papo_core)

- Los grupos de preguntas son hijos **directos** de `root` y se llaman `FlexContainerGroup1..N`, **consecutivos desde 1**: `register.save` recorre `range(1, count + 1)` con `root.getChild("FlexContainerGroup{}")`.
- Cada grupo tiene su cabecera `Section1..N` (hija directa de `root`, `ia.display.label`), con el mismo índice: `ui.toggleSection` empareja `SectionN` ↔ `FlexContainerGroupN` por nombre.
- Si hay contenedor de supervisor, se llama `FlexContainerSupervisor` (se excluye del conteo y se agrega aparte).
- Cada campo de respuesta conserva su `custom.item` (`papoItemID`, `registerTypeID`) y el binding de `custom.item.answer`. **No tocar.** Ejemplo de la plantilla:

```json
{
  "custom": {
    "item": {
      "papoItemID": 11079,
      "registerTypeID": 3
    }
  },
  "propConfig": {
    "custom.item.answer": {
      "binding": {
        "config": {
          "path": "this.props.selected"
        },
        "transforms": [
          {
            "fallback": "none",
            "inputType": "scalar",
            "mappings": [
              {
                "input": true,
                "output": "Cumple"
              },
              {
                "input": false,
                "output": "No Cumple"
              }
            ],
            "outputType": "scalar",
            "type": "map"
          }
        ],
        "type": "property"
      }
    },
    "props.style.fontSize": {
      "binding": {
        "config": {
          "path": "view.custom.fontSize"
        },
        "type": "property"
      }
    }
  }
}
```

- `view.custom` debe tener al menos: `dbConnection` (bindeado a `session.custom.dbConnection`), `registerTypeID`, `referencePapo`, `insights`, `initialPapoDateTime`. Y `view.params`: `papoID`, `nodeID`, `workstationID`, `workstationnodeID`.

Binding de `custom.dbConnection` en la plantilla (nunca hardcodear):

```json
{
  "binding": {
    "config": {
      "path": "session.custom.dbConnection"
    },
    "type": "property"
  },
  "persistent": true
}
```

## 2. Custom methods de root

En `root.scripts.customMethods`. Reemplazar las versiones inline por estos wrappers (idénticos en las 235 vistas migradas):

**toggleFlexRoot** — param `sectionIndex`

```json
{
  "name": "toggleFlexRoot",
  "params": [
    "sectionIndex"
  ],
  "script": "\tpapo_core.ui.toggleSection(self, sectionIndex)"
}
```

**answerRecopile** — param `flexContainer`

```json
{
  "name": "answerRecopile",
  "params": [
    "flexContainer"
  ],
  "script": "\treturn papo_core.register.recopile(flexContainer, self)"
}
```

## 3. Message handler de root

En `root.scripts.messageHandlers`. Scope: **solo page** (`pageScope: true`, `sessionScope: false`, `viewScope: false`). Idéntico en las 235 vistas:

```json
{
  "messageType": "saveDataRoot",
  "pageScope": true,
  "script": "\tpapo_core.register.save(self)",
  "sessionScope": false,
  "viewScope": false
}
```

## 4. onStartup de la vista

En `events.system.onStartup` del **nivel view** (raíz del `view.json`, no del componente root). Forma usada por 140 vistas:

```json
{
  "config": {
    "script": "\tself.custom.initialPapoDateTime = system.date.now()\n\tpapo_core.ui.initForm(self)"
  },
  "scope": "G",
  "type": "script"
}
```

Las vistas que muestran el dropdown de supervisor agregan una línea con `papo_core.sign.supervisorOpt` (forma de `Page/Embedded/Ensamble/Form_EA11-0901_1h`, 73 vistas). Se documenta solo para no romperla: no forma parte de este procedimiento.

```json
{
  "config": {
    "script": "\tself.custom.initialPapoDateTime = system.date.now()\n\tself.custom.supervisorOption = papo_core.sign.supervisorOpt(self)\n\tpapo_core.ui.initForm(self)"
  },
  "scope": "G",
  "type": "script"
}
```

## 5. Transform de custom.insights

En `propConfig["custom.insights"]` del nivel view: binding de propiedad al `TextField` de comentarios + transform script. Idéntico en 234 de 235 vistas:

```json
{
  "binding": {
    "config": {
      "path": "/root/TextField.props.text"
    },
    "transforms": [
      {
        "code": "\treturn papo_core.ui.preInsight(self, value)",
        "type": "script"
      }
    ],
    "type": "property"
  },
  "persistent": true
}
```

## 6. onClick de cada Section

En `events.dom.onClick` de cada `SectionN`. Forma mayoritaria (303 ocurrencias), tomada de `Section1` de la plantilla:

```json
{
  "config": {
    "script": "\tsectionIndex = int(self.meta.name.replace(\"Section\", \"\"))\n\tself.view.getChild(\"root\").toggleFlexRoot(sectionIndex)"
  },
  "scope": "G",
  "type": "script"
}
```

Variante documentada con docstring (46 ocurrencias, `Page/Embedded/Ensamble/Form_EA11-0901_1h`), funcionalmente igual:

```json
{
  "config": {
    "script": "\t\"\"\"\n\tSection button onClick - trigger accordion toggle.\n\t\n\tVersion: 1.1.0\n\t\n\tChangelog:\n\t\t2026-07-05 | William | v1.0.0 - Initial version\n\t\t2026-07-05 | William | v1.1.0 - Dynamic, hierarchy-independent\n\t\"\"\"\n\t\n\t# Extract section index from component name\n\tsectionIndex = int(self.meta.name.replace(\"Section\", \"\"))\n\t\n\t# Trigger accordion toggle on root\n\tself.view.getChild(\"root\").toggleFlexRoot(sectionIndex)"
  },
  "scope": "G",
  "type": "script"
}
```

## 7. onClick del botón Guardar

En `events.dom.onClick` del botón Guardar (`Button_Apply_0`, `ia.input.button`; en otras vistas se llama `Button_Apply`). El botón solo dispara el diálogo; al confirmar se envía `saveDataRoot`:

```json
{
  "config": {
    "script": "\tpapo_core.ui.confirmSave()"
  },
  "scope": "G",
  "type": "script"
}
```

## 8. Validar

1. El JSON parsea: `python3 -c "import json; json.load(open('view.json'))"`.
2. No quedan `def` inline de recolección/guardado en root (solo los wrappers de arriba).
3. Los `custom.item` siguen intactos (comparar conteo antes/después).
4. Re-scan del proyecto en el gateway; abrir la vista, expandir secciones, guardar y revisar `registerhistory`.
5. Volver a correr el grafo (`ignition-graph`) y confirmar que la vista pasa a "Completa" en `MIGRATION_STATUS.md`.

## Pendientes conocidos

- `Cubiertas/Form_PL11-0101-CA_start`, `-CU_start` y `-S&A_start`: solo tienen el wrapper del botón Guardar (`confirmSave`); faltan los pasos 2–6.
- `OREC/Form_MZ11-0101_4h`: el botón Guardar todavía llama a `alerts.showAlert(...)` inline en vez de `papo_core.ui.confirmSave()`.
- `F&A/Form_AC10-0201_start`: el transform de `custom.insights` tiene un `return value` muerto después del wrapper.
