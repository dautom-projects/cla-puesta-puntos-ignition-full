SELECT TOP(100)
  tstamp as [Timestamp],
   ItemID,
 DUFWRev ,
 [Group],
 StartDate ,
 EndDate ,
 Priority ,
 Locked ,
 Qty ,
 StatusID,
 EventID
FROM currentSchedule
where StatusID = 4
	and ItemID is not NULL 
	and DUFWRev is not NULL
	and StartDate is not NULL
order by tstamp desc