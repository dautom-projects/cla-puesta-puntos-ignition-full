# CLA MES Ignition - Proyecto PAPO

## Qué es este proyecto

PAPO es una aplicación de formularios industriales en **Ignition Perspective 8.1.x**
para la planta de manufactura Clarios. Gestiona formularios de piso ("puestas a
punto"), firmas de operario/supervisor, registros de turno y reportes PDF across
las áreas de la planta (Ensamble, Metalurgia, OREC, F&A, General).

## Stack

- **Plataforma:** Ignition Perspective 8.1.x (SCADA/HMI)
- **Scripting:** Jython 2.7 (Python 2 sobre JVM) — NO usar sintaxis de Python 3
- **Base de datos:** SQL Server, conexión `papo_db`
- **User sources:** ClariosAD (AD, primario) + papo_db_users (failover)

## Rutas clave (relativas a esta carpeta projects/)

- Proyecto Ignition: `cla_mes/`
- Vistas Perspective: `cla_mes/com.inductiveautomation.perspective/views/<ruta>/view.json`
- Project Library: `cla_mes/ignition/script-python/papo_core/<modulo>/code.py`

## Jerarquía de nodos

ENTERPRISE → SITE → AREA → LINE → CELL

## Turnos (int 1/2/3)

- T1: 22:00–06:00
- T2: 06:00–14:00
- T3: 14:00–22:00

## Arquitectura papo_core (Project Library)

Toda la lógica pesada vive en el package `papo_core`. Cada vista tiene solo
wrappers de una línea. Se llama SIN prefijo `project.`:

```
papo_core.register.save(self)
papo_core.ui.toggleSection(self, sectionIndex)
papo_core.sign.signOperator(self)
```

Módulos:
- `register.py` — recopile, save
- `ui.py` — toggleSection, initForm, preInsight
- `sign.py` — supervisorOpt, signOperator, requestSupervisorAuth, signSupervisor, authenticateAndSign
- `report.py` — extractReportData
- `overview.py` — getPapoListFiltered, getCardPath

## Convenciones de código (SIEMPRE aplicar)

- Indentación: **tabs**
- Variables/funciones: **camelCase**
- Funciones públicas: sin underscore; helpers privados: con `_` prefijo
- Docstrings con Version / Changelog / Args / Returns
- Comentarios en inglés, describen QUÉ hace el código
- Comparaciones con None: usar `is` / `is not`
- Un solo try/except por función pública
- Loggers: `logger.error` con nombre = referencia del PAPO (para filtrar)
- **dbConnection** siempre de `view.custom` o `session.custom`, NUNCA hardcodear "papo_db"

## Reglas críticas al editar view.json

1. **SIEMPRE hacer backup antes** de tocar un view.json
2. **Leer una vista ya estandarizada** como plantilla de referencia antes de editar
3. El JSON de Perspective es **estricto** — respetar formato de events/scripts/bindings
4. Después de editar, hacer **re-scan del proyecto** en el gateway (o restart)
5. **Validar** que el JSON parsea: `python -c "import json; json.load(open('view.json'))"`
6. **Preservar** los `custom.item` de cada campo (contienen respuestas)
7. Scripts de papo_core se llaman SIN `project.`

## Flujo de guardado (ruta oficial)

1. Cada campo: `custom.item = {papoItemID, answer, registerTypeID}`
2. `answerRecopile` (custom method root) recolecta recursivamente
3. `saveDataRoot` (message handler root) junta TODO en UN JSON, UN INSERT
4. Firma operario: type 10 "Finalizado" + type 12 Idle "Sin Iniciar" con regCode+1
5. Firma supervisor: type 10 "Revisado"

RegisterCode identifica un ciclo. Al leer el último RegisterCode SIEMPRE ordenar
por `RegisterCode DESC` (NO por Timestamp — causa duplicados cuando firma e idle
comparten el mismo timestamp exacto). Bug ya corregido en papo_core.sign.

## Documentos de contexto

- `.claude/docs/CONTEXT_PROYECTO.md` — contexto general completo
- `.claude/docs/CONTEXT_AUTOMATIZACION_JSON.md` — cómo inyectar wrappers en view.json
- `.claude/docs/PROCEDIMIENTO_ESTANDARIZACION.md` — pasos de estandarización por vista
- `.claude/docs/USAGE.md` — referencia de wrappers de papo_core
- `.claude/docs/papo_core_reference/` — los 5 módulos papo_core como referencia

## Estado actual

- 63 formularios inventariados
- papo_core creado y en despliegue a producción
- Digitalizacion_Template: firmas migrándose a papo_core
- Pendiente: estandarizar los 63 forms con wrappers

<!--
CLAUDE.md se carga en el contexto al inicio de CADA sesion.
Manten este archivo por debajo de ~200 lineas. Lo que solo importe
para tareas concretas muevelo a .claude/rules/ (con paths:) o a un skill.
-->
