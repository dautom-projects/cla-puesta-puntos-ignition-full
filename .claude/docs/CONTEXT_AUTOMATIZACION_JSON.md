# PAPO — Automatización de Wrappers en JSON (para Claude Code)

## Objetivo de la tarea

Automatizar la aplicación del procedimiento de estandarización editando
directamente los archivos JSON de las vistas de Ignition Perspective, para
inyectar los wrappers de `papo_core` sin hacerlo manualmente en el Designer.

Esto es lo que Perspective NO permite hacer en runtime (no se pueden inyectar
scripts a componentes en ejecución), pero SÍ se puede hacer editando el
filesystem del proyecto.

## Estructura del filesystem de un proyecto Ignition

En este repo, el proyecto vive en:
```
gateway-data-active/projects/cla_mes/
```

Las vistas Perspective están en:
```
cla_mes/com.inductiveautomation.perspective/views/<ruta_de_la_vista>/view.json
```

Cada vista es una carpeta que contiene:
- `view.json` — la definición completa de la vista (componentes, props, scripts, bindings)
- `thumbnail.png` — miniatura (ignorar)

El Project Library (scripts de `papo_core`) está en:
```
cla_mes/ignition/script-python/papo_core/<modulo>/code.py
```
Cada módulo es una carpeta con `code.py` y `resource.json`.

## Anatomía de un view.json

Estructura relevante (simplificada):

```json
{
  "custom": { },
  "params": { },
  "props": { },
  "root": {
    "children": [
      {
        "meta": {"name": "Section1"},
        "events": {
          "dom": {
            "onClick": {
              "config": {
                "script": "sectionIndex = int(...)\n..."
              },
              "scope": "G",
              "type": "script"
            }
          }
        }
      }
    ],
    "meta": {"name": "root"}
  },
  "scripts": {
    "customMethods": [
      {
        "name": "toggleFlexRoot",
        "params": ["sectionIndex"],
        "script": "papo_core.ui.toggleSection(self, sectionIndex)"
      }
    ],
    "messageHandlers": [
      {
        "messageType": "saveDataRoot",
        "scopes": {"page": true, "session": true, "view": true},
        "script": "papo_core.register.save(self)"
      }
    ]
  }
}
```

## Puntos de inyección por vista

### Form_XXXX_start / Form_XXXX_end

**En `root.scripts.customMethods`** (array), agregar/reemplazar:
- `toggleFlexRoot` (params: `["sectionIndex"]`) → `papo_core.ui.toggleSection(self, sectionIndex)`
- `answerRecopile` (params: `["flexContainer"]`) → `return papo_core.register.recopile(flexContainer, self)`

**En `root.scripts.messageHandlers`** (array), agregar/reemplazar:
- `saveDataRoot` → `papo_core.register.save(self)`

**En la vista → `events.onStartup`** (a nivel de view, no root):
- `papo_core.ui.initForm(self)`

**En `custom.insights`** → agregar transform tipo script:
- `return papo_core.ui.preInsight(self, value)`

**En cada componente `Section{N}`** → `events.dom.onClick.config.script`:
```python
sectionIndex = int(self.meta.name.replace("Section", ""))
self.view.getChild("root").toggleFlexRoot(sectionIndex)
```

**En cada `Section{N}.props.style.classes`** → binding property a
`../FlexContainerGroup{N}.position.display` con transform map:
- true → "button-questions", false → "button-questions-2", fallback → "button-questions"

**En el botón Guardar** → `events.dom.onClick.config.script`:
```python
alerts.showAlert(state="warning", title="Guardar registro",
    message="Esta seguro de que desea guardar?",
    btnTextPrimary="Si", btnTextSecondary="No", btnActionPrimary="saveDataRoot")
```

## Limpieza requerida en view.custom

Eliminar estas claves de `custom` si existen (legacy):
- `answers`, `formato`, `test`, `flexGroupCount`, `flexCount`, `refreshSecond`
- `dsTable_v3`, `dsTable_vJ`, `changedRegister`, `viewOn` (solo en Digitalizacion_Template)

Eliminar de cada `FlexContainerGroup{N}.custom`:
- `answers` (binding/script reactivo legacy)

Verificar/crear en `custom`:
- `dbConnection`, `initialPapoDateTime`, `registerTypeID`, `insights`, `user`, `sign`, `referencePapo`

## Reglas de nombrado a normalizar

- Títulos de sección → `Section1`, `Section2`, ... (buscar labels/botones que
  actúen como títulos y renombrar por índice)
- Grupos de preguntas → `FlexContainerGroup1`, `FlexContainerGroup2`, ...
- Contenedor supervisor → `FlexContainerSupervisor`

El emparejamiento es por número: `Section{N}` ↔ `FlexContainerGroup{N}`.

## Precauciones críticas

1. **Hacer backup del proyecto antes de tocar cualquier JSON.** Un error de
   estructura rompe la vista y no carga en el Designer.

2. **El JSON de Perspective es estricto.** Respetar el formato exacto de
   `events`, `scripts`, `bindings`. Un campo mal ubicado invalida la vista.

3. **Después de editar, el gateway necesita re-scan o reinicio del proyecto**
   para detectar los cambios (o reimport desde el Designer).

4. **No inventar la estructura.** Antes de editar, LEER un `view.json` de una
   vista YA estandarizada manualmente y usarla como plantilla de referencia
   exacta para el formato de cada tipo de script/binding.

5. **Preservar** los `custom.item` de cada campo — contienen las respuestas
   mapeadas a papoItemID. NO tocarlos.

6. **Los scripts de `papo_core` se llaman SIN prefijo `project.`** —
   `papo_core.ui.initForm(self)`, no `project.papo_core.ui.initForm(self)`.

## Flujo de trabajo sugerido

1. Leer una vista ya estandarizada (ej: Form_EA11-0901_start) como referencia
2. Extraer los templates exactos de cada script/binding de esa referencia
3. Para cada vista a estandarizar:
   a. Backup
   b. Renombrar Sections y FlexContainerGroups por índice
   c. Inyectar los custom methods, message handlers, onStartup en `root.scripts`
   d. Inyectar los onClick en Sections y botones
   e. Inyectar los bindings de style.classes
   f. Agregar el transform en custom.insights
   g. Limpiar las claves legacy de custom
   h. Validar que el JSON sigue siendo parseable
4. Re-scan del proyecto en el gateway
5. Verificar cada vista en el Designer antes de desplegar

## Verificación post-edición

Por cada vista editada, confirmar:
- [ ] El JSON parsea sin errores
- [ ] La vista carga en el Designer sin overlay de error
- [ ] Los custom methods aparecen con sus params correctos
- [ ] Los message handlers tienen los scopes correctos
- [ ] El acordeón funciona (Sections expanden/colapsan)
- [ ] El guardado produce UN registro con todos los grupos
- [ ] Las firmas funcionan (operario y supervisor)
