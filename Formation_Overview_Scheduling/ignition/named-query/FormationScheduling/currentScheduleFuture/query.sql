SELECT *
FROM currentSchedule
where  StatusID = 2 
	and ( locked <> 1 or locked is NULL )
	and ItemID >=1 and ItemID <= 37
order by ItemID asc, StartDate asc