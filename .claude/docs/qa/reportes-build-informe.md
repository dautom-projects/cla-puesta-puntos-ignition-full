# Migración de los reportes a papo_core.report.build() (2026-10-28)

Gateway local PAPOS (develop), base cla-db-papo, navegador a 1920x1080.

## Qué se hizo

Los 65 reportes con script (todos menos `Default` y la copia de `Deleted/`) pasan a una sola llamada a `papo_core.report.build()` con su lista de secciones. 16 ya estaban migrados (piloto F&A, segunda familia F&A, OREC); esta ronda migra los 49 que faltaban:

| Área | Reportes |
|---|---|
| Ensamble | EA11-0901, EA11-1101, EA11-1201, EA11-1501, EA11-1601, EA11-1603, EA11-2201, EA11-2501, EA11-2601, EA11-4101, EA11-4200 |
| F&A | AC10-0201, AC10-0501, AC10-1003, AC10-1801, CG10-0101, FO10-1701-1, GR10-0501, PT11-0104, TE11-0401, TE11-0601 |
| Metalurgia | FU10-0202, FU11-0101, PA11-0301, PA11-0401, RE10-0102, RE11-0101, SO02-4502, TR11-0101, TR11-0102 |
| OREC | CI11-0101, CU11-0101, EC07-0101, MZ07-0101, MZ11-0101, PO11-0101, RJ07-0101, SO02-4502 |
| Pacifico y base | 10 PL11-0101 y `PAPO Vertical Base Shift Close` |

Las secciones salen de `report_convert.py` (lee el script viejo bloque por bloque) y, en los casos propios, a mano. Lo que solo tiene un reporte queda en unas líneas después de `build()`: los tags de MZ07-0101, las sumas de RJ07-0101, AC10-1801 y TE11-0601, los cálculos de RE11-0101, las firmas por turno de TR11-0102, `extractShiftChecklist` de FU10-0202 y la firma por hallazgo de SO02-4502.

`papo_core.report` pasó de v2.4.0 a v2.8.4 con las opciones que pedían estos reportes: casillas por turno (GR10-0501), por número de turno (TR11-0102), por día de la semana (TR11), por casilla semanal (SO02-4502), grilla mensual (`monthGrid`), encabezado de fecha y turno, copias con otra normalización, tipo de registro por casilla, marcas X anidadas y modo x (PT11-0104), marcas por texto de respuesta, ítems de un tipo dentro de otro registro (MZ11-0101), normalizaciones A/R, marca, Ok / No Ok. 73 tests.

## Cómo se probó

1. Comparación en sombra (`report_shadow.py`) de 22 reportes en todos sus ciclos antes de migrar
2. PDF base de cada reporte con su script viejo desde Gestión (un ciclo por reporte, la misma fila después)
3. Migración y commit por área
4. PDF final de la misma fila y comparación caja por caja; las marcas ✔ / ✘ se identifican por la forma del glifo (el código de la fuente cambia con el orden de uso)

## Resultado (41 reportes con ciclos)

| Resultado | Reportes |
|---|---|
| Igual caja por caja | 25: EA11-0901, EA11-1201, EA11-1501, EA11-1601, EA11-1603, EA11-2201, EA11-2501, EA11-2601, EA11-4101, EA11-4200, AC10-1801, CG10-0101, FO10-1701-1, PT11-0104, TE11-0401, TE11-0601, FU10-0202, MZ11-0101, PA11-0401, TR11-0101, TR11-0102, EC07-0101, PL11-0101-CA, PL11-0101-CU, PL11-0101-S&A |
| Solo cambios aprobados | 10: AC10-0201, AC10-0501, EA11-1101, GR10-0501, PA11-0301, RE10-0102, RE11-0101, MZ07-0101 (✘ → ✔ en la columna Cumple de los reprocesados; PA11-0301 además None en blanco); CI11-0101, PO11-0101 (turno de la planta y fecha con formato) |
| Cambios explicados | 6, abajo (SO02-4502 cuenta dos: Metalurgia y OREC) |

- **AC10-1003:** salen 4 marcas de la respuesta "Exportación" que el script viejo nunca imprimía (comparaba el texto con tilde sin `u""`)
- **FU11-0101:** desaparece una ✘ falsa del ítem 7906 (respuesta de texto "Mantenimiento Correctivo"; el script viejo reusaba la clave del ítem anterior)
- **CU11-0101:** el comentario sale en el orden de los registros (15:50 antes de 15:51)
- **RJ07-0101 y SO02-4502 (OREC):** ciclos cruzados entre Rejillas #1 y #2 del nodo 36: el PDF ya solo trae la estación de la fila (antes mezclaba registros de la #2), confirmado contra la base
- **SO02-4502 (Metalurgia):** sale una firma que antes quedaba vacía: el registro de prueba de develop guarda el rol como texto (`<ArrayWrapper>: [...]`) y el script viejo solo lo reconocía como lista

Los 8 sin ciclos en develop (7 copias de PL11-0101 y la base) tienen el mismo script, viejo y nuevo, que uno probado igual (PL11-0101-CA y EA11-1201).

## Corregido por la prueba

| Commit | Qué |
|---|---|
| `4ddf0c3` | `report_bin.py` leía mal los scripts de menos de 256 bytes que empiezan con salto de línea |
| `59996bb` | `true` / `false` de JSON en las secciones de cuatro reportes (Jython no los conoce) |
| `4b25ca2` | AC10-1801 (bueno = Si / malo = No, suma de rechazos), TE11-0601 (suma) y PT11-0104 (Ok / No Ok) |
| `b36886b` | La respuesta "Sí" con tilde no se clasificaba (MZ07-0101) |
| `1f0c213` | La marca de calidad salía como bytes UTF-8 ("âœ˜") en CU11-0101 |

## Pendiente

- `Digitalizacion_Template`: la tabla de vista previa y `lastRegisterType` todavía leen por nodo
- La consulta `RegisterHistory` queda sin uso en los reportes migrados (la tabla lee `RegisterHistoryStation`)
- El script viejo de EC07-0101 y EC11-0101 fallaba en algunos ciclos; con `build()` ya generan
