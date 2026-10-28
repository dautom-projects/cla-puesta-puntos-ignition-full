# QA de formularios PAPO

Generado: 2026-10-28 13:11 · Baseline: `HEAD` · Vistas: 1

Resultado: **PASA** · 1 vistas pasan, 0 fallan

## Etapas globales

- ✅ 7 Grafo

## Por vista

### `Page/Embedded/F&A/Form_FO10-0100_input` · PASA · 19 ítems, 0 respuestas comparadas
- ✅ 1 Estructura
- ✅ 2 Recolección
- ✅ 3 Respuestas
- ✅ 4 Flujo v2
- ✅ 5 Diseño
- ✅ 6 Contrato de objetos

## 9 Visual (2026-10-28, navegador a 1920x1080, estación 13 de la base de prueba)

- [x] Sin ingresos en el ciclo, la tabla muestra "Sin ingresos de baterías en este ciclo" (sin encabezado)
- [x] Primer ingreso (mesa 1, 12 baterías): el total muestra 12 antes de guardar; al reabrir, la tabla lista la fila (13:08, mesa 1, cantidad 12, Soporte D.)
- [x] Segundo ingreso (mesa 2, 8 baterías): el total muestra 20 (suma del formulario, no de la mesa)
- [x] Después de guardar, la tabla se recarga sin recargar la página (el formulario embebido sigue vivo entre ingresos: el root recibe `refreshPreviewTable` de `papo_core.register.save`)
- [x] PDF desde Gestión (ciclo "En proceso"): página 1 con los ingresos 12 y 8; página 2 "TOTAL BATERIAS INGRESADAS" = 20
- Referencia sale "0" en la tabla porque los ingresos de prueba dejaron "Seleccionar" (es lo que se guarda)

Registros de prueba: IDs 8226 y el siguiente (PapoID 56, estación 13, ciclo 3), quedan "En proceso".
