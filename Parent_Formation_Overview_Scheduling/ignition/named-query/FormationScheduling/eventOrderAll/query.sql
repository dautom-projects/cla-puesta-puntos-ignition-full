SELECT A.rowID,
  A.[Table],
  A.[Group],
  A.DUFWRev,
  A.GpoDoof,
  A.Qty,
  A.StartDate,
  cast( 
  		concat(
  				format(A.StartDate,'yyyy-MM-dd H:'),
  				iif (CEILING(datepart(minute,A.StartDate) / 5.0) * 5 < 60, CEILING(datepart(minute,A.StartDate) / 5.0) * 5,'00')
  				) 
 				as datetime) 
  	as StartTimeGroup,
  A.EndDate,
  A.FormHrs,
  A.RefillAcid,
  A.StartOrder,
  ISNULL(A.Locked,0) as Locked
FROM currentSchedule A
WHERE A.StatusID = 2 AND A.ItemID >= 0
ORDER BY Locked desc, StartTimeGroup, A.StartOrder