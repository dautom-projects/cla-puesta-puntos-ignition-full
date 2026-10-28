# Verificación de F&A y OREC (2026-10-28)

Pedido del usuario: asegurar que los formularios de F&A y OREC funcionan. Cada PAPO se corrió en el navegador a 1920x1080 con un usuario con sesión iniciada, desde su estación en `Digitalizacion_Template`, con el ciclo completo de un operario: cada botón de registro (Inicio, 30 min, SKU, Mmto, 1 hr, 4 hr, Barcada, Paro, Hallazgo, Nueva Ref., Fin…), todos los campos llenos, Firma Supervisor y Firma Operario. Después:

1. **Registros:** cada registro guardado del ciclo trae exactamente los ítems que recolecta su vista (`papo_core.register.save`), en el mismo orden y sin `papoItemID` nulo; el ciclo cierra (tipo 12) con las dos firmas.
2. **PDF:** el PDF del ciclo, abierto desde Gestión, se compara casilla por casilla con lo guardado: cada `@grupo.papoItemIDn@` muestra la respuesta y cada marca (Cumple / No cumple, Bueno / Malo, Si / No) aparece solo cuando la respuesta es esa.

Herramientas en el scratchpad de la sesión (`verify/`: `run.js`, `check.py`, `plan.json`); no están en el repo.

## Resultado

44 PAPOs con el ciclo completo: **0 diferencias** en los registros y **0 diferencias** en los PDF.

| Área | PAPOs | Registros | PDF |
|---|---|---|---|
| F&A | AC10-0201, AC10-0202-HD, AC10-0202-SLI, AC10-0301, AC10-0501, AC10-0801, AC10-1003, AC10-1101, AC10-1801, CA02-2102, CG10-0101, FO10-0100, FO10-0601, FO10-1701, FO10-1701-1, GR10-0501 (16) | iguales a la vista | sin diferencias |
| OREC | CI11-0101, CU11-0101, EC07-0101, EC11-0101, EJ07-0101, EJ11-0101, EJ11-0102, MZ07-0101, MZ11-0101, PO07-0101, PO11-0101-1…4, RJ11-0101-1…12, SO02-4502, RJ07-0101 (28) | iguales a la vista | sin diferencias |

AC10-0202-SLI, FO10-0100 y GR10-0501 se corrieron antes de sus correcciones del mismo día (checkbox de llenado, tabla de ingresos y total, rotación con fecha e inventario final); esos cambios se probaron aparte en el navegador (ver sus informes en esta carpeta).

## Pendiente

- F&A: PT11-0104, TE11-0601 y TE11-2601 sin correr; AC10-1801 conviene repetirlo (su 30 min quedó con 22 campos vacíos por una prueba en dos pestañas a la vez)

## Hallazgos

- **Ítems que se guardan y el PDF no imprime:** la plantilla original no tiene la casilla (supervisores, EPP de AC10-1003, densidad y penetración de MZ07-0101, textos de hallazgo de SO02-4502…). Lista completa en `items-ajenos.md` ("Casillas que el PDF no tiene"). Decidir con el área si alguno debe salir
- **Hora de la firma del supervisor:** el "Revisado" se inserta con `CURRENT_TIMESTAMP` del servidor SQL; en develop el servidor está en UTC y queda 5 h adelante del resto del ciclo (EJ07-0101: Fin 15:06, Revisado 20:06). Anotado en el BACKLOG
- Ya conocidos (BACKLOG): CI11-0101 guarda 4844–4851 dos veces; PO11-0101-N guarda 5168 dos veces y 5169, que no existe en `papoitem`
