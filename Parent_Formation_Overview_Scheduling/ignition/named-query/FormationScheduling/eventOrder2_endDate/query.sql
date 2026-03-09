SELECT A.rowID,
  A.StartOrder,
  A.[Table],
  A.[Group],
  A.DUFWRev,
  A.StartDate,
  A.EndDate,
  A.FormHrs,
  A.RefillAcid
FROM currentSchedule A
WHERE A.StatusID = 2 AND A.ItemID <= :maxTable AND A.ItemID >= :minTable
ORDER BY A.EndDate