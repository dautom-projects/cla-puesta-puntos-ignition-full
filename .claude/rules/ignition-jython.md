---
paths:
  - "**/*.py"
  - "**/view.json"
  - "**/code.py"
---

# Reglas Ignition Perspective / Jython (PAPO)

## Jython 2.7
- Sin f-strings: usar "{}".format(...)
- unicode, basestring y long existen
- Nada de sintaxis exclusiva de Python 3

## Código
- Tabs, camelCase, funciones públicas sin _ y helpers privados con _
- Docstring con Version / Changelog / Args / Returns; comentarios en inglés (QUÉ, no CÓMO)
- is / is not para None; != en vez de <>
- Un solo try/except por función pública; logger.error con nombre = referencia del PAPO
- dbConnection siempre de view.custom o session.custom, nunca hardcodeado
- Lógica en el root con message handlers; los botones solo envían mensajes
- Turnos: nunca system.date.getHour24(); usar java.util.Calendar con TimeZone America/Bogota
- Último RegisterCode: ORDER BY RegisterCode DESC, nunca por Timestamp

## Al editar view.json
- Backup antes de tocar; usar una vista ya estandarizada como plantilla
- Validar que el JSON parsea después de editar
- Preservar custom.item de cada campo
- papo_core se llama sin prefijo project.
