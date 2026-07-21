# Procedimiento de Estandarización de Formularios PAPO
**Versión:** 2.0.0 — 2026-07-20
**Arquitectura:** Toda la lógica vive en el Project Library package `papo_core`. Cada vista solo tiene **wrappers de una línea** que llaman a la librería.

## Package papo_core
```
project/
└── papo_core/
    ├── register.py    # recopile, save
    ├── ui.py          # toggleSection, initForm, preInsight
    ├── sign.py        # supervisorOpt, signOperator, requestSupervisorAuth, signSupervisor, authenticateAndSign
    ├── report.py      # extractReportData
    └── overview.py    # getPapoListFiltered, getCardPath
```
**Requisito previo:** el package `papo_core` debe estar instalado en el Project Library del gateway antes de aplicar este procedimiento.

---

## Herramientas disponibles

| Herramienta | Uso |
|---|---|
| `standardize_view.py` | Aplica pasos 1-9 automáticamente usando raw text manipulation |
| `sync_view.py` | Sincroniza view.json con Designer (version MAX+2 vs gateway) |
| `inspect_view.py` | Extrae scripts, bindings, customs para verificación rápida |
| `/sync` | Skill que invoca sync_view.py o sentinel según el tipo de archivo |

---

# Vista: Form_XXXX_start / Form_XXXX_end / Form_XXXX_1h / Form_XXXX_30min

---

## PASO 1 — Identificar TODAS las Section{N} y FlexContainerGroup{N}

**CRÍTICO:** Un formulario puede tener 1, 2, 3 o más secciones. Los pasos 2, 3 y 4 se aplican a **TODAS** las secciones, no solo a Section1.

- [ ] Listar todas las Section{N} presentes en el view.json
- [ ] Verificar que cada Section{N} corresponda a su FlexContainerGroup{N} por número
- [ ] **Validar correspondencia en AMBAS direcciones:** toda `Section{N}` debe tener su `FlexContainerGroup{N}`, y todo `FlexContainerGroup{N}` su `Section{N}` (sin huérfanos). A veces se agrega una y falta la otra → binding roto. `check_sections.py` / `validate_all.py` reportan `MISSING FlexContainerGroupN` y `ORPHAN` (colección recursiva, no solo hijos directos del root).
- [ ] Renombrar si es necesario para que coincidan (Section1↔FlexContainerGroup1, Section2↔FlexContainerGroup2, etc.)

---

## PASO 2 — Binding de clase en CADA Section (repetir por cada N)

Para **cada** Section{N} encontrada:

- [ ] En `Section{N}.props.style.classes` → Property Binding a `../FlexContainerGroup{N}.position.display`

**Transform Map (igual para todas las secciones):**

|Input|Output|
|---|---|
|true|"button-questions"|
|false|"button-questions-2"|
|Fallback|"button-questions"|

---

## PASO 3 — onClick en CADA Section (repetir por cada N)

Para **cada** Section{N} encontrada:

- [ ] Agregar/reemplazar dom.onClick:
```python
sectionIndex = int(self.meta.name.replace("Section", ""))
self.view.getChild("root").toggleFlexRoot(sectionIndex)
```

**Nota:** El script es IDÉNTICO para todas las secciones — `self.meta.name` se resuelve dinámicamente.

---

## PASO 4 — FlexContainerGroups: display y limpieza (repetir por cada N)

Para **cada** FlexContainerGroup{N}:

- [ ] Agregar `"display": false` en `position` (colapsar por defecto)
- [ ] Eliminar `custom.answers` del FlexContainerGroup (binding/script reactivo legacy)
- [ ] Verificar que cada campo dentro tenga `custom.item` con `{papoItemID, answer, registerTypeID}`

---

## PASO 5 — Limpiar view.custom

### Eliminar (legacy) — valor en `view.custom`:
- [ ] `answers`
- [ ] `formato`
- [ ] `test`
- [ ] `flexGroupCount` (ahora dinámico en papo_core)
- [ ] `flexCount` (ahora dinámico en papo_core)
- [ ] **`refreshSecond`** — quitar SIEMPRE el valor `view.custom.refreshSecond` si el form lo tiene
- [ ] `dsTable_v3`, `dsTable_vJ`
- [ ] `changedRegister`
- [ ] `supervisorOption` (solo el valor estático — ahora se puebla en onStartup)

