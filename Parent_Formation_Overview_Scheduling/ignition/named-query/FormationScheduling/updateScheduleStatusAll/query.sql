update currentSchedule 
set 
	StatusID = :statusID , 
	tstamp = getdate()
where  StatusID = 2 
	and ( locked <> 1 or locked is NULL )
	and ItemID >=0 and ItemID <= 1000
	and  StartDate >=  :clearFrom 
