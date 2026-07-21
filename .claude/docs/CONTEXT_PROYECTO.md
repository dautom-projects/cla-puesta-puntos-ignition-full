# PAPO — Contexto del Proyecto (para Claude Code)

## Qué es PAPO

PAPO es una aplicación de formularios y flujos de trabajo industriales para una
planta de manufactura (Clarios). Gestiona formularios de piso de planta, flujos
de firma de supervisores, registros de turno y reportes across varias áreas de
la planta (Ensamble, NFR/Carga y Terminado, Reciclado, OREC, F&A, Cubiertas,
Formación).

Los usuarios son operarios y supervisores de planta. Rellenan formularios
digitales ("puestas a punto") en estaciones de trabajo fijas, y los supervisores
los firman.

## Stack técnico

- **Plataforma:** Ignition Perspective 8.1.x (SCADA/HMI de Inductive Automation)
- **Lenguaje de scripting:** Jython 2.7 (Python 2 sobre la JVM)
- **Base de datos:** SQL Server (conexión `papo_db`)
- **User sources:** ClariosAD (Active Directory, primario) + papo_db_users (soft failover)

## Jerarquía de nodos

```
ENTERPRISE → SITE → AREA → LINE → CELL
```

## Roles

- `Operator` — operario de planta, rellena formularios
- `Supervisor_PAPO` — supervisor, firma formularios (valida IP de estación)
- `Administrator` — admin, firma sin validar IP
- `INTEGRADOR` — integrador, firma sin validar IP

## Turnos

Los turnos se representan como int (1, 2, 3):
- Turno 1 (T1): 22:00 – 06:00
- Turno 2 (T2): 06:00 – 14:00
- Turno 3 (T3): 14:00 – 22:00

## Tipos de registro (RegisterTypeID)

| ID | Significado |
|----|-------------|
| 1 | Cada hora |
| 2 | Cada 2 horas |
| 3 | Cada media hora |
| 4 | Cada 4 horas |
| 5 | Cambio de referencia |
| 6 | Mantenimiento |
| 7 | Inicio de turno |
| 8 | Fin de turno |
| 9 | Mitad de turno |
| 10 | Firma (operario "Finalizado" / supervisor "Revisado") |
| 11 | Diario |
| 12 | Idle / "Sin Iniciar" (inicio de nuevo ciclo) |
| 13 | Multi / check inicial |
| 14 | Control de rechazos |
| 15 | Hallazgos |
| 16 | Ingreso de baterías |
| 17 | Salida de baterías |
| 18 | Defectos |
| 19 | Paro |
| 20 | Barcada |

## Tablas principales

- `registerhistory` — todos los registros de formularios (respuestas, firmas, idle)
- `registertype` — catálogo de tipos de registro
- `papo` — catálogo de formularios (tiene `Reference`, `Description`)
- `papoitem` — preguntas de cada formulario
- `papoitem_registertype` — relación pregunta ↔ tipos de registro donde aparece
- `node` — jerarquía de nodos (tiene `DisplayName`, `Type`, `ParentNodeID`, `topic`)
- `nodepapo` — relación nodo ↔ papo
- `workstation` — estaciones de trabajo (tiene `IpAddress`, `Description`)
- `workstationnode` — relación estación ↔ nodo

## Estructura de DataAnswer (JSON)

Cada registro en `registerhistory.DataAnswer` es un JSON:

```json
{
  "items": [
    {"papoItemID": 133, "answer": "Cumple", "registerTypeID": 7},
    {"papoItemID": 134, "answer": "No Cumple", "registerTypeID": 7},
    {"insights": " | T: 3, H: 21:32 - comentario", "registerTypeID": 7,
     "user": "Nombre Apellido", "timestamp": "Sun Jul 05 21:35:41 COT 2026"}
  ]
}
```

- Cada item de respuesta tiene `papoItemID`, `answer`, `registerTypeID`
- El último item es metadata: `insights`, `registerTypeID`, `user`, `timestamp`