### Eliminar de propConfig (legacy bindings, nivel-vista):
- [ ] `custom.answers*` (cualquier sufijo: startShift, supervisor, oneHour, condiciones, etc.)
- [ ] `custom.db` (si existe, renombrado a dbConnection)
- [ ] **`custom.refreshSecond`** — quitar también el binding del propConfig raíz
- [ ] `custom.test`, `custom.formato`, `custom.flexGroupCount`, `custom.flexCount`, `custom.dsTable_v3`, `custom.dsTable_vJ`, `custom.changedRegister`

> **Nota:** `standardize_view_v2.py` (STEP 4 + 4b) elimina automáticamente el valor `refreshSecond` del bloque `custom` Y el binding `custom.refreshSecond` del propConfig **nivel-vista**. Los `custom.refreshSecond` a **nivel-componente** (dentro de propConfig de hijos, indentación profunda) NO se tocan — son de otro alcance.
> **NO eliminar** `custom.path`: la referencia dorada (Form_EA11-2501_1h) lo conserva.

### Crear/Verificar:
- [ ] `dbConnection` (string, valor: `"papo_db"`) → binding a `session.custom.dbConnection`
- [ ] `initialPapoDateTime` (timestamp object) → se setea en onStartup
- [ ] `registerTypeID` (int) → 7 (start), 3 (30min), etc.
- [ ] `insights` (string) → con transform (Paso 7)
- [ ] `user` (string)
- [ ] `sign` (string, vacío)
- [ ] `referencePapo` (string, vacío)

### Formato de initialPapoDateTime en JSON:
```json
"initialPapoDateTime": {"$": ["ts", 192, 0], "$ts": 0}
```
**NUNCA** usar string vacío `""` — causa TypeError en preInsight.

---

## PASO 6 — onStartup script en view

### Con supervisor (forms _start y _end):
```python
self.custom.initialPapoDateTime = system.date.now()
self.custom.supervisorOption = papo_core.sign.supervisorOpt(self)
papo_core.ui.initForm(self)
```

### Sin supervisor (forms _1h, _30min, _2h, _mitad, _SKU):
```python
self.custom.initialPapoDateTime = system.date.now()
papo_core.ui.initForm(self)
```

**CRÍTICO:** Si ya existe un onStartup con script legacy (supervisor dropdown inline, etc.), REEMPLAZAR el script completo. No solo insertar cuando falta.

---

## PASO 7 — Transform en view.custom.insights (pre-insight)

En `view.custom.insights` agregar/verificar script transform:
```python
return papo_core.ui.preInsight(self, value)
```

---

## PASO 8 — Custom Methods en root.scripts

**CRÍTICO:** Estos van en `root.scripts.customMethods`, NO en el bloque scripts de ningún componente hijo.

### toggleFlexRoot
- [ ] **Nombre:** `toggleFlexRoot`
- [ ] **Parámetros:** `["sectionIndex"]`
- [ ] **Script:** `papo_core.ui.toggleSection(self, sectionIndex)`

### answerRecopile
- [ ] **Nombre:** `answerRecopile`
- [ ] **Parámetros:** `["flexContainer"]`
- [ ] **Script:** `return papo_core.register.recopile(flexContainer, self)`

---

## PASO 9 — Message Handlers en root.scripts

**CRÍTICO:** Estos van en `root.scripts.messageHandlers`, NO en componentes hijos.

### saveDataRoot
- [ ] **Message Type:** `saveDataRoot`
- [ ] **Script:** `papo_core.register.save(self)`
- [ ] **pageScope:** true

### signOperator (si aplica — forms con firma)
- [ ] **Message Type:** `signOperator`
- [ ] **Script:** `papo_core.sign.signOperator(self)`
- [ ] **pageScope:** true

---

## PASO 10 — onClick del botón Guardar (Button_Apply)

- [ ] Reemplazar CUALQUIER script legacy (`alerts.showAlert(...)` inline, con cualquier
      mensaje de confirmación) por el wrapper de una línea:
```python
papo_core.ui.confirmSave()
```
- [ ] Mensaje FIJO para todos los forms (definido dentro de `confirmSave`, NO varía por form):
      `"Esta seguro de que desea guardar el registro"`
- [ ] `confirmSave()` internamente llama a `alerts.showAlert(...)` con `btnActionPrimary="saveDataRoot"`

- [ ] **Verificar** que el botón NO tenga un bloque `"scripts"` propio — si lo tiene, eliminarlo. Los scripts van SOLO en `root.scripts`.

---

## PASO 10.5 — Canonicalizar (CRÍTICO: evita reordenamiento del Designer)

