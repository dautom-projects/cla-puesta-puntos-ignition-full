SELECT databaseBES.DUFWRev,
  databaseBES.[Group],
  databaseBES.FormProg,
  databaseBES.FormHrs,
  databaseBES.RefillAcid,
  databaseBES.BathLevel,
  databaseBES.[Table], 
  databaseBES.Priority,
  databaseBES.Qty
FROM databaseBES
WHERE databaseBES.DUFWRev LIKE '%' + :skuFilter + '%'
	and databaseBES.[Group] LIKE '%' + :groupFilter  + '%'