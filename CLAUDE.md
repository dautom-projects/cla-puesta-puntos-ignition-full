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

## Base de datos papo_db

Esquema completo en `.claude/docs/DATABASE_SCHEMA.dbml`.

- Tablas de PAPO: `node`, `nodepapo`, `papo`, `papoitem`, `papoitem_registertype`, `registerhistory`, `registertype`, `workstation`, `workstationnode`
- `users`, `roles`, `user_roles`: user source `papo_db_users`
- `scada_*`: tablas internas del user source de Ignition (vacías)
- `fa_cpk_*`: proyecto CPK/SPC de F&A, no pertenecen a PAPO
- No hay FKs físicas: todas las relaciones son lógicas

## Rutas clave (relativas a esta carpeta projects/)

- Proyecto Ignition: `cla-project/`
- Vistas Perspective: `cla-project/com.inductiveautomation.perspective/views/<ruta>/view.json`
- Project Library: `cla-project/ignition/script-python/papo_core/<modulo>/code.py`

## Jerarquía de nodos

ENTERPRISE → SITE → AREA → LINE → CELL

## Turnos (int 1/2/3)

- T1: 22:00–06:00
- T2: 06:00–14:00
- T3: 14:00–22:00

## Roles

- `Operator` — operario, rellena formularios
- `Supervisor_PAPO` — supervisor, firma formularios (valida IP de la estación)
- `Administrator`, `INTEGRADOR` — firman sin validar IP

## Vistas principales

- `Form_XXXX_<tipo>` — formularios embebidos (start, end, 1h, 30min, SKU, ...)
- `Page/Digitalizacion_Template` — preview con tabla de respuestas y firmas
- `Page/PopUps/Authenticator` — popup para que el supervisor firme sin cerrar la sesión del operario
- `Page/Overview_Papos` — lista de tarjetas de formularios; `Page/Embedded/Embedded_PAPO` — tarjeta individual
- Reportes (EA11-0901, etc.) — generan el PDF del formulario

## Despliegue

- Se desarrolla en una máquina dev y se despliega compartiendo la vista completa
- Scripts de cache (tags UDT) y de reporte se despliegan aparte
- Cada cambio se registra en `.claude/docs/DEPLOY_INVENTORY.md`
- Sync con el gateway local (PAPOS, Ignition 8.1.19): manual, con Project → Update Project en el Designer. El timer `claude-code-sync` no puede re-escanear en 8.1.19 (`system.project.requestScan` no existe)

## Arquitectura papo_core (Project Library)

Toda la lógica pesada vive en el package `papo_core`. Cada vista tiene solo
wrappers de una línea. Se llama SIN prefijo `project.`:

```
papo_core.register.save(self)
papo_core.ui.toggleSection(self, sectionIndex)
papo_core.sign.signOperator(self)
```

Módulos (`papo_core/<modulo>/code.py`, funciones públicas):
- `register` — recopile, save
- `ui` — toggleSection, initForm, preInsight, confirmSave, getSecurityImage
- `sign` — supervisorOpt, signOperator, requestSupervisorAuth, signSupervisor, signSupervisorFromSelection, authenticateAndSign, autoCloseOpenForms
- `report` — extractReportData, extractReportDataAuto
- `overview` — getPapoListFiltered, getCardPath
- `items` — getRangeColor

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
- Turnos: nunca system.date.getHour24(); usar java.util.Calendar con TimeZone America/Bogota
- Deploy: siempre desplegar el módulo del Project Library antes que la vista que lo llama

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
3. `saveDataRoot` (message handler root) junta TODO en UN JSON, UN INSERT con Status "En proceso"
4. Firma operario: type 10 "Finalizado" + type 12 Idle "Sin Iniciar" con regCode+1
5. Firma supervisor: type 10 "Revisado"

RegisterCode identifica un ciclo. Al leer el último RegisterCode SIEMPRE ordenar
por `RegisterCode DESC` (NO por Timestamp — causa duplicados cuando firma e idle
comparten el mismo timestamp exacto). Bug ya corregido en papo_core.sign.

## Documentos de contexto

- `cla-project/ignition/script-python/papo_core/` — código fuente del package papo_core (referencia de los módulos)
- `.claude/docs/USAGE.md` — referencia de funciones de papo_core y desde dónde se llaman
- `.claude/docs/MIGRATION_STATUS.md` — estado de migración de las vistas Form_* por módulo
- `.claude/docs/PROCEDIMIENTO_ESTANDARIZACION.md` — pasos de estandarización por vista
- `.claude/docs/CONTEXT_AUTOMATIZACION_JSON.md` — cómo inyectar wrappers en view.json
- `.claude/docs/DATABASE_SCHEMA.dbml` — esquema de papo_db generado desde la base viva (notas de dominio, conteos y catálogos)
- `.claude/docs/DEPLOY_INVENTORY.md` — registro de cambios aplicados para desplegar
- `.claude/docs/BACKLOG.md` — pendientes y horizonte del proyecto

## Estado actual

- 63 formularios inventariados → 238 vistas Form_* (variantes start/1h/2h/end/...)
- papo_core creado y en despliegue a producción
- Migración Form_* (ver `.claude/docs/MIGRATION_STATUS.md`, corrida 2026-10-22):
  - 235 completas (ui + register), 3 parciales, 0 sin migrar
  - Parciales: Cubiertas `Form_PL11-0101-CA_start`, `-CU_start`, `-S&A_start` (solo confirmSave)
  - 94 usan además `sign.supervisorOpt` en onStartup
- Digitalizacion_Template: firmas aún inline (0 llamadas a papo_core); signOperator, requestSupervisorAuth, signSupervisor y authenticateAndSign sin uso todavía

<!--
CLAUDE.md se carga en el contexto al inicio de CADA sesion.
Manten este archivo por debajo de ~200 lineas. Lo que solo importe
para tareas concretas muevelo a .claude/rules/ (con paths:) o a un skill.
-->
