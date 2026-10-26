-- Preguntas fijas de los formularios -> papoitem.Description
-- Generado por papo_objects.py --questions-sql el 2026-10-26: el formulario lee la pregunta de papoItemID y
-- la base queda con el texto que mostraba. Aplicar en cla-db-papo y luego en producción.

SET XACT_ABORT ON;
BEGIN TRANSACTION;
-- Page/Embedded/Metalurgia/Form_PA11-0301_start · antes: N'Tengo todos los elementos de proteccion personal para iniciar labores'
UPDATE papoitem SET Description = N'¿Tengo todos los elementos de protección personal para iniciar labores?' WHERE ID = 4216;
-- Page/Embedded/Metalurgia/Form_PA11-0301_start · antes: N'Tengo el area de trabajo en completo orden'
UPDATE papoitem SET Description = N'¿Tengo el área de trabajo en completo orden?' WHERE ID = 4218;
-- Page/Embedded/Metalurgia/Form_PA11-0301_start · antes: N'Los tableros del filtroprensa estan en buen estado (sin danos en estructura y aletas laterales)'
UPDATE papoitem SET Description = N'¿Están en buen estado los tableros del filtroprensa, no presentan daños en su estructura y aletas laterales?' WHERE ID = 4252;
-- Page/Embedded/Metalurgia/Form_PA11-0301_start · antes: N'Los elementos de izaje (polipasto, eslingas, viga separadora) se encuentran en buen estado'
UPDATE papoitem SET Description = N'Los elementos de izaje (polipasto, eslingas,viga separadora) se encuentran en buen estado' WHERE ID = 4253;
COMMIT;

-- Rollback:
-- UPDATE papoitem SET Description = N'Tengo todos los elementos de proteccion personal para iniciar labores' WHERE ID = 4216;
-- UPDATE papoitem SET Description = N'Tengo el area de trabajo en completo orden' WHERE ID = 4218;
-- UPDATE papoitem SET Description = N'Los tableros del filtroprensa estan en buen estado (sin danos en estructura y aletas laterales)' WHERE ID = 4252;
-- UPDATE papoitem SET Description = N'Los elementos de izaje (polipasto, eslingas, viga separadora) se encuentran en buen estado' WHERE ID = 4253;
-- TEXTO DE LA BASE 4220: se queda el de papoitem (preguntas_texto_base.json)
