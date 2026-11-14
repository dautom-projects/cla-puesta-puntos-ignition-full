# Auditoría del modo tablet a 1280x800 (fase 0, 2026-11-14)

`ui_check.js` v1.4 sin llenar ni guardar (`papoUiAudit`, `minTouchPx: 40`) en el panel del navegador emulando una
tablet de 10" horizontal (1280x800), con el menú lateral cerrado (como quedará en la fase 1). Recorre los 69 PAPOs
con estación de la base de prueba (una estación por PAPO) y abre cada registro y cada sección: 210 formularios y
334 secciones. Los 28 `Form_*` sin botón en ninguna estación no se pueden abrir así (igual que en la prueba general).

## Resultado

| Revisión | 1280x800 | De esos, también a 1920x1080 |
|---|---|---|
| Textos cortados | 40 en 11 formularios | 39 (ya estaban en escritorio) |
| Filas apretadas / final de sección cortado | 0 | — |
| Campos fuera de la sección | 0 | — |
| Controles de menos de 40 px de alto | 1353 en 118 formularios: texto 869, numérico 339, dropdown 79, checkbox 66 | iguales (no dependen del ancho) |

- Con el menú cerrado, a 1280 px los formularios se ven como en escritorio: el único texto que se corta solo en
  tablet es "Condición placa, marcar con (X) si la placa es rep…" de **EA11-1603 1 hr** (Control por atributos).
- Los otros 39 están cortados también a 1920x1080 (revisados con el mismo script). Vienen de los originales y van al
  BACKLOG; no son del modo tablet:
  - AC10-0201 (Inicio, 30 min, Nueva Ref., Mantenimiento): preguntas largas en filas de una línea ("Densidad vs
    especificacion (min. 1280 - max. 1305)", "Valor del equipo vs especificacion: 20,5 +/- 2,5 y…", "Voltaje antes de
    la volcadora…", "Area de trabajo aseada…", "Cabinas electricas…")
  - EA11-1101 1 hr: etiquetas `Min:` / `Max:` y valores de tag `null` en celdas bajas
  - EA11-1601 2 hr: "Temperatura 1 Izquierda (Bateria Grande…" y "Temperatura 2 Derecha (Bateria Pequena…"
  - EA11-2501 2 hr: 10 valores de referencia en celdas bajas ("20 ms", "65 ± 5 PSI", "máx. 8%"…)
  - FO10-0100 (Ing. Baterias y Fin): "Temperatura agua de la mesa (menor a 45C)", "A quien se le escalo el problema…"
  - TE11-2601 Inicio: "En caso de presentar desviacion en el producto, re…"
- Lo que sí falta para tablet es el **tamaño táctil**: campos de texto y numéricos de unos 30 px, dropdowns y
  algunos checkbox bajos. Eso lo cubren las variantes de las clases `PAPO/Field/*` y las filas `PAPO/Tablet/*`
  (fases 2 y 3).
- Otros avisos que no son del modo tablet: 12 preguntas repetidas dentro de una sección (ya conocidas), 2 checkbox sin
  texto en TE11-2601 Inicio y el registro "Diario" de TR11-0102, que no es un formulario con secciones ni Guardar.

## Formularios con textos cortados (1280x800)

| PAPO | Registro | Secciones | Textos cortados | También a 1920 |
|---|---|---|---|---|
| AC10-0201 | Inicio | 5 | 5 | 5 |
| AC10-0201 | 30 min | 1 | 2 | 2 |
| AC10-0201 | Nueva Ref. | 1 | 2 | 2 |
| AC10-0201 | Mantenimiento | 1 | 3 | 3 |
| EA11-1101 | 1 hr | 1 | 12 | 12 |
| EA11-1601 | 2 hr | 2 | 2 | 2 |
| EA11-1603 | 1 hr | 4 | 1 | 0 |
| EA11-2501 | 2 hr | 6 | 10 | 10 |
| FO10-0100 | Ing. Baterias | 1 | 1 | 1 |
| FO10-0100 | Fin | 1 | 1 | 1 |
| TE11-2601 | Inicio | 4 | 1 | 1 |

## Cómo repetirla

1. Servir los scripts: configuración `papo-qa-scripts` de `.claude/launch.json` (python `http.server` en el puerto
   8765 sobre `.claude/skills/papo-qa/scripts`).
2. En el Template, con el panel a 1280x800 y el menú cerrado: cargar `ui_check.js` y la lista de PAPOs
   (`audit_list.js`: ruta del Template de una estación por PAPO, sacada de `workstationnode` + `nodepapo`) y correr
   `papoUiAudit(auditList, {wait: 900, openWait: 2500, navWait: 4000, minTouchPx: 40})`.
3. Seguir `papoAuditState` y resumir con `papoAuditMarkdown(papoAuditState.results)`.

La auditoría navega dentro del cliente (sin recargar) y espera con un `MessageChannel` cuando la página está en
segundo plano: con el panel oculto, los temporizadores del navegador se frenan a uno por segundo.
