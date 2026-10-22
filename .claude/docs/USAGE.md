# papo_core — referencia de uso

Generado leyendo `cla-project/ignition/script-python/papo_core/*/code.py` y las vistas (2026-10-22).
Vistas que llaman a cada módulo: `.claude/ignition-graph/impact.json` (`used_by`). Función, componente y ubicación: escaneo del texto de cada `view.json` buscando `papo_core.<modulo>.<funcion>`.

Ruta del package: `cla-project/ignition/script-python/papo_core/`. Se llama sin prefijo `project.`.

## papo_core.items

impact.json: 2 vista(s) lo usan.

### `items.getRangeColor(value, minValue, maxValue, colorType="border")`

Devuelve el color hex (borde o texto) según si el valor está dentro del rango [minValue, maxValue]; neutro si está en rango o vacío.

**Llamado desde:** 2 vista(s).

| Componente | Ubicación | Veces |
|---|---|---|
| `NumericEntryField` | `propConfig:props.style.borderColor` | 17 |
| `NumericEntryField` | `propConfig:props.style.color` | 17 |
| `NumericEntryField_3` | `propConfig:props.style.borderColor` | 2 |
| `NumericEntryField_3` | `propConfig:props.style.color` | 2 |
| `NumericEntryField_1` | `propConfig:props.style.borderColor` | 2 |
| `NumericEntryField_1` | `propConfig:props.style.color` | 2 |
| `NumericEntryField_2` | `propConfig:props.style.borderColor` | 1 |
| `NumericEntryField_2` | `propConfig:props.style.color` | 1 |
| `NumericEntryField_4` | `propConfig:props.style.borderColor` | 1 |
| `NumericEntryField_4` | `propConfig:props.style.color` | 1 |
| `NumericEntryField_5` | `propConfig:props.style.borderColor` | 1 |
| `NumericEntryField_5` | `propConfig:props.style.color` | 1 |

- `Page/Embedded/Ensamble/Form_EA11-2501_2h`
- `Page/Embedded/Ensamble/Form_EA11-2601_1h`

## papo_core.overview

impact.json: 1 vista(s) lo usan.

### `overview.getPapoListFiltered(value)`

Filtra la lista cacheada de PAPOs por jerarquía completa (empresa/sitio/área/línea/estación/referencia) y rol.

**Llamado desde:** 1 vista(s).

| Componente | Ubicación | Veces |
|---|---|---|
| nivel view (raíz del view.json) | `propConfig:custom.formats` | 1 |

- `Page/Overview_Papos`

### `overview.getCardPath(value)`

Construye el texto de origen de la tarjeta "De: topic/workstation" consultando la BD.

**Llamado desde:** ninguna vista.

> No tiene llamadas en vistas ni en otros scripts del proyecto.

## papo_core.register

impact.json: 235 vista(s) lo usan.

### `register.recopile(flexContainer, root)`

Recorre recursivamente un FlexContainer y recolecta los custom.item {papoItemID, registerTypeID, answer}.

**Llamado desde:** 235 vista(s).

| Componente | Ubicación | Veces |
|---|---|---|
| `root` (componente) | `customMethod:answerRecopile` | 235 |

Vistas: 235 Form_* (detalle por vista en `MIGRATION_STATUS.md`).

### `register.save(root)`

Recolecta las respuestas de todos los FlexContainerGroup y guarda un único registro en registerhistory (formularios start y end).

**Llamado desde:** 235 vista(s).

| Componente | Ubicación | Veces |
|---|---|---|
| `root` (componente) | `messageHandler:saveDataRoot` | 235 |

Vistas: 235 Form_* (detalle por vista en `MIGRATION_STATUS.md`).

## papo_core.report

impact.json: 0 vista(s) lo usan.

### `report.extractReportData(data, sections, signaturePrefix=('firmaAdministrator', 'firmaOperator'))`

Extrae y aplana datos de registerhistory al dict del reporte según una lista de secciones configuradas (tipos, nombre, max, normalize).

**Llamado desde:** ninguna vista.

> No se encontraron llamadas en vistas ni scripts. Los 67 reportes son binarios y el grafo no los analiza: probablemente se llama desde ahí (sin verificar).

### `report.extractReportDataAuto(data)`

Variante autoconfigurada: descubre los RegisterTypeID en papoitem_registertype y arma las secciones desde registertype.Description.

**Llamado desde:** ninguna vista.

> Igual que extractReportData: sin llamadas en archivos de texto; los reportes no se analizan.

## papo_core.sign

impact.json: 96 vista(s) lo usan.

### `sign.supervisorOpt(root)`

Devuelve la lista ordenada de nombres completos de usuarios con rol Supervisor_PAPO para poblar el dropdown.

**Llamado desde:** 94 vista(s).

