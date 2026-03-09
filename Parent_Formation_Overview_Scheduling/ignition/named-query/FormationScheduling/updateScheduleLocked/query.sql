update currentSchedule 
set 
	Locked = :locked , 
	tstamp = getdate()
where  EventID =  :eventID 
	
