# QA de formularios PAPO

Generado: 2026-10-27 20:56 · Baseline: `HEAD` · Vistas: 1

Resultado: **FALLA** · 0 vistas pasan, 1 fallan

## Etapas globales

- ✅ 7 Grafo

## Por vista

### `Page/Embedded/F&A/Form_GR10-0501_start` · FALLA · 282 ítems, 0 respuestas comparadas
- ✅ 1 Estructura
- ❌ 2 Recolección: ítem 61: antes 6511 en FlexContainerGroup4, ahora 6512 en FlexContainerGroup5; 284 ítems antes, 282 ahora
- ❌ 3 Respuestas: 6512 (root/FlexContainerGroup5/Checkbox0): el original tiene lógica no reconocida (tipo ia.display.label); 6520 (root/FlexContainerGroup5/FlexContainer_5/DateTimeInput): el original tiene lógica no reconocida (tipo ia.display.label); 6521 (root/FlexContainerGroup5/FlexContainer_6/DateTimeInput): el original tiene lógica no reconocida (tipo ia.display.label); 6525 (root/FlexContainerGroup6/Checkbox0): el original tiene lógica no reconocida (tipo ia.display.label); 6533 (root/FlexContainerGroup6/FlexContainer_6/DateTimeInput): el original tiene lógica no reconocida (tipo ia.display.label) (+67)
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

## Verificación de las fallas 2 y 3 (esperadas)

Se quitaron a pedido del usuario las filas "Niveles de los tanques a inicio de turno" de Scruber (6511) y Torres de enfriamiento (6615): mostraban un tag y no se llenan. Las etapas 2 y 3 comparan por posición, así que desde el ítem 61 cada campo se compara con el siguiente del baseline. Comprobado aparte contra `HEAD`:

- El árbol es igual a `HEAD` sin esas dos filas y con `baseBasisPx` 712 → 662 (FlexContainerGroup4) y 690 → 640 (FlexContainerGroup12)
- Recolección: 284 → 282 ítems; faltan solo 6511 y 6615; el resto en el mismo orden y contenedor
- A 1920x1080: Scruber abre con 12 filas en 662 px y Torres con 12 en 640 px, sin filas cortas ni espacio sobrante; ciclo completo (Inicio 282 ítems, firmas, Fin) en el código 9 del nodo 29; PDF de Gestión con las casillas de nivel de Scrubber y Torres vacías
