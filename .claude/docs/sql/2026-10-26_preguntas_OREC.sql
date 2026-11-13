-- Preguntas fijas de los formularios -> papoitem.Description
-- Generado por papo_objects.py --questions-sql el 2026-10-26: el formulario lee la pregunta de papoItemID y
-- la base queda con el texto que mostraba. Aplicar en cla-db-papo y luego en produccion.

SET XACT_ABORT ON;
BEGIN TRANSACTION;
-- Page/Embedded/OREC/Form_EC11-0101_start  antes: N'Succion de Ciclon'
UPDATE papoitem SET Description = N'Succion ciclon' WHERE ID = 5123;
-- Page/Embedded/OREC/Form_MZ11-0101_4h, Page/Embedded/OREC/Form_MZ11-0101_start  antes: N'Tiempo de mezcla'
UPDATE papoitem SET Description = N'Tiempo de Mezcla' WHERE ID = 5167;
COMMIT;

-- Rollback:
-- UPDATE papoitem SET Description = N'Succion de Ciclon' WHERE ID = 5123;
-- UPDATE papoitem SET Description = N'Tiempo de mezcla' WHERE ID = 5167;
