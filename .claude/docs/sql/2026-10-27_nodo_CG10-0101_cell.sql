-- Nodo de la segunda estación de CG10-0101 como CELL
-- 2026-10-27 · el nodo 1001 ("PC Name", hijo de la línea 85 "Llenadoras iniciales 2") se creó con Type 'Workstation' para
-- que CG10-0101 se llene desde otra estación en la misma línea. Digitalizacion_Template, Overview_Papos y CP-pk solo
-- resuelven la línea y el área desde nodos LINE o CELL: con 'Workstation' la ruta del formulario sale
-- Page/Embedded/None/... ("View Not Found"). CELL es el nivel bajo LINE (ENTERPRISE > SITE > AREA > LINE > CELL).
-- Su Topic era solo 'PC': Gestión y Gestión Gerencia arman la ruta del reporte con los 3 primeros segmentos del Topic
-- ('Report "PC/CG10-0101" does not exist'). Pasa a la ruta completa, como el resto de nodos (Topic del padre + '/' + Name).
-- nodepapo 2136 y workstationnode 1001 no cambian. Idempotente: solo cambia el nodo si sigue con los valores viejos.

SET XACT_ABORT ON;
BEGIN TRANSACTION;

UPDATE node SET Type = 'CELL' WHERE ID = 1001 AND Type = 'Workstation' AND ParentNodeID = 85;

UPDATE node SET Topic = 'Clarios/Andina/F&A/Llenadoras iniciales 2/PC Name' WHERE ID = 1001 AND Topic = 'PC';

COMMIT TRANSACTION;

-- Rollback
-- UPDATE node SET Type = 'Workstation', Topic = 'PC' WHERE ID = 1001 AND Type = 'CELL';
