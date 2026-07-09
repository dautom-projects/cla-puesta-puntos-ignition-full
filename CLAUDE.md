# CLA Puesta de Puntos — Project Instructions

## Docker Container
Docker container: `ignition-cla-puesta-puntos`
Database container: `mysql-cla-puesta-puntos`

## Project Structure
```
projects/
└── cla-project/
    ├── com.inductiveautomation.perspective/
    │   └── views/
    │       └── Page/Embedded/
    │           ├── Ensamble/
    │           │   ├── Linea 1/   (Form_EA11-1101_start, Form_EA11-1101_end, ...)
    │           │   └── Linea 4/
    │           ├── NFR/
    │           ├── Reciclado/
    │           ├── OREC/
    │           ├── F&A/
    │           ├── Cubiertas/
    │           └── Formacion/
    └── ignition/
        └── script-python/
            └── papo_core/   (register.py, ui.py, sign.py, report.py, overview.py)
```

## Database
- Engine: SQL Server
- Connection name: `papo_db`
- Never hardcode the connection — always use `self.view.custom.dbConnection` or `self.session.custom.dbConnection`

## view.json Structure (Form_XXXX_start / Form_XXXX_end)
All form views follow the same pattern:

### root.children order
```
spacer1 → Tittle → Section1 → FlexContainerGroup1 → Section2 → FlexContainerGroup2 → ... → spacerN → FlexContainerSupervisor → Label (Observaciones) → TextField → Label (spacer) → FlexContainer (buttons)
```

### Key objects
- **Section{N}** — label with onClick accordion script + binding to `FlexContainerGroup{N}.position.display`
- **FlexContainerGroup{N}** — flex container with 2 sub-columns, contains checkboxes with `custom.item.papoItemID`
- **FlexContainerSupervisor** — supervisor dropdown (papoItemID from `custom.papoItemID`)
- **root.scripts.customMethods** — `answerRecopile`, `toggleFlexRoot`
- **root.scripts.messageHandlers** — `saveDataRoot`

### Pairing rule
Section{N} ↔ FlexContainerGroup{N} (same index number)

### Do NOT touch
- `custom.item` on each field component (papoItemID mappings)
- Object paths and tag paths unless explicitly requested
- The main logic of existing scripts

## papo_core Convention
- Call: `papo_core.modulo.funcion(self)` — NO `project.` prefix
- Public functions: no underscore
- Private helpers: `_` prefix

## Sync
After editing any view.json, run `/sync` to trigger a Designer project scan.
The gateway Timer Script `claude-code-sync` detects the sentinel file and calls `system.project.requestScan()`.
