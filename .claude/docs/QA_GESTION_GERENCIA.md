# QA — Page/Gestion Gerencia (filtrado y consultas)

Fecha: 2026-10-22. Revisión estática del `view.json`, de la Project Library y de los logs de PAPOS.
Las consultas no se ejecutaron contra `papo_db` (sin acceso directo a SQL Server desde aquí).

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
| 10 | Frecuencia de consultas | ❌ Falla | `custom.refresh` y `endTime` cambian cada segundo, así que las 3 consultas corren cada segundo por sesión. Además `custom.dataTable` (no lo usa ninguna tabla) consulta `sql.getRegisterHistory` sin filtros cada segundo |
| 11 | Selección → reporte PDF | ✅ Pasa | `onRowClick` desempaqueta la fila y `custom.path` resuelve la referencia del master. Sin fila seleccionada, `custom.path` falla (`'NoneType' ... split`) y deja error en el log |
| 12 | Referencias rotas | ❌ Falla | `position.basis` de los dropdowns apunta a `../Dropdown Area` (no existe); 7 labels leen `view.custom.ips` / `ipStation` (no existen); `custom.dataTable` usa `nodeId`, `papoId`, `refreshTable` (no existen); el handler `signPapoSup` busca el componente `Table` (no existe) y nadie lo envía en esta vista; `custom.refresh` envía `filterTable` cada segundo sin receptor |

## Correcciones propuestas

1. Filtro de supervisor por **nombre completo normalizado** (minúsculas, espacios simples) en las tres tablas y en los contadores; el dropdown pasa a tener el nombre como valor.
2. Contadores calculados sobre las filas ya filtradas.
3. Quitar `custom.refresh` del struct de `dataReports` y usar un reloj de 1 minuto para `startTime`/`endTime`; borrar `custom.dataTable`.
4. Corregir el inicio de Día Actual / Día Anterior con la regla de turnos (T1 empieza a las 22:00 del día anterior), compartida con `Page/Gestion`.
5. Agregar `WorkstationNodeID` a la llave de ciclo en las consultas 1–3 (y en `sql.getRegisterHistory`).
6. Resolver la pregunta "Supervisor" con `COALESCE(MasterPapoID, ID)`.
7. Limpiar referencias rotas y proteger `custom.path` cuando no hay selección.
8. Supervisores del dropdown: sumar los asignados en formularios, no solo los que firmaron.
