---
name: papo-qa
description: Pipeline de QA de los formularios PAPO, compuerta antes de cada commit de estandarización. Compara cada vista Form_* contra su versión en un commit baseline y valida estructura, recolección de respuestas (mismos custom.item, orden y contenedor), respuestas de los objetos frente al original, flujo v2, diseño estándar, contrato de los objetos, grafo de dependencias y, con dos registros guardados, el DataAnswer en la base. Úsalo antes de commitear cualquier cambio a formularios o cuando pidan "QA", "validar el estándar" o "comparar con el original".
---

# papo-qa

Ninguna parte de la estandarización se commitea si este pipeline no pasa. Plan: `/Users/dautom/.claude/plans/sorted-questing-sunrise.md`.

## Uso

Formularios cambiados contra el último commit (etapas 1–6, más la 7 con `--graph`):

```bash
python3 .claude/skills/papo-qa/scripts/papo_qa.py --views "Page/Embedded/Ensamble/Form_EA11-0901_start" --graph --report .claude/docs/qa/EA11-0901.md
```

Un piloto contra la copia original (commit donde se creó):

```bash
python3 .claude/skills/papo-qa/scripts/papo_qa.py --views "Page/Embedded/Ensamble/Form_EA11-0901_1h_PruebaPiloto" --baseline bd2dd43
```

Datos: tras guardar un registro desde el piloto, comparar su `DataAnswer` con uno del original (solo SELECT en `cla-db-papo`):

```bash
python3 .claude/skills/papo-qa/scripts/papo_qa.py --compare-db <ID piloto> <ID original>
```

Sale con código 1 si alguna etapa falla.

Crear o regenerar un piloto (copia `_PruebaPiloto` con el estándar completo y su reporte de QA):

```bash
python3 .claude/skills/papo-qa/scripts/make_pilot.py "Page/Embedded/F&A/Form_AC10-0201_start" [--rebuild]
```

Prueba de UI y guardado en el navegador (`scripts/ui_check.js`, se ejecuta dentro del cliente Perspective en la página de `Digitalizacion_Template`): abre un registro, recorre cada sección y verifica que no se corte el final, que no haya textos cortados, checkbox sin texto o preguntas repetidas, que las opciones queden en una línea, que marcar no desplace la página y que los valores sigan al cerrar y reabrir; luego llena todo con valores fijos (textos "QA", numéricos 7, horas 08:15, la última opción de cada dropdown) y, con `save: true`, guarda por la confirmación estándar. Cada sección reporta además su tiempo de apertura (`openMs`) y el color de rango de sus numéricos (`numericColors`) para compararlos entre original y piloto. Correrla a 1920 x 1080, la resolución para la que está hecha la aplicación. En el gateway local (develop) no hay `ClariosAD`: el supervisor queda sin opciones y el aviso "supervisor sin opciones" es esperado (en producción funciona; no tocarlo). Mismo flujo sobre el original y sobre el piloto (`pilot_swap.py`) y después `papo_qa.py --compare-db <piloto> <original> --exact`: con los mismos datos, las respuestas deben ser iguales (las horas del día se comparan solo por formato: cada guardado abre el formulario a otra hora). Usar una página de Perspective nueva en cada corrida: Perspective conserva la página y el estado de sus vistas al recargar mientras exista `perspective-tab-id` en `sessionStorage`; borrarlo antes de navegar.

Simular el estándar en todo el proyecto (originales leídos de git; no escribe nada): `python3 .claude/skills/papo-qa/scripts/simulate_all.py`.

Probar el guardado de un piloto desde el flujo real (el Template abre el original por ruta): `pilot_swap.py on <formulario>` pone el piloto en la ruta del original (con backup) y `pilot_swap.py off --all` lo restaura. No commitear con un intercambio activo (`pilot_swap.py status`).

## Etapas

| # | Etapa | Qué valida |
|---|---|---|
| 1 | Estructura | JSON parsea, Gson canónico, mismo fin de línea que el baseline |
| 2 | Recolección | Mismos `custom.item` (papoItemID, registerTypeID, bindings), orden y contenedor; instancias de repeater expandidas; `custom.insights` y el TextField de Observaciones intactos |
| 3 | Respuestas | Cada campo convertido a objeto responde igual que el original con valores de muestra, y su respuesta inicial (sección sin abrir) es la del campo sin tocar. Además muestra y hace lo mismo: pregunta o texto del checkbox, placeholder, `enabled`, bindings de valor y de opciones; una propiedad del original que el objeto no recibe falla |
| 4 | Flujo v2 | Ningún hallazgo nuevo de wrappers del v2 ni de `"papo_db"` (comparado por ubicación); en vistas con `PAPO/Form`, sin handlers legacy |
| 5 | Diseño | Raíz con `PAPO/Form`, todo campo es objeto o tiene `PAPO/Field/*`, sin anchos fijos en px, sin clases inexistentes nuevas; cada sección abierta (`custom.baseBasisPx`) alcanza para sus filas como en el original |
| 6 | Contrato | Los parámetros que pasa el formulario existen en el objeto; `answer` de salida, `value` inout; `custom.item.answer` lee `params.answer` |
| 7 | Grafo | Sin referencias no resueltas ni mensajes desbalanceados nuevos frente al grafo del baseline |
| 8 | Datos | Mismos ítems (por `papoItemID`, dice cuáles sobran o faltan), orden, `registerTypeID` y formato de respuesta en dos registros; las respuestas vacías, "-" o de tags sin valor no se comparan. Usar un registro del original con su versión actual |
| 9 | Visual | Checklist manual en el reporte |

## Pruebas del pipeline

```bash
python3 -m unittest discover -s .claude/skills/papo-qa/scripts/tests -v
```

Una copia limpia del piloto pasa y un error sembrado por etapa falla en esa etapa. Correrlas después de cualquier cambio a `papo_qa.py`.
