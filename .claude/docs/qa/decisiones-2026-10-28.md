# QA de formularios PAPO

Generado: 2026-10-28 06:38 · Baseline: `HEAD` · Vistas: 5

Resultado: **FALLA** · 2 vistas pasan, 3 fallan

## Etapas globales

- ✅ 7 Grafo

## Por vista

### `Page/Embedded/F&A/Form_GR10-0501_start` · PASA · 282 ítems, 0 respuestas comparadas
- ✅ 1 Estructura
- ✅ 2 Recolección
- ✅ 3 Respuestas
- ✅ 4 Flujo v2
- ✅ 5 Diseño
- ✅ 6 Contrato de objetos

### `Page/Embedded/F&A/Form_GR10-0501_start_PruebaPiloto` · PASA · 284 ítems, 0 respuestas comparadas
- ✅ 1 Estructura
- ✅ 2 Recolección
- ✅ 3 Respuestas
- ✅ 4 Flujo v2
- ✅ 5 Diseño
- ✅ 6 Contrato de objetos

### `Page/Embedded/OREC/Form_CU11-0101_start` · FALLA · 21 ítems, 0 respuestas comparadas
- ✅ 1 Estructura
- ❌ 2 Recolección: ítem 20: antes 5275 en FlexContainerGroup8, ahora 10961 en FlexContainerSupervisor; 25 ítems antes, 21 ahora
- ✅ 3 Respuestas
- ✅ 4 Flujo v2
- ✅ 5 Diseño
- ✅ 6 Contrato de objetos

### `Page/Embedded/OREC/Form_CU11-0101_start_PruebaPiloto` · FALLA · 21 ítems, 0 respuestas comparadas
- ✅ 1 Estructura
- ❌ 2 Recolección: ítem 20: antes 5275 en FlexContainerGroup8, ahora 10961 en FlexContainerSupervisor; 25 ítems antes, 21 ahora
- ✅ 3 Respuestas
- ✅ 4 Flujo v2
- ✅ 5 Diseño
- ✅ 6 Contrato de objetos

### `Page/Embedded/OREC/Form_PO07-0101_start` · FALLA · 72 ítems, 0 respuestas comparadas
- ✅ 1 Estructura
- ❌ 2 Recolección: ítem 21: antes None en FlexContainerGroup1, ahora 8123 en FlexContainerGroup1
- ✅ 3 Respuestas
- ✅ 4 Flujo v2
- ✅ 5 Diseño
- ✅ 6 Contrato de objetos

## 9 Visual (manual)

- [ ] Designer y Chrome se ven igual (Sections, botones, campos, valores de tag)
- [ ] Abrir la sección, llenar, cerrar y reabrir: los valores siguen
- [ ] Numérico fuera de rango en rojo
- [ ] Guardar un registro y correr `--compare-db <piloto> <original>`
- [ ] Reporte PDF del registro guardado
- [ ] Tiempo de apertura de la sección más grande (anotar segundos)
