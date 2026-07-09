# Rules for Editing view.json Files

## Before editing
1. Read the full view.json ONCE to map the structure
2. Identify Section{N} and FlexContainerGroup{N} pairs
3. Locate root.scripts (customMethods, messageHandlers) at the end of root object

## While editing
- Use targeted Edit tool calls — never rewrite the full file
- Preserve ALL `custom.item` objects (papoItemID mappings) — DO NOT modify
- Preserve ALL existing bindings on field components unless explicitly asked
- JSON must remain valid after every edit — no trailing commas, no missing brackets
- Maintain exact indentation (2 spaces for JSON)

## After editing
- Run `/sync` to trigger Designer project scan
- Confirm the JSON parses: `python -c "import json; json.load(open('path/to/view.json'))"`

## Component location pattern
In root.children array, components appear in this order:
1. spacer/title labels
2. Alternating: Section{N} → FlexContainerGroup{N} (for each question group)
3. spacer
4. FlexContainerSupervisor (supervisor dropdown)
5. Observaciones label + TextField
6. Button container (Guardar + Cancelar)

## Scripts location
- `root.scripts.customMethods` — array at the end of root object
- `root.scripts.messageHandlers` — array after customMethods
- View-level `events.system.onStartup` — at the top of the file, outside root
