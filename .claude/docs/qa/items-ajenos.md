# Ítems de otro PAPO y que no existen en los formularios (2026-10-28)

**Un ítem de otro PAPO no es error** (usuario, 2026-10-28): cada formulario guarda en su propio registro y el reporte lee las respuestas de ese registro por `papoItemID`, sin mirar de qué PAPO es el ítem. Comprobado en las plantillas: EA11-1201 y EA11-1501 imprimen 10964 (de GR10-0501), AC10-0201 imprime 11011 / 11012 (de EA11-1201), CA02-2102 imprime 10940 (de EA11-2201) y EA11-2201 imprime 348 / 349 / 6910. Lo que importa es que el reporte del formulario tenga la casilla y que el ítem no se repita dentro del mismo formulario.

La versión anterior de este archivo marcaba como problema todo ítem cuyo `papoitem.PapoID` no fuera el de la mayoría de la vista; queda descartado.

## IDs que no existen en `papoitem`

Todo viene de los originales (comparado con `6c57a21`); el estándar copió los mismos IDs.

| Vista | IDs | ¿El PDF tiene la casilla? |
|---|---|---|
| `Cubiertas/Form_PL11-0101-CU_start` | 1010446, 1010447 | No |
| `F&A/Form_FO10-0100_input` | 0 ×2 | No |
| `F&A/Form_FO10-0601_input` | 0 ×2 | No |
| `Metalurgia/Form_FU11-0101_start` | 5169 | No |
| `OREC/Form_PO11-0101-1_start` … `-4_start` | 5169 | No |
| `POLY/Form_PL11-0101-CAJA_start` | 9134–9139 | Su plantilla no usa claves `papoItemID` |

## Casillas que el PDF no tiene

No es por ser de otro PAPO: la plantilla del reporte no tiene la clave, así que se guarda y no se imprime. Puede ser a propósito (el reporte no muestra ese campo).

- `Ensamble/Form_EA11-2601_2h`: la sección "Doshoras" del reporte solo tiene 11352; los otros 24 campos (3075–3098) no salen
- `Ensamble/Form_EA11-2201_2h`: 11195, 11200 y 11201 no salen (348 / 349 / 6910 sí)
- `Ensamble/Form_EA11-1501_2h`: 11035 y 11036 no salen
- `Metalurgia/Form_TR11-0102_start`: el supervisor guarda 10949, que el PDF no tiene; la firma se lee del registro tipo 10, así que no se pierde

Encontrados en la verificación de F&A y OREC (2026-10-28, ciclo completo y PDF casilla por casilla, `verificacion-fa-orec.md`). Todas las plantillas son las originales (el estándar solo cambió los scripts de los reportes):

- Supervisor sin casilla (la firma sale del registro tipo 10): 10965 PT11-0104, 10969 FO10-1701-1, 10971 AC10-1801, 10972 AC10-0501, 10976 CA02-2102, 10977 AC10-0301, 10950 SO02-4502 (OREC); y 6201 ("Validación firma del supervisor/champion") en TE11-0601
- `F&A/Form_AC10-0201_*`: 5801 (ruidos extraños), 5804 (correa de la volcadora) y 6753 (multímetro)
- `F&A/Form_AC10-1003_*`: 5568 (tipo de estiba) y 6724–6730 (elementos de protección: botas, gafas, guantes, tapabocas, tapón)
- `F&A/Form_AC10-1801_*`: 5949 (cantidad de rechazos alto voltaje), 5950 (definición), 6830 (rayada) y 6832 (humedad)
- `F&A/Form_FO10-0601_*`: 6471 (baterías reportadas por aislamiento corto); el ítem 0 ya está arriba
- `F&A/Form_FO10-1701_*`: 6159 (borne picado)
- `F&A/Form_FO10-1701-1_*`: 6289 (turno) y 6296 (operario)
- `F&A/Form_TE11-2601_start`: 6904 (Termosellado TBS Ref) y 6905 (Probadora de fuga TBS Ref)
- `F&A/Form_GR10-0501_start`: 6052, 6056, 6060, 6064 y 6068 (los "Relevantes" de tanque 7, suavizador, lavadora, scrubber y planta F.A)
- `OREC/Form_CI11-0101_start`: 4851 (cinta pegante, tijeras, separador de cartón, estibas)
- `OREC/Form_EC07-0101_barcada`: 7930 (hora inicio); `_end`: 7955 (lote de papel batch date)
- `OREC/Form_MZ07-0101_30min`: 5231–5236 (densidad y penetración LCS / LC / LCI)
- `OREC/Form_SO02-4502_start`: los 16 textos "Hallazgo …" (4496–4526, pares); el PDF solo marca el ítem revisado
- `OREC/Form_RJ07-0101_end`: 7985 (producción buenas) y 7988 (kilos desperdicio)
- `OREC/Form_PO11-0101-N_start`: 5168 sí sale (marcas Antes / Durante); 5169 no existe en `papoitem` (arriba)

Cómo repetirlo: recorrer los `custom.item` de cada vista y buscar `papoItemID<ID>` en la plantilla de su reporte (`report_bin.py show <data.bin> --template`); los IDs, contra `SELECT ID FROM papoitem`.
