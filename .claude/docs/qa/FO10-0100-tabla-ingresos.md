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

## Columnas del PDF (2026-10-28, pedido del usuario)

La tabla pasa a las 17 columnas de la página 1 del reporte, en su orden: Mesa de formación, Combinada, Circuitos, Referencia, Programa a ingresar, Programa cargado, Cantidad de baterías, Hora de inicio, Hora final estimada, Hora final real, Circuito con errores (fallas), Ingreso parcial, Nivel de agua programado de la mesa, Nivel de agua de la mesa medido, Temperatura agua de la mesa (menor a 45°C), Temperatura de la batería al inicio y Observaciones.

- [x] QA 1–7 y papo-lint sin hallazgos
- [x] Navegador a 1920x1080 con 4 ingresos del ciclo: Combinada e Ingreso parcial con ✔ / ✘ como el PDF, títulos en varias líneas, ningún encabezado ni celda cortada (revisado en el DOM)

## Sin Observaciones (2026-10-28, pedido del usuario)

- [x] La tabla queda con 16 columnas (sale Observaciones); QA 1–7 y papo-lint sin hallazgos; navegador a 1920x1080 sin celdas cortadas

## Alto según los registros (2026-10-28, pedido del usuario)

- [x] Alto = encabezado 84 px + 32 px por ingreso; sin ingresos 80 px (ícono y mensaje visibles)
- [x] Encabezado de 84 px: el título de 4 líneas ("Temperatura agua de la mesa (menor a 45°C)") se ve completo (antes 66 px y se cortaba)
- [x] Estación 44 sin ingresos y luego estación 13 en la misma sesión: la tabla pasa de vacía a 4 ingresos (214 px, sin scroll). Antes mostraba los de la estación anterior porque el formulario embebido no se recrea al cambiar de estación
