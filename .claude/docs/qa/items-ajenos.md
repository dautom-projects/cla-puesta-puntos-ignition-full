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

Cómo repetirlo: recorrer los `custom.item` de cada vista y buscar `papoItemID<ID>` en la plantilla de su reporte (`report_bin.py show <data.bin> --template`); los IDs, contra `SELECT ID FROM papoitem`.
