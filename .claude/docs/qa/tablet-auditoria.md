# Auditoría del modo tablet a 1280x800 (2026-11-14)

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
  algunos checkbox bajos. Eso lo cubren el bloque `MODO TABLET` del tema y las clases marcador `PAPO/Tablet/*`
  (fases 2 y 3).
- Otros avisos que no son del modo tablet: 12 preguntas repetidas dentro de una sección (ya conocidas), 2 checkbox sin
  texto en TE11-2601 Inicio y el registro "Diario" de TR11-0102, que no es un formulario con secciones ni Guardar.

## Después del modo tablet (fase 4)

Misma auditoría con las 238 vistas marcadas (`tablet_rows.py`) y el tema con el bloque `MODO TABLET` cargado en el
gateway local:

| Revisión | Antes | Después |
|---|---|---|
| Textos cortados | 40 en 11 formularios | 10, todos en EA11-2501 2 hr (valores de referencia en celdas de una fila horizontal, también cortados a 1920) |
| Filas apretadas / final de sección cortado | 0 | 0 |
| Campos fuera de la sección | 0 | 0 |
| Controles de menos de 40 px | 1353 en 118 formularios | 15 en 6 PAPOs |

- Los 15 controles que siguen de unos 32 px están anidados: el objeto queda dentro de contenedores que se encogen
  dentro de una fila de alto fijo. Son EA11-0901 1 hr (6 numéricos), AC10-0202-SLI (1 numérico en 4 registros),
  AC10-1801 Inicio (2 numéricos), FO10-0601 Fin y FO10-1701 Sal. Baterias (un dropdown cada uno) y CI11-0101 Inicio
  (el numérico nativo de dos rangos). Se pueden usar; quedan en el BACKLOG.
- Avisos de "checkbox sin texto" en AC10-1801, CA02-2102 y TR11-0101 fueron de tiempo de carga: con más espera
  salen limpios. El de TE11-2601 Inicio ya estaba antes.

## Encabezado del Template (AC10-1801, 2026-11-14)

La auditoría abre los registros con `click()` y no revisaba el encabezado. Revisión de los 69 PAPOs:

| Revisión | Antes, a 1280 | Después, a 1280 | Después, a 800 |
|---|---|---|---|
| Título partido o cortado | 6 a 25 px (AC10-1801, EA11-1501, PA11-0301, PL11-0101-S&A, RE11-0101, TE11-0601) | 0 (20 px, una línea) | 0 (20 px, hasta dos líneas dentro de la barra) |
| Botón de registro oculto | 2: "Fin" de AC10-1801 y EA11-1601 | 0 | 0 |
| Registros en dos filas | — | 0 | 15, todos de 5 o 6 registros (ninguno de estación con tablet) |
| Botones de firma estirados | — | 0 | 0 |

Bajo 1300 px los espacios vacíos de la barra pasan a 0 y los botones de registro a 120 px (el texto más largo, "Mantenimiento", mide 99): 4 registros caben en una fila desde 780 px, 5 desde 900 y 6 desde 1020. Los PAPOs de las estaciones con tablet tienen como mucho 4. A 1920x1080 el encabezado no cambia (81 fotos de `layout_snapshot.js`).

## Popups, ciclo y Overview en tamaño tablet (2026-11-15)

- **Ciclo completo a 800x600** en EA11-1201 (base de prueba): Guardar Inicio, Firma Supervisor, Guardar Fin y Firma Operario. En `registerhistory` quedaron En proceso (7), Revisado, En proceso (8), Finalizado y Sin Iniciar con RegisterCode 2.
- **Popups** de confirmación ("Guardar registro", "Firmar PAPO") y de aviso ("Firma Exitosa"): centrados y completos a 960 y 800 px. `Page/PopUps/Authenticator` (supervisor que firma sobre la sesión del operario) se abre centrado con 350x220 fijos y no depende del ancho; no se abrió en el ciclo porque la sesión era de `admin`, que firma sin pedir usuario.
- **Overview**: a 800 px el filtro Estación quedaba en 0 px y Ref se salía; corregido con bindings bajo 1300 px. Las tarjetas (431 px fijos) quedan de a una por debajo de unos 900 px. El pie de 9 px (`Total: …`) mide lo mismo a 1920: viene del original.
- **Pendiente**: en los 75 formularios con supervisor, el desplegable (`Objects/Dropdown`, 40 px en tablet) queda dentro de `FlexContainerSupervisor` de 32 px y se le cortan 8 px abajo.

## Formularios con textos cortados antes del modo tablet (1280x800)

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