| Componente | Ubicación | Veces |
|---|---|---|
| nivel view (raíz del view.json) | `events.system.onStartup` | 94 |

Vistas: 94 Form_* (detalle por vista en `MIGRATION_STATUS.md`).

### `sign.signOperator(root)`

Firma de operario: inserta type 10 "Finalizado" + Idle type 12 "Sin Iniciar" con RegisterCode + 1.

**Llamado desde:** ninguna vista.

> Sin llamadas: Digitalizacion_Template sigue con la lógica de firma inline en su handler signOperator.

### `sign.requestSupervisorAuth(button)`

Entrada del botón Firma Supervisor: valida estado e IP y pide confirmación (mensaje signSuper) o abre el popup Page/PopUps/Authenticator.

**Llamado desde:** ninguna vista.

> Sin llamadas en vistas todavía (firmas en migración en Digitalizacion_Template).

### `sign.signSupervisor(root)`

Firma de supervisor directa con el usuario logueado (type 10 "Revisado").

**Llamado desde:** ninguna vista.

> Sin llamadas en vistas ni dentro del módulo (el handler signSuper no la invoca aún).

### `sign.signSupervisorFromSelection(root)`

Firma de supervisor sobre la fila seleccionada en una tabla de gestión (root.view.custom.selection).

**Llamado desde:** 2 vista(s).

| Componente | Ubicación | Veces |
|---|---|---|
| `root` (componente) | `messageHandler:signPapoSup` | 2 |

- `Page/Gestion`
- `Page/Gestion Gerencia`

### `sign.authenticateAndSign(popup)`

Autentica al supervisor desde el popup (credenciales, rol e IP) y ejecuta la firma.

**Llamado desde:** ninguna vista.

> Sin llamadas: Page/PopUps/Authenticator no referencia papo_core.

### `sign.autoCloseOpenForms(dbConnection)`

Cierra automáticamente los formularios que quedaron "En proceso" tras el cambio de turno (Finalizado + Sin Iniciar); pensado para un Gateway Timer/Scheduled Script.

**Llamado desde:** ninguna vista.

> Llamada desde el **Scheduled Script de gateway** del proyecto (`ignition/event-scripts/data.bin`, binario; el grafo no lo analiza), cron `10 6,14,22 * * *` (06:10, 14:10, 22:10): `papo_core.sign.autoCloseOpenForms("papo_db")`. Observación: la conexión está hardcodeada en ese script.

## papo_core.ui

impact.json: 238 vista(s) lo usan.

### `ui.toggleSection(root, sectionIndex)`

Acordeón: expande el FlexContainerGroup de la sección clicada y colapsa los demás.

**Llamado desde:** 235 vista(s).

| Componente | Ubicación | Veces |
|---|---|---|
| `root` (componente) | `customMethod:toggleFlexRoot` | 235 |

Vistas: 235 Form_* (detalle por vista en `MIGRATION_STATUS.md`).

### `ui.initForm(root)`

Inicializa el formulario al arrancar (initialPapoDateTime para mostrar turno/hora).

**Llamado desde:** 235 vista(s).

| Componente | Ubicación | Veces |
|---|---|---|
| nivel view (raíz del view.json) | `events.system.onStartup` | 235 |

Vistas: 235 Form_* (detalle por vista en `MIGRATION_STATUS.md`).

### `ui.preInsight(root, value)`

Antepone turno y hora al comentario: " | T: {shift}, H: {HH:MM} - {value}".

**Llamado desde:** 235 vista(s).

| Componente | Ubicación | Veces |
|---|---|---|
| nivel view (raíz del view.json) | `propConfig:custom.insights` | 235 |

Vistas: 235 Form_* (detalle por vista en `MIGRATION_STATUS.md`).

### `ui.confirmSave()`

Muestra el diálogo estándar de confirmación de guardado; al confirmar envía el mensaje saveDataRoot.

**Llamado desde:** 237 vista(s).

| Componente | Ubicación | Veces |
|---|---|---|
| `Button_Apply_0` | `events.dom.onClick` | 133 |
| `Button_Apply` | `events.dom.onClick` | 104 |

Vistas: 237 Form_* (detalle por vista en `MIGRATION_STATUS.md`).

### `ui.getSecurityImage(papoItemID,dbConnection)`

Devuelve la ruta /system/images/EPP/... de la imagen de EPP según la descripción del papoItem.

**Llamado desde:** 2 vista(s).

| Componente | Ubicación | Veces |
|---|---|---|
| `Image` | `propConfig:props.source` | 5 |
| `Image_0` | `propConfig:props.source` | 1 |

- `Page/Embedded/F&A/Form_AC10-0201_start`
- `Page/Embedded/F&A/Form_FO10-1701_start`

> Observación: no tiene try/except y si el papoItem no existe `url` queda sin definir (NameError).

