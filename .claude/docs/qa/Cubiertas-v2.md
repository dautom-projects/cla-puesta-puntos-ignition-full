# QA de formularios PAPO

Generado: 2026-10-26 17:56 · Baseline: `HEAD` · Vistas: 3

Resultado: **FALLA** · 0 vistas pasan, 3 fallan

## Etapas globales

- ✅ 7 Grafo

## Por vista

### `Page/Embedded/Cubiertas/Form_PL11-0101-CA_start` · FALLA · 110 ítems, 0 respuestas comparadas
- ✅ 1 Estructura
- ❌ 2 Recolección: ítem 3: antes 9169 en FlexContainerGroup1, ahora 9169 en FlexContainerGroup2; cambió el binding de custom.insights
- ✅ 3 Respuestas
- ✅ 4 Flujo v2
- ❌ 5 Diseño: la raíz no tiene PAPO/Form
- ✅ 6 Contrato de objetos

### `Page/Embedded/Cubiertas/Form_PL11-0101-CU_start` · FALLA · 102 ítems, 0 respuestas comparadas
- ✅ 1 Estructura
- ❌ 2 Recolección: ítem 3: antes 10377 en FlexContainerGroup1, ahora 10377 en FlexContainerGroup2; cambió el binding de custom.insights
- ✅ 3 Respuestas
- ✅ 4 Flujo v2
- ❌ 5 Diseño: la raíz no tiene PAPO/Form
- ✅ 6 Contrato de objetos

### `Page/Embedded/Cubiertas/Form_PL11-0101-S&A_start` · FALLA · 155 ítems, 0 respuestas comparadas
- ✅ 1 Estructura
- ❌ 2 Recolección: ítem 2: antes 10780 en FlexContainerGroup1, ahora 10780 en FlexContainerGroup2; cambió el binding de custom.insights
- ✅ 3 Respuestas
- ✅ 4 Flujo v2
- ❌ 5 Diseño: la raíz no tiene PAPO/Form
- ✅ 6 Contrato de objetos

## 9 Visual (manual)

- [ ] Designer y Chrome se ven igual (Sections, botones, campos, valores de tag)
- [ ] Abrir la sección, llenar, cerrar y reabrir: los valores siguen
- [ ] Numérico fuera de rango en rojo
- [ ] Guardar un registro y correr `--compare-db <piloto> <original>`
- [ ] Reporte PDF del registro guardado
- [ ] Tiempo de apertura de la sección más grande (anotar segundos)
