SELECT  
 StartDate ,
  ItemID,
 DUFWRev ,
 [Group],
 EndDate ,
 Priority ,
 Locked ,
 Qty ,
 StatusID,
 EventID
FROM currentSchedule
where (StatusID = 1 or StatusID = 2 )
	and ItemID is not NULL 
	and DUFWRev is not NULL
	and StartDate is not NULL
order by StartDate asc,Priority asc,ItemID asc