El Designer/Gson serializa las llaves en orden **alfabético**. Los scripts insertan
llaves nuevas al inicio del bloque, rompiendo ese orden; al guardar, el Designer
re-ordena TODO → diff gigante ("reordenamiento de objetos"). Para evitarlo,
canonicalizar el view.json a orden Gson ANTES del sync:

```bash
python C:/Users/willi/.claude/scripts/canonicalize_view.py "<ruta>/view.json"
```

- Re-serializa exactamente como Gson (sort_keys + escapes HTML) — verificado byte-idéntico.
- Aborta si el contenido cambia (solo reordena llaves).
- Tras esto, un save del Designer produce **0 diff**.

## PASO 11 — Sync y Pruebas

### Pipeline completo por cada vista:
```bash
python C:/Users/willi/.claude/scripts/standardize_view_v2.py "<ruta>/view.json"
python C:/Users/willi/.claude/scripts/fix_all_sections.py   "<ruta>/view.json"
python C:/Users/willi/.claude/scripts/canonicalize_view.py  "<ruta>/view.json"
python C:/Users/willi/.claude/scripts/sync_view.py          "<carpeta_de_la_vista>"
```

### Sync (solo):
```bash
python C:/Users/willi/.claude/scripts/sync_view.py "<carpeta_de_la_vista>"
```

### Validación:
1. [ ] JSON válido: `python -c "import json; json.load(open('view.json'))"`
2. [ ] Acordeón funciona (TODAS las Sections expanden/colapsan)
3. [ ] Guardado funciona (registro en registerhistory con todos los grupos)
4. [ ] Insights en el JSON con prefijo turno/hora
5. [ ] Firma de operario funciona (si aplica)
6. [ ] Reporte PDF con datos correctos (si aplica)

---

# Vistas especiales

## Overview_Papos (PASO 12)
En el binding de la lista filtrada, transform:
```python
return papo_core.overview.getPapoListFiltered(value)
```

## Embedded_PAPO (PASO 13)
En el binding del path "De:", transform:
```python
return papo_core.overview.getCardPath(value)
```

## Reportes EA11-0901, etc. (PASO 14)
En el Data Source Script del reporte:
```python
papo_core.report.extractReportData(data)
```

---

## Errores conocidos y soluciones

| Error | Causa | Solución |
|---|---|---|
| `TypeError: getHour24(): 1st arg can't be coerced to java.util.Date` | `initialPapoDateTime` es string `""` | Usar timestamp object `{"$": ["ts", 192, 0], "$ts": 0}` |
| Designer no detecta cambios | version insuficiente o actor="admin" | Usar `sync_view.py` (MAX+2, actor="external") |
| Scripts inyectados en botón en vez de root | `standardize_view.py` v1.0.0 buscaba primera ocurrencia | Corregido en v1.1.0 (busca desde root.scripts) |
| onStartup no reemplazado | Script solo insertaba si faltaba, no reemplazaba legacy | Corregido en v1.1.0 |
| json.load/dump destruye escapes Gson | Python's json no preserva `=`, `'`, etc. | NUNCA usar json.dump para escribir view.json |

---

## RESUMEN DE WRAPPERS

|Ubicación|Wrapper|
|---|---|
|Section{N} → onClick (TODAS)|`toggleFlexRoot(sectionIndex)` inline|
|Section{N} → style.classes (TODAS)|Property binding a `../FlexContainerGroup{N}.position.display` + map|
|view → onStartup|`self.custom.initialPapoDateTime = system.date.now()` + `papo_core.ui.initForm(self)` (+ `supervisorOpt` si aplica)|
|view.custom.insights → transform|`papo_core.ui.preInsight(self, value)`|
|root.scripts → toggleFlexRoot|`papo_core.ui.toggleSection(self, sectionIndex)`|
|root.scripts → answerRecopile|`papo_core.register.recopile(flexContainer, self)`|
|root.scripts → saveDataRoot|`papo_core.register.save(self)`|
|root.scripts → signOperator|`papo_core.sign.signOperator(self)`|
|Botón Guardar → onClick|`papo_core.ui.confirmSave()` (mensaje fijo: "Esta seguro de que desea guardar el registro")|
|Overview filtrado → transform|`papo_core.overview.getPapoListFiltered(value)`|
|Embedded_PAPO path → transform|`papo_core.overview.getCardPath(value)`|
|Reporte → data source|`papo_core.report.extractReportData(data)`|
