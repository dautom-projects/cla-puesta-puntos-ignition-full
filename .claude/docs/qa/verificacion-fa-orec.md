# Verificación de F&A y OREC (2026-10-28)

Pedido del usuario: asegurar que los formularios de F&A y OREC funcionan. Cada PAPO se corrió en el navegador a 1920x1080 con un usuario con sesión iniciada, desde su estación en `Digitalizacion_Template`, con el ciclo completo de un operario: cada botón de registro (Inicio, 30 min, SKU, Mmto, 1 hr, 4 hr, Barcada, Paro, Hallazgo, Nueva Ref., Fin…), todos los campos llenos, Firma Supervisor y Firma Operario. Después:

1. **Registros:** cada registro guardado del ciclo trae exactamente los ítems que recolecta su vista (`papo_core.register.save`), en el mismo orden y sin `papoItemID` nulo; el ciclo cierra (tipo 12) con las dos firmas.
2. **PDF:** el PDF del ciclo, abierto desde Gestión, se compara casilla por casilla con lo guardado: cada `@grupo.papoItemIDn@` muestra la respuesta y cada marca (Cumple / No cumple, Bueno / Malo, Si / No) aparece solo cuando la respuesta es esa.

Herramientas en el scratchpad de la sesión (`verify/`: `run.js`, `check.py`, `plan.json`); no están en el repo.

## Resultado

47 PAPOs (los 19 de F&A y los 28 de OREC) con el ciclo completo: **0 diferencias** en los registros y **0 diferencias** en los PDF.

| Área | PAPOs | Registros | PDF |
|---|---|---|---|
| F&A | AC10-0201, AC10-0202-HD, AC10-0202-SLI, AC10-0301, AC10-0501, AC10-0801, AC10-1003, AC10-1101, AC10-1801, CA02-2102, CG10-0101, FO10-0100, FO10-0601, FO10-1701, FO10-1701-1, GR10-0501, PT11-0104, TE11-0601, TE11-2601 (19) | iguales a la vista | sin diferencias |
| OREC | CI11-0101, CU11-0101, EC07-0101, EC11-0101, EJ07-0101, EJ11-0101, EJ11-0102, MZ07-0101, MZ11-0101, PO07-0101, PO11-0101-1…4, RJ11-0101-1…12, SO02-4502, RJ07-0101 (28) | iguales a la vista | sin diferencias |

AC10-0202-SLI, FO10-0100 y GR10-0501 se corrieron antes de sus correcciones del mismo día (checkbox de llenado, tabla de ingresos y total, rotación con fecha e inventario final); esos cambios se probaron aparte en el navegador (ver sus informes en esta carpeta).

## Operario y supervisor en el PDF

Revisadas también las casillas de quien guardó y firmó (2026-10-28, a pedido del usuario):

- **Quien guardó cada registro** (`register1.user`, `shift1.user`, `endShift1.user`…): sale el nombre ("Soporte D.") en los 47; las que quedan vacías son de registros que el ciclo no tuvo (p. ej. `register2`…`register9` de FO10-1701-1)
- **Supervisor** (`firmaAdministratorN`): sale el nombre en todos
- **Operario** (`firmaOperator`): vacía en AC10-0301, AC10-0501, AC10-1003, CA02-2102, FO10-0601, TE11-2601 y EC07-0101 (FO10-0100 imprime `<N/A>`). No es el reporte: el reporte pone cada firma según el rol guardado con ella (`Operator` → operario, `Supervisor_PAPO` → supervisor) y el usuario de prueba de develop (admin, "Soporte D.") tiene Administrator y Supervisor_PAPO, no Operator, así que su firma de operario cae en la casilla del supervisor
- Comprobado con ciclos firmados por operarios reales de la base de prueba, abiertos desde Gestión: AC10-0501 del 25/06 (parredhe, modo `roleLast`) imprime "Hernan Arredondo" y CA02-2102 del 25/06 (bsalinm2, modo `role`) imprime "Mauricio Salinas", el nombre y apellido guardados en su firma. Los 7 reportes usan uno de esos dos modos; CG10-0101 (modo `status`) ya la llena en develop

