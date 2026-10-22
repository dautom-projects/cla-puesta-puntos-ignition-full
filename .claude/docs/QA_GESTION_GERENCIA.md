# QA — Page/Gestion Gerencia (filtrado y consultas)

Fecha: 2026-10-22. Revisión del `view.json`, de la Project Library y de los logs de PAPOS, validada contra la base de pruebas `cla-db-papo` (contenedor `mssql`, 2,898 registros del 2025-10-22 al 2026-10-22).

## Flujo de la vista

Filtros: **Supervisor**, **Periodo** (Turno 1/2/3, Día Anterior, Día Actual, Semana, Mes, Personalizado) e **Inicio/Fin**.
`custom.dataReports` corre 3 consultas (ciclos del periodo, firmas tipo 10 y supervisor del formulario) y arma la lista; las tres tablas (`TablaGeneral`, `TablaOperario`, `TablaSupervisor`) la filtran en su transform. Al hacer clic en una fila se llena `custom.selection`, que alimenta el ReportViewer.

## Resultado por pipeline

| # | Pipeline | Resultado | Detalle |
|:-:|---|:-:|---|
| 1 | Carga de supervisores (onStartup) | ⚠️ Pasa | Solo lista supervisores que ya firmaron algo (`Revisado`); uno asignado que nunca firmó no aparece |
| 2 | Supervisor → TablaGeneral | ❌ Falla | El dropdown tiene como valor el **usuario** (`username`) y la tabla compara contra `SupervisorEsperado`, que es el **nombre completo**. Al elegir un supervisor la tabla queda vacía |
| 3 | Supervisor → TablaOperario | ❌ Falla | No aplica el filtro de supervisor |
| 4 | Supervisor → TablaSupervisor | ❌ Falla | El filtro está escrito pero no hace nada (`pass`) |
| 5 | Contadores (total, sin firma operario, sin firma supervisor) | ❌ Falla | Se calculan sobre todos los registros; no respetan el filtro de supervisor |
| 6 | Periodo → rango de fechas | ⚠️ Parcial | Turnos, Semana, Mes y Personalizado pasan. **Día Actual** y **Día Anterior** fallan en el turno 1: entre 00:00 y 05:59 arrancan un día antes de lo debido, y desde las 22:00 no toman el nuevo día de producción |
| 7 | Consulta de ciclos (consulta 1) | ⚠️ Riesgo | Agrupa por `NodeID + PapoID + RegisterCode`. Si dos estaciones del mismo nodo llenan el mismo PAPO, sus ciclos con igual `RegisterCode` se mezclan (falta `WorkstationNodeID`) |
| 8 | Firmas (consulta 2) | ⚠️ Riesgo | Mismo riesgo que el 7. La detección de "Cierre Automatico" sí pasa (coincide con lo que escribe `autoCloseOpenForms`) |
| 9 | Supervisor esperado del formulario (consulta 3) | ❌ Falla | Busca la pregunta "Supervisor" con `papoitem.PapoID = PapoID`. Los PAPO clonados (`MasterPapoID`) no tienen `papoitem`: quedan en la firma o "Sin asignar" |
| 10 | Frecuencia de consultas | ⚠️ Riesgo | `custom.refresh` y `endTime` cambian cada segundo, así que las 3 consultas corren cada segundo por sesión. Además `custom.dataTable` (no lo usa ninguna tabla) consulta `sql.getRegisterHistory` sin filtros cada segundo |
| 11 | Selección → reporte PDF | ✅ Pasa | `onRowClick` desempaqueta la fila y `custom.path` resuelve la referencia del master. Sin fila seleccionada, `custom.path` falla (`'NoneType' ... split`) y deja error en el log |
| 12 | Referencias rotas | ❌ Falla | `position.basis` de los dropdowns apunta a `../Dropdown Area` (no existe); 7 labels leen `view.custom.ips` / `ipStation` (no existen); `custom.dataTable` usa `nodeId`, `papoId`, `refreshTable` (no existen); el handler `signPapoSup` busca el componente `Table` (no existe) y nadie lo envía en esta vista; `custom.refresh` envía `filterTable` cada segundo sin receptor |

## Validación con datos (cla-db-papo)

