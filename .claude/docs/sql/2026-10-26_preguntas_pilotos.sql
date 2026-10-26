-- Preguntas fijas de los formularios -> papoitem.Description
-- Generado por papo_objects.py --questions-sql el 2026-10-26: el formulario lee la pregunta de papoItemID y
-- la base queda con el texto que mostraba. Aplicar en cla-db-papo y luego en producción.

SET XACT_ABORT ON;
BEGIN TRANSACTION;
-- Page/Embedded/Ensamble/Form_EA11-0901_1h_PruebaPiloto · antes: N'Verificacion del DAPE con muestra patron'
UPDATE papoitem SET Description = N'Verificación del DAPE con muestra patron' WHERE ID = 167;
-- Page/Embedded/Ensamble/Form_EA11-0901_1h_PruebaPiloto · antes: N'Huella 3.5 +/- 0.5 mm (verificacion del cumplimiento con galga) - Buen estado de los electrodos .'
UPDATE papoitem SET Description = N'Huella 3.5 ± 0.5 mm (verificación del cumplimiento con galga) Buen estado de los electrodos' WHERE ID = 174;
-- Page/Embedded/Ensamble/Form_EA11-0901_1h_PruebaPiloto · antes: N'Polaridad y referencia de cubierta segun la lista de materiales y programa de produccion.'
UPDATE papoitem SET Description = N'Polaridad y referencia de cubierta según la lista' WHERE ID = 199;
-- Page/Embedded/Ensamble/Form_EA11-0901_1h_PruebaPiloto · antes: N'Cubierta sin rechupes o contraccion.'
UPDATE papoitem SET Description = N'Cubierta sin rechupes o contracción' WHERE ID = 200;
-- Page/Embedded/Ensamble/Form_EA11-0901_1h_PruebaPiloto · antes: N'No presencia rebabas ni quema los faldones de la cubierta.'
UPDATE papoitem SET Description = N'No presencia rebabas ni quema los faldones de la cubierta' WHERE ID = 11458;
-- Page/Embedded/Ensamble/Form_EA11-0901_1h_PruebaPiloto · antes: N'Paralelismo Caja - Cubierta homogeneo en todos el perimetro.'
UPDATE papoitem SET Description = N'Paralelismo Caja - Cubierta homogeneo en todos el perimetro' WHERE ID = 11457;
-- Page/Embedded/Ensamble/Form_EA11-0901_1h_PruebaPiloto · antes: N'Altura borne positivo.'
UPDATE papoitem SET Description = N'Altura borne positivo' WHERE ID = 205;
-- Page/Embedded/Ensamble/Form_EA11-0901_1h_PruebaPiloto · antes: N'Altura borne negativo.'
UPDATE papoitem SET Description = N'Altura borne negativo' WHERE ID = 206;
-- Page/Embedded/Ensamble/Form_EA11-0901_1h_PruebaPiloto · antes: N'Verificacion de DAPE con muestra patron.'
UPDATE papoitem SET Description = N'Verificacion de DAPE con muestra patrón' WHERE ID = 210;
-- Page/Embedded/Ensamble/Form_EA11-0901_1h_PruebaPiloto · antes: N'Caja y cubierta de color sin talladuras.'
UPDATE papoitem SET Description = N'Caja y cubierta de color sin talladuras' WHERE ID = 214;
-- Page/Embedded/Ensamble/Form_EA11-0901_1h_PruebaPiloto · antes: N'Apariencia general de bateria segun criterios de aceptacion y rechazo RH02-0500 Anexo 4.'
UPDATE papoitem SET Description = N'Apariencia general de batería según criterios de aceptación y rechazo RH02-0500 Anexo 4.' WHERE ID = 215;
COMMIT;

-- Rollback:
-- UPDATE papoitem SET Description = N'Verificacion del DAPE con muestra patron' WHERE ID = 167;
-- UPDATE papoitem SET Description = N'Huella 3.5 +/- 0.5 mm (verificacion del cumplimiento con galga) - Buen estado de los electrodos .' WHERE ID = 174;
-- UPDATE papoitem SET Description = N'Polaridad y referencia de cubierta segun la lista de materiales y programa de produccion.' WHERE ID = 199;
-- UPDATE papoitem SET Description = N'Cubierta sin rechupes o contraccion.' WHERE ID = 200;
-- UPDATE papoitem SET Description = N'No presencia rebabas ni quema los faldones de la cubierta.' WHERE ID = 11458;
-- UPDATE papoitem SET Description = N'Paralelismo Caja - Cubierta homogeneo en todos el perimetro.' WHERE ID = 11457;
-- UPDATE papoitem SET Description = N'Altura borne positivo.' WHERE ID = 205;
-- UPDATE papoitem SET Description = N'Altura borne negativo.' WHERE ID = 206;
-- UPDATE papoitem SET Description = N'Verificacion de DAPE con muestra patron.' WHERE ID = 210;
-- UPDATE papoitem SET Description = N'Caja y cubierta de color sin talladuras.' WHERE ID = 214;
-- UPDATE papoitem SET Description = N'Apariencia general de bateria segun criterios de aceptacion y rechazo RH02-0500 Anexo 4.' WHERE ID = 215;
