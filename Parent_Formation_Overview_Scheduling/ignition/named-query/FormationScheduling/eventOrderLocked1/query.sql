SELECT A.rowID,
  A.[Table],
  A.[Group],
  A.DUFWRev,
  A.GpoDoof,
  A.Qty,
  A.StartDate,
 	iif(DATEPART(hour, A.StartDate) >= 23 and CEILING(datepart(minute,A.StartDate) / 5.0) * 5 >= 60,
	  	Convert(DateTime, DATEDIFF(DAY, -1, A.StartDate)),
	  		cast(
	  		concat(
	  				format(A.StartDate,'yyyy-MM-dd'),
	  				' ',
	  				iif (CEILING(datepart(minute,A.StartDate) / 5.0) * 5 < 60,DATEPART(hour, A.StartDate), 
	  						iif (DATEPART(hour, A.StartDate) >= 23, '00', DATEPART(hour, A.StartDate)+1 )
	  					),
	  				':',
	  				iif (CEILING(datepart(minute,A.StartDate) / 5.0) * 5 < 60, CEILING(datepart(minute,A.StartDate) / 5.0) * 5,'00')
	  				) 
	 				as datetime)
	 			)
  	as StartTimeGroup,
  A.EndDate,
  A.FormHrs,
  A.RefillAcid,
  A.StartOrder,
  ISNULL(A.Locked,0) as Locked
FROM currentSchedule A
WHERE A.StatusID = 2 AND A.ItemID <= :maxTable AND A.ItemID >= :minTable and ISNULL(A.Locked,0) = 1
ORDER BY Locked desc, StartTimeGroup, A.StartOrder