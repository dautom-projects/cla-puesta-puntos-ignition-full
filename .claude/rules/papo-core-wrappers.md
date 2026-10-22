# papo_core Wrapper Injection Rules

Verified against `Page/Embedded/Ensamble/Form_EA11-1501_30min` (no supervisor) and
`Page/Embedded/Ensamble/Form_EA11-0901_1h` (with supervisor) on 2026-10-22.
Exact JSON of each wrapper: `.claude/docs/CONTEXT_AUTOMATIZACION_JSON.md`.

## Standard wrappers for Form views

### customMethods (root.scripts.customMethods)
- `toggleFlexRoot` (params: ["sectionIndex"]) → `papo_core.ui.toggleSection(self, sectionIndex)`
- `answerRecopile` (params: ["flexContainer"]) → `return papo_core.register.recopile(flexContainer, self)`

### messageHandlers (root.scripts.messageHandlers)
- `saveDataRoot` → `papo_core.register.save(self)` — pageScope: true, sessionScope: false, viewScope: false
- Form views have no `signOperator` handler: operator/supervisor signatures live in `Page/Digitalizacion_Template`

### View-level onStartup (events.system.onStartup)
```python
self.custom.initialPapoDateTime = system.date.now()
papo_core.ui.initForm(self)
```
- With supervisor: add `self.custom.supervisorOption = papo_core.sign.supervisorOpt(self)` before initForm (also used by non-start forms, e.g. Form_EA11-0901_1h)

### initialPapoDateTime format in view.json
Must be a timestamp object, NOT a string:
```json
"initialPapoDateTime": {"$": ["ts", 192, 0], "$ts": 0}
```

### custom.insights transform
- Property binding to `/root/TextField.props.text` + script transform: `return papo_core.ui.preInsight(self, value)`

### Section{N} onClick script
```python
sectionIndex = int(self.meta.name.replace("Section", ""))
self.view.getChild("root").toggleFlexRoot(sectionIndex)
```

### Section{N} style.classes binding
- Property binding to `../FlexContainerGroup{N}.position.display`
- Map transform: true → "button-questions", false → "button-questions-2", fallback → "button-questions"

### Save button onClick (Button_Apply / Button_Apply_0)
- `papo_core.ui.confirmSave()` — shows the standard confirmation and sends `saveDataRoot` on confirm

### Cancel button onClick (Button_Apply_1)
- `system.perspective.sendMessage(messageType="closeEmbeded", payload={"estado": False,}, scope="session")`

## Legacy keys to remove from view.custom
answers, formato, test, flexGroupCount, flexCount, refreshSecond, dsTable_v3, dsTable_vJ, changedRegister

## Required keys in view.custom
dbConnection, initialPapoDateTime, registerTypeID, insights, user, sign, referencePapo
- With supervisor: also `supervisorOption`

## Calling convention
- ALWAYS: `papo_core.modulo.funcion(self)`
- NEVER: `project.papo_core.modulo.funcion(self)`
