# Prueba general de los formularios PAPO (2026-10-27)

Gateway local PAPOS (develop), base cla-db-papo, navegador a 1920x1080.

## Qué se probó

Los 69 PAPOs que tienen estación (Ensamble 11, F&A 19, Metalurgia 10, OREC 26, General 3) y sus 209 formularios, cada uno con el ciclo completo:

1. Firma del operario si había un ciclo abierto
2. Inicio y el resto de los registros del formulario
3. Firma del supervisor
4. Fin
5. Firma del operario

En cada registro, `ui_check.js` llena todos los campos, abre cada sección (sin filas comprimidas ni final cortado) y guarda. Después se abre el PDF del ciclo en Gestión y se compara casilla por casilla con lo guardado (`DataAnswer`). Para eso se leen las claves de la plantilla del `.bin` y las reglas del script de datos de cada reporte: por turno, por día de la semana, Si/No, Ok, marcas X, `<N/A>`…

## Resultado por área

| Área | PAPOs | Ciclos completos | PDF igual a lo guardado | Pendiente |
|---|---|---|---|---|
| Ensamble | 11 | 11 | 10 (EA11-1601 sin PDF: error 500 del reporte) | Reportes EA11-0901, EA11-1101, EA11-1501 y EA11-1601 (BACKLOG) |
| F&A | 19 | 19 | 19 | Plantillas GR10-0501 y PT11-0104 (BACKLOG) |
| Metalurgia | 10 | 10 | 10 | Reportes TR11-0101, TR11-0102 y SO02-4502 (BACKLOG) |
| OREC | 26 | 26 | 26 | Reporte EC07-0101; PO07-0101 mezcla ciclos de dos estaciones (BACKLOG) |
| General | 3 | 3 | 3 | — |

Todos los formularios guardan y firman.

## Corregido durante la prueba

| Commit | Qué |
|---|---|
| `e9d971a`, `60b2931` | Secciones cortadas en Ensamble (etiquetas sin alto fijo; altos medidos) |
| `b037b95`, `8503d84` | `fit_sections` v1.0.2: secciones sin `baseBasisPx` (se abren con su `position.basis`); 29 vistas |
| `e735ed8`, `e769ea4` | Regresión del estándar: scripts que leían `props.value` de campos que ya son objetos. RE11-0101_end guardaba None en la suma de "Produccion (kg)"; GR10-0501_start y PT11-0104_start ya no ponían la hora inicial. papo_qa v1.13.0 lo revisa |
| `ed49f9e` | Fila comprimida en "Seguridad" de TR11-0101_start |
| `580b304`, `127f19e` | Regresión del estándar: el Guardar de MZ11-0101_4h enviaba `saveStartShift`, un handler legacy que se había quitado, y el registro de 4 horas no se guardaba. papo_qa v1.14.0 lo revisa |
| `253829d` | Hallazgos de reportes, datos y originales en el BACKLOG |

Después de las dos regresiones se revisaron todas las vistas Form_* con las comprobaciones nuevas: no queda ninguna con el problema.

## Lo que no es del estándar (BACKLOG)

- **Reportes (Designer):**
  - GR10-0501: el Fin reemplaza el Inicio de su turno
  - PT11-0104: clave sin punto en el ítem 6257
  - TR11-0101: el rango deja fuera el 6350
  - TR11-0102: grilla mensual vacía
  - SO02-4502: tres casillas con claves de dos columnas
  - EJ11-0101: clave repetida, sale "7.0 7.0"
  - EC07-0101: referencia de la barcada cortada
  - EA11-1601: error 500
  - Varios reportes no tienen sección para el Fin
- **Datos:**
  - CG10-0101 asignado a un nodo `Workstation`: "View Not Found"; se probó en la línea 85
  - `RegisterCode` se numera por estación, pero los reportes filtran por nodo (PO07-0101)
- **Originales:**
  - EJ11-0101_1h no guarda nada
  - PO07-0101_start guarda 10 ítems dos veces
  - FO10-0601_input tiene un autocompletado que nunca funcionó
  - GR10-0501_start tiene checkbox ocultos con error

## Esperado en develop

- Sin ClariosAD: el supervisor queda vacío. El reporte muestra `<N/A>`, y el Revisado se guarda con hora UTC.
- Sin tags: los campos y etiquetas ligados a tags guardan None y el PDF imprime "None". Pasa en PA11-0301, EJ07-0101, EJ11-0102 y TE11-0601.
- Los campos calculados a partir de textos llenados con "QA" quedan vacíos (EJ07-0101 peso de pasta).

## Límites de la comprobación

- Los textos en vertical del PDF no se leen (usuario y firma por turno en SO02-1006 y SO02-4502).
- La grilla `turnoN.diaD` de TR11-0102 no se compara (sale vacía; está en el BACKLOG).
- El rojo fuera de rango y el modo oscuro no se midieron en esta prueba (ya se revisaron en las fases 4 y 5).
