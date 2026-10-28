# QA de formularios PAPO

Generado: 2026-10-28 00:54 · Baseline: `HEAD` · Vistas: 2

Resultado: **FALLA** · 0 vistas pasan, 2 fallan

## Etapas globales

- ✅ 7 Grafo

## Por vista

### `Page/Embedded/Ensamble/Form_EA11-1601_start` · FALLA · 22 ítems, 0 respuestas comparadas
- ✅ 1 Estructura
- ❌ 2 Recolección: ítem 16: antes 11190 en FlexContainerGroup2, ahora 11191 en FlexContainerGroup2; 23 ítems antes, 22 ahora
- ✅ 3 Respuestas
- ✅ 4 Flujo v2
- ✅ 5 Diseño
- ✅ 6 Contrato de objetos

### `Page/Embedded/Ensamble/Form_EA11-1601_start_PruebaPiloto` · FALLA · 22 ítems, 0 respuestas comparadas
- ✅ 1 Estructura
- ❌ 2 Recolección: ítem 16: antes 11190 en FlexContainerGroup2, ahora 11191 en FlexContainerGroup2; 23 ítems antes, 22 ahora
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

## Verificación de la falla 2 (esperada)

"Estado Termoselladora" (`FlexContainerGroup2`) tenía 9 filas para 8 ítems: 11190 (nivel de aceite) y 11191 (instrumentos calibrados) salían dos veces en pantalla y en el registro, y 11194 ("Las boquillas están limpias y en buen estado", en `papoitem` del PAPO 1105 y con su fila en el PDF) no estaba en ninguna fila. 11192 y 11193 sí se guardaban (sección "Estado Elementos de Soporte"; el BACKLOG decía que faltaban). La etapa 2 compara por posición, así que desde el ítem 16 cada campo se compara con el siguiente del baseline. Comprobado aparte contra `HEAD`:

- El árbol es igual a `HEAD` sin `Checkbox_5` (el segundo 11190), con `Checkbox_7` en 11194 (era el segundo 11191) y `baseBasisPx` 450 → 400 (8 filas de 50 px)
- Recolección: 23 → 22 ítems; los 10 ítems 11185–11194 una vez cada uno; el resto en el mismo orden y contenedor
- El reporte `EA11-1601` imprime por `papoItemID` (`@startShift.papoItemID11185@` … `11194@`): con esto se llena la fila de las boquillas, que antes salía vacía
- Mismo cambio en `Form_EA11-1601_start_PruebaPiloto`
- A 1920x1080 (2026-10-28, estación 75, ciclo 3): "Estado Termoselladora" con 8 filas en 400 px, sin preguntas repetidas ni filas cortadas; el Inicio (registro 8024) guarda 22 ítems con 11185–11194 una vez cada uno; ciclo cerrado (1 hr, firmas, Fin)
