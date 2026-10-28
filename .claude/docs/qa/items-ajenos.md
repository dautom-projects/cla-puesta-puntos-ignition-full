# Ítems de otro PAPO en los formularios (2026-10-28)

Revisión de las 239 vistas `Form_*` (sin las `_PruebaPiloto`): cada `custom.item.papoItemID` contra `papoitem.PapoID` de cla-db-papo. Columna "PAPO de la vista" = el dueño de la mayoría de sus ítems. Todo viene de los originales (comparado con `6c57a21`); el estándar copió los mismos IDs. El reporte de cada PAPO solo imprime sus claves, así que un ítem ajeno se guarda y no sale en el PDF.

Encontrado al corregir GR10-0501 (`.claude/docs/qa/GR10-0501-ids.md`), donde siete numéricos guardaban en ítems de TE11-0601.

| Vista | PAPO de la vista (ítems) | Ítems ajenos o inexistentes |
|---|---|---|
| `Cubiertas/Form_PL11-0101-CU_start` | PL11-0101-CU (100) | 1010446 (no existe), 1010447 (no existe) |
| `Ensamble/Form_EA11-1201_start` | EA11-1201 (28) | 5981 (GR10-0501) ×2, 10964 (GR10-0501) |
| `Ensamble/Form_EA11-1501_2h` | EA11-1501 (22) | 11035 (EA11-1201), 11036 (EA11-1201) |
| `Ensamble/Form_EA11-1501_start` | EA11-1501 (21) | 10964 (GR10-0501) |
| `Ensamble/Form_EA11-2201_2h` | EA11-1601 (20) | 348 (EA11-2201), 349 (EA11-2201), 6910 (EA11-2201) ×2 |
| `Ensamble/Form_EA11-2601_1h` | EA11-2601 (14) | 276 (EA11-1101) |
| `Ensamble/Form_EA11-2601_2h` | EA11-2501 (24) | 11352 (EA11-2601) |
| `F&A/Form_AC10-0201_start` | AC10-0201 (79) | 11011 (EA11-1201), 11012 (EA11-1201) |
| `F&A/Form_CA02-2102_start` | CA02-2102 (49) | 10940 (EA11-2201) |
| `F&A/Form_FO10-0100_input` | FO10-0100 (17) | 0 (no existe) ×2 |
| `F&A/Form_FO10-0601_input` | FO10-0601 (19) | 0 (no existe) ×2 |
| `Metalurgia/Form_FU11-0101_start` | FU11-0101 (168) | 5168 (PO11-0101), 5169 (no existe) |
| `Metalurgia/Form_TR11-0102_start` | TR11-0102 (24) | 10949 (TR11-0101) |
| `OREC/Form_PO11-0101-1_start` | PO11-0101 (21) | 5169 (no existe) |
| `OREC/Form_PO11-0101-2_start` | PO11-0101 (21) | 5169 (no existe) |
| `OREC/Form_PO11-0101-3_start` | PO11-0101 (21) | 5169 (no existe) |
| `OREC/Form_PO11-0101-4_start` | PO11-0101 (21) | 5169 (no existe) |
| `POLY/Form_PL11-0101-CAJA_start` | PL11-0101-CA (109) | 9134 (no existe), 9135 (no existe), 9136 (no existe), 9137 (no existe), 9138 (no existe), 9139 (no existe) |
| `POLY/Form_PL11-0101-CUBIERTA_start` | PL11-0101-CU (70) | 9253 (PL11-0101-CA), 9254 (PL11-0101-CA), 9255 (PL11-0101-CA), 9256 (PL11-0101-CA), 9257 (PL11-0101-CA), 9258 (PL11-0101-CA), 9259 (PL11-0101-CA), 9260 (PL11-0101-CA), 9261 (PL11-0101-CA), 9262 (PL11-0101-CA), 9263 (PL11-0101-CA), 9264 (PL11-0101-CA), 9265 (PL11-0101-CA), 9266 (PL11-0101-CA), 9267 (PL11-0101-CA), 9268 (PL11-0101-CA), 9269 (PL11-0101-CA), 9270 (PL11-0101-CA), 9271 (PL11-0101-CA), 9272 (PL11-0101-CA), 9273 (PL11-0101-CA), 9274 (PL11-0101-CA), 9275 (PL11-0101-CA), 9276 (PL11-0101-CA), 9277 (PL11-0101-CA), 9278 (PL11-0101-CA), 9279 (PL11-0101-CA) |

## Lectura

- **Copias de otro formulario**: `EA11-2201_2h` lleva los ítems de EA11-1601 (11195 "Presión de aire" en 15 campos, 11200, 11201) y solo 4 propios; `EA11-2601_2h` usa los de EA11-2501 (3075–3098); `PL11-0101-CUBIERTA_start` tiene 27 de PL11-0101-CA. Para corregirlas hay que saber qué ítem propio corresponde a cada campo (y quizás crearlos en `papoitem`, cambio de base)
- **Supervisor con ítem ajeno**: el Dropdown del supervisor de `EA11-1201_start` y `EA11-1501_start` guarda 10964 (de GR10-0501) y el de `TR11-0102_start` 10949 (de TR11-0101). La firma se lee del registro tipo 10, así que no se pierde, pero el ítem queda mal
- **IDs que no existen**: 0 (`FO10-0100_input`, `FO10-0601_input`), 5169 (`PO11-0101-1..4`, `FU11-0101`, ya en el BACKLOG), 9134–9139 (`PL11-0101-CAJA_start`), 1010446–1010447 (`PL11-0101-CU_start`)
- **Sueltos**: 5981 en dos etiquetas de `EA11-1201_start`, 11035 / 11036 (EA11-1201) en `EA11-1501_2h`, 276 (EA11-1101) en `EA11-2601_1h`, 11011 / 11012 (EA11-1201) en `AC10-0201_start`, 10940 (EA11-2201) en `CA02-2102_start`, 5168 (PO11-0101) en `FU11-0101_start` (ya en el BACKLOG)

Cómo repetirlo: `SELECT i.ID, i.PapoID, p.Reference FROM papoitem i JOIN papo p ON p.ID = i.PapoID` y recorrer los `custom.item` de cada vista.
