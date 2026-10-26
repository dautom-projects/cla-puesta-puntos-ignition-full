-- Preguntas fijas de los formularios -> papoitem.Description
-- Generado por papo_objects.py --questions-sql el 2026-10-26: el formulario lee la pregunta de papoItemID y
-- la base queda con el texto que mostraba. Aplicar en cla-db-papo y luego en producción.

SET XACT_ABORT ON;
BEGIN TRANSACTION;
-- Page/Embedded/Ensamble/Form_EA11-0901_2h, Page/Embedded/Ensamble/Form_EA11-0901_30min, Page/Embedded/Ensamble/Form_EA11-0901_4h · antes: N'Alineacion de soldadura .'
UPDATE papoitem SET Description = N'Alineación de soldadura' WHERE ID = 175;
-- Page/Embedded/Ensamble/Form_EA11-0901_2h, Page/Embedded/Ensamble/Form_EA11-0901_4h · antes: N'Densimetro segun la referencia y lista de materiales'
UPDATE papoitem SET Description = N'Densimetro según la referencia y lista de materiales' WHERE ID = 202;
-- Page/Embedded/Ensamble/Form_EA11-0901_2h, Page/Embedded/Ensamble/Form_EA11-0901_4h · antes: N'Aplicacion de silicona en ventozas para garantizar sello entre ventozas y roscas.'
UPDATE papoitem SET Description = N'Aplicación de silicona en ventozas para garantizar sello entre ventozas y roscas' WHERE ID = 213;
-- Page/Embedded/Ensamble/Form_EA11-0901_2h, Page/Embedded/Ensamble/Form_EA11-0901_4h · antes: N'Prueba de fuga en agua 5psi por 10 seg (Aplica solo para SOFASA).'
UPDATE papoitem SET Description = N'Prueba de fuga en agua 5psi por 10 seg (Aplica solo para SOFASA)' WHERE ID = 211;
-- Page/Embedded/Ensamble/Form_EA11-0901_2h, Page/Embedded/Ensamble/Form_EA11-0901_4h · antes: N'Planitud cubierta despues de Termosellado baterias ciegas.'
UPDATE papoitem SET Description = N'Planitud cubierta despúes de Termosellado baterías ciegas' WHERE ID = 195;
-- Page/Embedded/Ensamble/Form_EA11-0901_2h, Page/Embedded/Ensamble/Form_EA11-0901_4h · antes: N'No presencia rebabas ni quema los faldones de la cubierta.'
UPDATE papoitem SET Description = N'No presencia rebabas ni quema los faldones de la cubierta' WHERE ID = 198;
-- Page/Embedded/Ensamble/Form_EA11-0901_2h, Page/Embedded/Ensamble/Form_EA11-0901_4h · antes: N'Paralelismo Caja - Cubierta homogeneo en todos el perimetro.'
UPDATE papoitem SET Description = N'Paralelismo Caja - Cubierta homogeneo en todos el perimetro' WHERE ID = 196;
-- Page/Embedded/Ensamble/Form_EA11-0901_2h, Page/Embedded/Ensamble/Form_EA11-0901_4h · antes: N'Limpieza Residuos plasticos Zona inferior de las Planchas de Queme en cada cambio de Familia.'
UPDATE papoitem SET Description = N'Limpieza Residuos plàsticos Zona inferior de las Planchas de Queme en cada cambio de Familia' WHERE ID = 203;
-- Page/Embedded/Ensamble/Form_EA11-0901_2h, Page/Embedded/Ensamble/Form_EA11-0901_4h · antes: N'Electrodos al rojo vivo, ajustar con llama de baja.'
UPDATE papoitem SET Description = N'Electrodos al rojo vivo, ajustar con llama de baja' WHERE ID = 204;
-- Page/Embedded/Ensamble/Form_EA11-0901_4h, Page/Embedded/Ensamble/Form_EA11-0901_start · antes: N'Labios de queme parejos en todos los tabiques. (Bateria liberacon de primera pieza).'
UPDATE papoitem SET Description = N'Labios de queme parejos en todos los tabiques. (Batería liberacón de primera pieza)' WHERE ID = 197;
-- Page/Embedded/Ensamble/Form_EA11-0901_4h, Page/Embedded/Ensamble/Form_EA11-0901_start · antes: N'Prueba de fuga en agua 5psi por 10 seg para todas las baterias.'
UPDATE papoitem SET Description = N'Prueba de fuga en agua 5psi por 10 seg para todas las baterías' WHERE ID = 212;
COMMIT;

-- Rollback:
-- UPDATE papoitem SET Description = N'Alineacion de soldadura .' WHERE ID = 175;
-- UPDATE papoitem SET Description = N'Densimetro segun la referencia y lista de materiales' WHERE ID = 202;
-- UPDATE papoitem SET Description = N'Aplicacion de silicona en ventozas para garantizar sello entre ventozas y roscas.' WHERE ID = 213;
-- UPDATE papoitem SET Description = N'Prueba de fuga en agua 5psi por 10 seg (Aplica solo para SOFASA).' WHERE ID = 211;
-- UPDATE papoitem SET Description = N'Planitud cubierta despues de Termosellado baterias ciegas.' WHERE ID = 195;
-- UPDATE papoitem SET Description = N'No presencia rebabas ni quema los faldones de la cubierta.' WHERE ID = 198;
-- UPDATE papoitem SET Description = N'Paralelismo Caja - Cubierta homogeneo en todos el perimetro.' WHERE ID = 196;
-- UPDATE papoitem SET Description = N'Limpieza Residuos plasticos Zona inferior de las Planchas de Queme en cada cambio de Familia.' WHERE ID = 203;
-- UPDATE papoitem SET Description = N'Electrodos al rojo vivo, ajustar con llama de baja.' WHERE ID = 204;
-- UPDATE papoitem SET Description = N'Labios de queme parejos en todos los tabiques. (Bateria liberacon de primera pieza).' WHERE ID = 197;
-- UPDATE papoitem SET Description = N'Prueba de fuga en agua 5psi por 10 seg para todas las baterias.' WHERE ID = 212;
-- TEXTO DE LA BASE 173: se queda el de papoitem (preguntas_texto_base.json)
-- TEXTO DE LA BASE 201: se queda el de papoitem (preguntas_texto_base.json)
