SELECT *
FROM currentSchedule
With (NOLOCK)
where  StatusID = 2 
	and ( locked <> 1 or locked is NULL )
	and ItemID >= :lineMin1 and ItemID <= :lineMax2
order by ItemID asc, StartDate asc