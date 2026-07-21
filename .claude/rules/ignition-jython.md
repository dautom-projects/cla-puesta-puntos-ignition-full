---
paths:
  - "**/*.py"
  - "**/view.json"
  - "**/code.py"
---

# Reglas Ignition Perspective / Jython

## Jython 2.7 (Python 2)
- NO usar f-strings. Usar `"{}".format(...)`
- `unicode` y `basestring` existen (son de Python 2)
- `long` existe como tipo numérico
- NO usar sintaxis exclusiva de Python 3

## Convenciones de código PAPO
- Indentación con TABS (no espacios)
- camelCase para variables y funciones
- Funciones públicas sin `_`, helpers privados con `_`
- Docstring con Version / Changelog / Args / Returns
- Comentarios en inglés describiendo QUÉ hace
- `is` / `is not` para comparar con None
- Un solo try/except por función pública
- dbConnection SIEMPRE de view.custom o session.custom, nunca "papo_db" hardcoded
- Loggers nombrados por referencia del PAPO para filtrado

## Al editar view.json
- SIEMPRE backup primero
- Leer una vista estandarizada como plantilla antes de editar
- Validar JSON parseable después de editar
- Preservar custom.item de cada campo
- papo_core se llama SIN prefijo project.
- Al leer último RegisterCode: ORDER BY RegisterCode DESC (no Timestamp)
