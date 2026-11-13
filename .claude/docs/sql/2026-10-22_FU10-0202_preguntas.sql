-- FU10-0202 (papo 1102) - Formato de inspeccion de cargador frontal
-- 2026-10-22: tildes danadas en 17 preguntas y 3 campos nuevos de Inicio de turno (tipo 7)
-- Ejecutar con sqlcmd -f 65001 (archivo UTF-8). Idempotente.
SET NOCOUNT ON;
SET XACT_ABORT ON;
BEGIN TRAN;

-- 1) Tildes: el texto se guardo como UTF-8 leido en Latin-1 (DIRECCIAN -> DIRECCION)
UPDATE papoitem SET Description = (N'DIRECCI' + NCHAR(211) + N'N (ARTICULACIONES)') WHERE ID = 11268 AND PapoID = 1102;
UPDATE papoitem SET Description = (N'ASIENTO (ERGONOM' + NCHAR(205) + N'A)') WHERE ID = 11269 AND PapoID = 1102;
UPDATE papoitem SET Description = (N'PLACA DE DISE' + NCHAR(209) + N'O CON CAPACIDAD DE CARGA') WHERE ID = 11273 AND PapoID = 1102;
UPDATE papoitem SET Description = (N'ASEO DEL EQUIPO (PRESENTACI' + NCHAR(211) + N'N)') WHERE ID = 11274 AND PapoID = 1102;
UPDATE papoitem SET Description = (N'NIVEL ACEITE HIDR' + NCHAR(193) + N'ULICO') WHERE ID = 11276 AND PapoID = 1102;
UPDATE papoitem SET Description = (N'NIVEL ACEITE TRANSMISI' + NCHAR(211) + N'N') WHERE ID = 11277 AND PapoID = 1102;
UPDATE papoitem SET Description = (N'NIVEL ELECTROLITO BATER' + NCHAR(205) + N'A') WHERE ID = 11279 AND PapoID = 1102;
UPDATE papoitem SET Description = (N'PILOTOS LUM' + NCHAR(205) + N'NICOS') WHERE ID = 11281 AND PapoID = 1102;
UPDATE papoitem SET Description = (N'INDICADORES PRESI' + NCHAR(211) + N'N ACEITE MOTOR') WHERE ID = 11283 AND PapoID = 1102;
UPDATE papoitem SET Description = (N'INDICADOR TEMP. ACEITE HIDR' + NCHAR(193) + N'ULICO') WHERE ID = 11284 AND PapoID = 1102;
UPDATE papoitem SET Description = (N'HOR' + NCHAR(211) + N'METRO') WHERE ID = 11286 AND PapoID = 1102;
UPDATE papoitem SET Description = (N'INDICADOR DE CARGA BATER' + NCHAR(205) + N'A') WHERE ID = 11287 AND PapoID = 1102;
UPDATE papoitem SET Description = (N'FUNCIONALIDAD SISTEMA HIDR' + NCHAR(193) + N'ULICO DE LEVANTE') WHERE ID = 11291 AND PapoID = 1102;
UPDATE papoitem SET Description = (N'FUGAS DE ACEITE HIDR' + NCHAR(193) + N'ULICO') WHERE ID = 11293 AND PapoID = 1102;
UPDATE papoitem SET Description = (N'FUGAS DE ACEITE TRANSMISI' + NCHAR(211) + N'N') WHERE ID = 11294 AND PapoID = 1102;
UPDATE papoitem SET Description = (N'CARNET DE CAPACITACI' + NCHAR(211) + N'N NORMAS CLARIOS ANDINA') WHERE ID = 11299 AND PapoID = 1102;
UPDATE papoitem SET Description = (N'CARNET DE OPERACI' + NCHAR(211) + N'N DE CARGADOR FRONTAL') WHERE ID = 11300 AND PapoID = 1102;

-- 2) Campos nuevos de Inicio de turno (Responsable por Clarios Andina = Supervisor, ID 11303, ya existe)
IF EXISTS (SELECT 1 FROM papoitem WHERE ID IN (12374, 12375, 12376) AND PapoID <> 1102)
	THROW 50001, 'Los IDs 12374-12376 ya existen en otro formulario: elegir otros IDs y actualizar Form_FU10-0202_start', 1;
IF NOT EXISTS (SELECT 1 FROM papoitem WHERE ID IN (12374, 12375, 12376))
BEGIN
	SET IDENTITY_INSERT papoitem ON;
	INSERT INTO papoitem (ID, RegisterTypeID, PapoID, Description, AnswerType) VALUES
		(12374, 7, 1102, N'Interno / Externo', 'STRING'),
		(12375, 7, 1102, (N'N' + NCHAR(176) + N' cargador frontal'), 'STRING'),
		(12376, 7, 1102, N'Empresa contratista', 'STRING');
	SET IDENTITY_INSERT papoitem OFF;
END
INSERT INTO papoitem_registertype (PapoItemID, RegisterTypeID)
SELECT v.ID, 7 FROM (VALUES (12374), (12375), (12376)) AS v(ID)
WHERE NOT EXISTS (SELECT 1 FROM papoitem_registertype r WHERE r.PapoItemID = v.ID AND r.RegisterTypeID = 7);

COMMIT;

-- Verificacion
SELECT pi.ID, pi.RegisterTypeID, pi.Description FROM papoitem pi WHERE pi.PapoID = 1102 AND (pi.ID IN (12374, 12375, 12376) OR pi.ID IN (11268, 11269, 11273, 11274, 11276, 11277, 11279, 11281, 11283, 11284, 11286, 11287, 11291, 11293, 11294, 11299, 11300)) ORDER BY pi.ID;
