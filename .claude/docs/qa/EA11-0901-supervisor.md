# QA de formularios PAPO

Generado: 2026-10-28 22:40 · Baseline: `HEAD` · Vistas: 1

Resultado: **FALLA** · 0 vistas pasan, 1 fallan

## Etapas globales

- ✅ 7 Grafo

## Por vista

### `Page/Embedded/Ensamble/Form_EA11-0901_start` · FALLA · 22 ítems, 0 respuestas comparadas
- ✅ 1 Estructura
- ❌ 2 Recolección: ítem 21: antes None en FlexContainerSupervisor, ahora 10938 en FlexContainerSupervisor
- ✅ 3 Respuestas
- ✅ 4 Flujo v2
- ✅ 5 Diseño
- ✅ 6 Contrato de objetos

La etapa 2 marca el cambio buscado: el ítem 21 (supervisor) pasa de `papoItemID` nulo a 10938 ("Supervisor" del PAPO 1), como se corrigió en EA11-1601 y EA11-2601 el 2026-10-26.

## Prueba (2026-10-28, navegador a 1920x1080)

- [x] Inicio guardado desde la estación 1: el último ítem es `{"papoItemID": 10938, "answer": "", "registerTypeID": 7}` (registro 8431; en develop el supervisor no tiene opciones sin ClariosAD)
- Quedan dos ítems nulos (posiciones 17 y 19) de `FlexContainerGroup3/FlexContainer_2` y `FlexContainer_3/FlexContainer`: contenedores con `custom.item` vacío que vienen del original (también en `_4h`); no llevan respuesta y ningún reporte los lee
