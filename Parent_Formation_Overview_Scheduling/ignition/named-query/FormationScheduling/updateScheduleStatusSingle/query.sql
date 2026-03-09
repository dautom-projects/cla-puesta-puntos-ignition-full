update currentSchedule 
set 
	StatusID = :statusID , 
	tstamp = getdate()
where  EventID =  :eventID 
	
