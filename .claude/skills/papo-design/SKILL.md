---
name: papo-design
description: Aplica el estándar de diseño PAPO (clases de estilo PAPO/Field/* y tokens del tema) a vistas Form_* sin tocar la recolección de respuestas. Solo cambia props.style/textStyle; verifica que custom.item, los bindings y el orden de recolección queden idénticos y no escribe la vista si algo falla. Simula por defecto. Úsalo cuando pidan "estandarizar el diseño", "aplicar las clases", "unificar estilos" de un formulario, una familia o un área.
---

# papo-design

Aplica `style-classes/PAPO/` a los campos con `custom.item`, al TextField de Observaciones y a los títulos `text-titles`. Estándar y diagnóstico: `.claude/docs/ESTANDAR_DISENO.md`.

## Uso

Simular (no escribe nada):

```bash
python3 .claude/skills/papo-design/scripts/papo_design.py --views "Page/Embedded/Ensamble/Form_EA11-0901_1h"
python3 .claude/skills/papo-design/scripts/papo_design.py --all-forms --report /tmp/papo-design.md
```

Aplicar (backup en `.claude/backups/<fecha>/papo-design/`):

```bash
python3 .claude/skills/papo-design/scripts/papo_design.py --views "Page/Embedded/Ensamble/Form_EA11-0901_1h" --apply
```

`--views` acepta rutas relativas a `views/` o al repo, carpetas o `view.json`.

## Garantías (por vista)

- Fuentes de respuesta idénticas: `custom.item`, sus bindings e instancias de repeater, en el orden de `recopile`
- Ningún cambio fuera de `props.style` / `props.textStyle`
- Solo vistas con serialización Gson canónica; conserva CRLF
- Backup antes de escribir y verificación tras releer (restaura el backup si falla)

## Reglas

`scripts/rules.json`: tipo de componente → clase, clases viejas que se reemplazan (sin dejar anchos fijos: la de `dropdown` traía 250 px; en columnas que no estiran el campo queda con `width: 100%`), valores que la clase ya define (se quitan del campo solo si coinciden) y colores de títulos que pasan a tokens. Los estáticos que su propio binding sobrescribe se quitan.

## Objetos estándar (v2)

`scripts/papo_objects.py` reemplaza los campos interactivos por `Objects/*` embebidos: el `custom.item` queda en el componente del formulario y su `answer` lee la salida `answer` del objeto. Mismas garantías de recolección (ítems, bindings y orden). Ver `.claude/docs/OBJETOS_ESTANDAR.md`.

```bash
python3 .claude/skills/papo-design/scripts/papo_objects.py --views "Page/Embedded/Ensamble/Form_EA11-0901_1h"
```

## Después de aplicar

1. `python3 .claude/skills/papo-lint/scripts/papo_lint.py --views <vistas>`: el patrón `formFieldDesign` debe quedar en 0
2. Fila en `.claude/docs/DEPLOY_INVENTORY.md` (clases `PAPO/` antes que las vistas) y commit `refactor: diseño estándar en <vistas>`
3. Update Project en el Designer y revisión visual