## Las otras áreas con el comparador nuevo (2026-10-28)

Los PDF de la prueba general (Ensamble, Metalurgia, General / POLY / Cubiertas, capturados el 2026-10-28 00:10–00:20 para comparar los reportes con `build()`) se volvieron a revisar con las marcas y las casillas de usuario y firma, que el comparador de esa prueba no miraba:

- **Marcas:** 0 diferencias en las 456 revisadas (EA11-1101, FU11-0101, PA11-0301, RE10-0102, RE11-0101, TR11-0101). PA11-0301 imprime ✘ en las Cumple de su copia `startShiftmodes`: es el modo "mark" (equis en Cumple, blanco en No Cumple), como está definido
- **Quien guardó y supervisor:** con nombre en todos; la firma del operario vacía por el mismo motivo del rol en develop
- **Valores:** EA11-1101 y EA11-1601 tuvieron registros nuevos en su ciclo después de capturar el PDF (no se comparan); RE11-0101 4404 es el ítem guardado dos veces que ya está en el BACKLOG
- **EA11-0901:** guardaba el supervisor con `papoItemID` nulo; corregido (10938, `EA11-0901-supervisor.md`)

## Cierre automático en el gateway (2026-10-28)

La corrida de las 14:10 fue con `papo_core.sign` v1.3.0 y cerró los 8 ciclos que estaban abiertos y habían empezado antes de las 14:00 (los 7 en "Revisado" de junio y julio, y FO10-0100 de la estación 13), con el turno del ciclo en el comentario y la firma a nombre del operario del último formulario. Dejó abierto FO10-0100 de la estación 44 (ciclo sin formularios). A esa hora no había ciclos abiertos de Granja ni de Metalurgia: las exclusiones quedan probadas solo con los tests. A las 22:10 no corrió (la prueba gratuita del gateway estaba vencida).

## AC10-1801, registro de 30 min

En las dos corridas (2026-10-28 09:57 y 16:46) el registro de 30 min se guardó sin llenar: textos vacíos y checkbox en "No Cumple" (solo la Referencia elegida); los de SKU y Mantenimiento, con los mismos 49 ítems, salieron llenos. No es el formulario: llenado a mano a 1920x1080 guarda lo escrito ("PRUEBA1" en Lote batería, "Cumple" en Apariencia del poliblado; registro 8430) y elegir la Referencia no borra los demás campos. Es el llenado automático de la prueba en esa vista (hay dos botones "30 min" en la página). En septiembre, con el formulario original, los operarios sí guardaban esos campos.

Detalles de la prueba que no son errores: en TE11-2601 dos checkbox de "Verificación de línea auxiliar" no tienen texto porque es una grilla (la pregunta está en la etiqueta de la izquierda, como en el original); en TE11-0601 la copia A / R del reporte muestra "A" en las casillas Cumple.

## Hallazgos

- **Ítems que se guardan y el PDF no imprime:** la plantilla original no tiene la casilla (supervisores, EPP de AC10-1003, densidad y penetración de MZ07-0101, textos de hallazgo de SO02-4502…). Lista completa en `items-ajenos.md` ("Casillas que el PDF no tiene"). Decidir con el área si alguno debe salir
- **Hora de la firma del supervisor:** el "Revisado" se inserta con `CURRENT_TIMESTAMP` del servidor SQL; en develop el servidor está en UTC y queda 5 h adelante del resto del ciclo (EJ07-0101: Fin 15:06, Revisado 20:06). Anotado en el BACKLOG
- Ya conocidos (BACKLOG): CI11-0101 guarda 4844–4851 dos veces; PO11-0101-N guarda 5168 dos veces y 5169, que no existe en `papoitem`