| Chequeo | Resultado |
|---|---|
| Tipos de nodo | 5 AREA, 23 LINE, 50 CELL. El 44 % de los registros (1,276 de 2,898) está en nodos CELL |
| Filtro en cascada de `Page/Gestion` (fix `feeaa50`) | Por Área antes 0 registros en las 5 áreas; ahora Ensamble 275, F&A 1,723, General 3, Metalurgia 94, OREC 803. Por Línea, Terminado 593 → 1,310 y Reactores 87 → 371 (registros de sus celdas) |
| Ciclos que mezclan estaciones (pipelines 7 y 8) | 13 nodos tienen 2+ estaciones; **56 ciclos** `NodeID + PapoID + RegisterCode` combinan 2–3 estaciones (p. ej. Terminado, PAPO 47, RegisterCode 0–3, 3 estaciones) |
| PAPOs clonados (pipeline 9) | 18 clones con 106 inicios de turno; sus 18 masters sí tienen la pregunta "Supervisor", así que `COALESCE(MasterPapoID, ID)` lo resuelve |
| Filtro de supervisor (pipelines 2–5) | El dropdown usa usuarios (`bhomej`, `bramirh1`…) y las tablas comparan con nombres (`Jorge Home`, `Herly Ramirez`…): nunca coinciden. Hay variantes del mismo nombre ("Herly  Ramirez " / "Herly Ramirez"), supervisores asignados en formularios que nunca firmaron (Fredy Arley Arboleda Mazo, Guillermo Andres Banderas Ayala, Oscar Viafara…) y 77 firmas con usuario `NA` ("NA NA") |
| Costo de las consultas (pipeline 10) | Semana actual: 2 ciclos, ~15 ms. Todo el historial: 411 ciclos, 603 firmas, ~26 ms. Correrlas cada segundo no se nota con estos datos, pero crece con el historial de producción |

## Correcciones propuestas

1. Filtro de supervisor por **nombre completo normalizado** (minúsculas, espacios simples) en las tres tablas y en los contadores; el dropdown pasa a tener el nombre como valor.
2. Contadores calculados sobre las filas ya filtradas.
3. Quitar `custom.refresh` del struct de `dataReports` y usar un reloj de 1 minuto para `startTime`/`endTime`; borrar `custom.dataTable`.
4. Corregir el inicio de Día Actual / Día Anterior con la regla de turnos (T1 empieza a las 22:00 del día anterior), compartida con `Page/Gestion`.
5. Agregar `WorkstationNodeID` a la llave de ciclo en las consultas 1–3 (y en `sql.getRegisterHistory`).
6. Resolver la pregunta "Supervisor" con `COALESCE(MasterPapoID, ID)`.
7. Limpiar referencias rotas y proteger `custom.path` cuando no hay selección.
8. Supervisores del dropdown: sumar los asignados en formularios, no solo los que firmaron, y excluir el usuario `NA`.

## Estado tras la corrección (2026-10-22)

Corregidos en `Page/Gestion Gerencia` y validados ejecutando el código real de los transforms contra `cla-db-papo`:

- Pipelines 2–5: en las 25 opciones de supervisor (todo el historial), en la del mes y en la de la semana, cada opción trae registros y TablaGeneral / TablaOperario / TablaSupervisor coinciden con total / sin firma operario / sin firma supervisor
- Pipeline 1: el dropdown pasa de 7 nombres (con "NA NA") a los supervisores con reportes en el periodo (25 en todo el historial)
- Pipelines 7–8: 411 → 467 ciclos (los 56 que mezclaban estaciones quedan separados)
- Pipeline 9: "Sin asignar" 207 → 162 (PAPOs clonados resueltos por su master; gana la última respuesta del ciclo)
- Pipeline 6: Día Actual / Día Anterior correctos a las 03:30, 10:30 y 23:30 (antes fallaban 4 de 6 casos)
- Pipeline 10: sin `custom.refresh`; el fin del rango cambia una vez por minuto
- Pipelines 11–12: sin referencias rotas; `custom.path` ya no registra error sin selección

Pendiente fuera de esta vista: `Page/Gestion` tiene el mismo error de Día Actual / Día Anterior, y `sql.getRegisterHistory` agrupa ciclos sin `WorkstationNodeID`. El reporte PDF recibe `nodeID`, `papoID` y `registerCode` (sin estación), así que con dos estaciones en el mismo ciclo puede mezclar datos. Hay datos con problemas de codificación ("Carlos MuÃ...oz Tenorio").