Las firmas (RegisterTypeID 10) tienen otro formato:
```json
{"role": ["Administrator"], "name": "Soporte", "user": "dautom", "lastname": ""}
```

## Flujo de guardado (ruta oficial)

1. Cada campo tiene `custom.item` = `{papoItemID, answer, registerTypeID}`
2. `answerRecopile` (custom method en root) recorre recursivamente y recolecta
3. `saveDataRoot` (message handler en root) junta TODOS los grupos en UN JSON y hace UN INSERT
4. Firma operario: inserta tipo 10 "Finalizado" + tipo 12 Idle "Sin Iniciar" con regCode+1
5. Firma supervisor: inserta tipo 10 "Revisado"

El `RegisterCode` identifica un ciclo de formulario. Se reutiliza durante el
ciclo y se incrementa (+1) cuando el operario firma, iniciando un nuevo ciclo.

IMPORTANTE: al leer el último RegisterCode SIEMPRE ordenar por `RegisterCode DESC`,
NO por `Timestamp` — cuando la firma y el idle comparten el mismo timestamp exacto,
ordenar por Timestamp elige mal y duplica el RegisterCode.

## Arquitectura papo_core (Project Library)

Toda la lógica pesada vive en el package `papo_core`. Cada vista tiene solo
wrappers de una línea que llaman a la librería.

```
project/
└── papo_core/
    ├── register.py    # recopile(flexContainer, root), save(root)
    ├── ui.py          # toggleSection(root, sectionIndex), initForm(root), preInsight(root, value)
    ├── sign.py        # supervisorOpt, signOperator(root), requestSupervisorAuth(button),
    │                  # signSupervisor(root), authenticateAndSign(popup)
    ├── report.py      # extractReportData(data)
    └── overview.py    # getPapoListFiltered(value), getCardPath(value)
```

**Convención de llamado:** `papo_core.modulo.funcion(self)` (sin prefijo `project.`)

**Convención de funciones:**
- Públicas (llamadas desde vistas): sin underscore — `recopile`, `save`, `toggleSection`
- Privadas (helpers internos): con underscore — `_gatherItems`, `_getLastRegisterCode`

## Vistas principales

- `Form_XXXX_start` / `Form_XXXX_end` — formularios de inicio/fin de turno
- `Digitalizacion_Template` — vista de preview con tabla de respuestas y firma supervisor
- `PopUp Authenticator` — popup para que el supervisor firme sin cerrar sesión del operario
- `Overview_Papos` — lista de tarjetas de formularios
- `Embedded_PAPO` — tarjeta individual embebida
- Reportes (EA11-0901, etc.) — generan el PDF del formulario

## Convenciones de código (SIEMPRE aplicar)

- **Indentación:** tabs
- **Variables:** camelCase
- **Funciones públicas:** sin underscore; **helpers privados:** con `_` prefijo
- **Docstrings:** con secciones Version / Changelog / Args / Returns
- **Comentarios:** en inglés, describen QUÉ hace el código
- **Comparaciones con None:** usar `is` / `is not`
- **Bloques try/except:** único por función pública
- **Loggers:** `logger.error` con nombre basado en la referencia del PAPO
  (para poder filtrar logs por formulario). Fallback al nombre del módulo.
- **dbConnection:** siempre de `view.custom` o `session.custom`, nunca hardcodear `"papo_db"`

## Cómo se despliega

- El desarrollo se hace en una máquina dev.
- Los cambios se despliegan compartiendo la vista completa.
- Los scripts de cache (tags UDT) y los scripts de reporte se despliegan aparte.
- Después de cada cambio, se registra qué vista/componente se modificó para
  mantener el inventario de despliegue a producción.

## En el horizonte (contexto futuro)

- Migración a tablets/móvil (reemplazar identificación por IP fija con NFC)
- Migración de contraseñas de texto plano a hashing en papo_db_users
  (NOTA: evitar BCrypt — no funciona en Manual Mode DB User Source de Ignition,
   y su import rompe los módulos del Project Library en scope de sesión Perspective)
- Limpieza de ClariosAD (nombres con dobles espacios, columna Badge para NFC)
