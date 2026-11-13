# Automatización de wrappers en view.json

Plantilla: `cla-project/com.inductiveautomation.perspective/views/Page/Embedded/Ensamble/Form_EA11-1501_30min/view.json` (sin firma). Variante con `supervisorOpt`: `Page/Embedded/Ensamble/Form_EA11-0901_1h`. Extraído el 2026-10-22.

Mapa de dónde vive cada wrapper dentro de `view.json` y con qué claves, para inyectarlos en lote. Rutas expresadas como claves JSON desde la raíz del archivo.

## Esqueleto relevante de un view.json migrado

```text
view.json
├── custom{ dbConnection, registerTypeID, referencePapo, insights, initialPapoDateTime, ... }
├── params{ papoID, nodeID, workstationID, workstationnodeID }
├── propConfig
│   ├── "custom.dbConnection"  → binding a session.custom.dbConnection
│   └── "custom.insights"      → binding + transform papo_core.ui.preInsight      [W5]
├── events.system.onStartup     → papo_core.ui.initForm                             [W4]
└── root (ia.container.flex)
    ├── scripts.customMethods[]  → toggleFlexRoot, answerRecopile                   [W1, W2]
    ├── scripts.messageHandlers[]→ saveDataRoot                                     [W3]
    └── children[]
        ├── SectionN (ia.display.label) .events.dom.onClick                         [W6]
        ├── FlexContainerGroupN (ia.container.flex) → campos con custom.item
        ├── TextField (comentarios, fuente de custom.insights)
        └── FlexContainer_0.children[] → Button_Apply_0 / Button_Apply .events.dom.onClick  [W7]
```

## W1 — `root.scripts.customMethods[] (name == "toggleFlexRoot")`

```json
{
  "name": "toggleFlexRoot",
  "params": [
    "sectionIndex"
  ],
  "script": "\tpapo_core.ui.toggleSection(self, sectionIndex)"
}
```

Reemplazar el elemento con ese `name`; si no existe, agregarlo.

## W2 — `root.scripts.customMethods[] (name == "answerRecopile")`

```json
{
  "name": "answerRecopile",
  "params": [
    "flexContainer"
  ],
  "script": "\treturn papo_core.register.recopile(flexContainer, self)"
}
```

Igual que W1.

## W3 — `root.scripts.messageHandlers[] (messageType == "saveDataRoot")`

```json
{
  "messageType": "saveDataRoot",
  "pageScope": true,
  "script": "\tpapo_core.register.save(self)",
  "sessionScope": false,
  "viewScope": false
}
```

Reemplazar el elemento con ese `messageType`; conservar los demás handlers.

## W4 — `events.system.onStartup`

```json
{
  "config": {
    "script": "\tself.custom.initialPapoDateTime = system.date.now()\n\tpapo_core.ui.initForm(self)"
  },
  "scope": "G",
  "type": "script"
}
```

Objeto (no lista). Si la vista ya llama `supervisorOpt`, conservar esa línea (ver variante abajo). Ojo: 17 vistas lo tienen como lista de un elemento; normalizar a objeto o mantener la forma existente.

## W5 — `propConfig["custom.insights"]`

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

La clave literal es `"custom.insights"` (con punto) dentro de `propConfig`. `config.path` apunta al TextField de comentarios de esa vista: verificar el nombre.

## W6 — `root.children[i].events.dom.onClick  (meta.name =~ ^Section\d+$)`

```json
{
  "config": {
    "script": "\tsectionIndex = int(self.meta.name.replace(\"Section\", \"\"))\n\tself.view.getChild(\"root\").toggleFlexRoot(sectionIndex)"
  },
  "scope": "G",
  "type": "script"
}
```

Aplicar a cada `SectionN`. El índice sale del nombre, así que el script es el mismo para todas.

## W7 — `<botón Guardar>.events.dom.onClick  (meta.name in Button_Apply_0, Button_Apply)`

```json
{
  "config": {
    "script": "\tpapo_core.ui.confirmSave()"
  },
  "scope": "G",
  "type": "script"
}
```

El botón está anidado (en la plantilla: `root/FlexContainer_0/Button_Apply_0`); buscarlo recursivo por nombre. No confundir con `Button_Apply_1` (cerrar).

### Variante de W4 con supervisorOpt

```json
{
  "config": {
    "script": "\tself.custom.initialPapoDateTime = system.date.now()\n\tself.custom.supervisorOption = papo_core.sign.supervisorOpt(self)\n\tpapo_core.ui.initForm(self)"
  },
  "scope": "G",
  "type": "script"
}
```

## Claves comunes de un script de evento

- Eventos (`events.*`): `{"config": {"script": "..."}, "scope": "G", "type": "script"}`.
- Custom methods: `{"name", "params": [...], "script"}`. Message handlers: `{"messageType", "pageScope", "sessionScope", "viewScope", "script"}`.
- Transforms script: `{"code": "...", "type": "script"}` dentro de `binding.transforms[]`.
- El cuerpo de todo script empieza con `\t` (indentación de Ignition) y usa `\n\t` entre líneas; tabs, nunca espacios.

## Reglas para la inyección en lote

1. Backup de cada `view.json` antes de escribir.
2. Cargar con `json.load`, modificar el dict y escribir con `json.dump(obj, f, indent=2, ensure_ascii=False)` + `sort_keys=True` (Ignition guarda las claves ordenadas). Verificar el diff: solo deben cambiar los nodos W1–W7.
3. Validar que el resultado parsea y que el número de `custom.item` no cambió.
4. Identificar elementos por `name` / `messageType` / `meta.name`, nunca por índice.
5. Después: re-scan del proyecto y nueva corrida de `ignition-graph` para confirmar en `MIGRATION_STATUS.md`.
