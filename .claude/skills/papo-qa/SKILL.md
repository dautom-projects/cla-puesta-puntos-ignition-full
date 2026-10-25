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

## Etapas

| # | Etapa | Qué valida |
|---|---|---|
| 1 | Estructura | JSON parsea, Gson canónico, mismo fin de línea que el baseline |
| 2 | Recolección | Mismos `custom.item` (papoItemID, registerTypeID, bindings), orden y contenedor; instancias de repeater expandidas; `custom.insights` y el TextField de Observaciones intactos |
| 3 | Respuestas | Cada campo convertido a objeto responde igual que el original con valores de muestra, y su respuesta inicial (sección sin abrir) es la del campo sin tocar |
| 4 | Flujo v2 | Ningún hallazgo nuevo de wrappers del v2 ni de `"papo_db"` (comparado por ubicación); en vistas con `PAPO/Form`, sin handlers legacy |
| 5 | Diseño | Raíz con `PAPO/Form`, todo campo es objeto o tiene `PAPO/Field/*`, sin anchos fijos en px, sin clases inexistentes nuevas |
| 6 | Contrato | Los parámetros que pasa el formulario existen en el objeto; `answer` de salida, `value` inout; `custom.item.answer` lee `params.answer` |
| 7 | Grafo | Sin referencias no resueltas ni mensajes desbalanceados nuevos frente al grafo del baseline |
| 8 | Datos | Mismos ítems, orden, `registerTypeID` y formato de respuesta en dos registros |
| 9 | Visual | Checklist manual en el reporte |

## Pruebas del pipeline

```bash
python3 -m unittest discover -s .claude/skills/papo-qa/scripts/tests -v
```

Una copia limpia del piloto pasa y un error sembrado por etapa falla en esa etapa. Correrlas después de cualquier cambio a `papo_qa.py`.
