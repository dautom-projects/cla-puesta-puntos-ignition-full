# papo_core Wrapper Injection Rules

## Standard wrappers for Form views

### customMethods (root.scripts.customMethods)
- `toggleFlexRoot` (params: ["sectionIndex"]) → `papo_core.ui.toggleSection(self, sectionIndex)`
- `answerRecopile` (params: ["flexContainer"]) → `return papo_core.register.recopile(flexContainer, self)`

### messageHandlers (root.scripts.messageHandlers)
- `saveDataRoot` → `papo_core.register.save(self)`
- `signOperator` → `papo_core.sign.signOperator(self)`

### View-level onStartup (events.system.onStartup)
```python
self.custom.initialPapoDateTime = system.date.now()
papo_core.ui.initForm(self)
```
- With supervisor: add `self.custom.supervisorOption = papo_core.sign.supervisorOpt(self)` before initForm

### initialPapoDateTime format in view.json
Must be a timestamp object, NOT a string:
```json
"initialPapoDateTime": {"$": ["ts", 192, 0], "$ts": 0}
```

### custom.insights transform
- Script transform: `return papo_core.ui.preInsight(self, value)`

### Section{N} onClick script
```python
sectionIndex = int(self.meta.name.replace("Section", ""))
self.view.getChild("root").toggleFlexRoot(sectionIndex)
```

### Section{N} style.classes binding
- Property binding to `../FlexContainerGroup{N}.position.display`
- Map transform: true → "button-questions", false → "button-questions-2", fallback → "button-questions"

### Save button onClick
- `alerts.showAlert(state="warning", title="Guardar registro", message="Esta seguro de que desea guardar?", btnTextPrimary="Si", btnTextSecondary="No", btnActionPrimary="saveDataRoot")`

### Sign operator button onClick
- `alerts.showAlert(state="warning", title="Firmar PAPO", message="Esta seguro de que desea firmar el puesta a punto?", btnTextPrimary="Si", btnTextSecondary="No", btnActionPrimary="signOperator")`

## Legacy keys to remove from view.custom
answers, formato, test, flexGroupCount, flexCount, refreshSecond, dsTable_v3, dsTable_vJ, changedRegister

## Required keys in view.custom
dbConnection, initialPapoDateTime, registerTypeID, insights, user, sign, referencePapo

## Calling convention
- ALWAYS: `papo_core.modulo.funcion(self)`
- NEVER: `project.papo_core.modulo.funcion(self)`
