update currentSchedule 
set currentSchedule.label = IIF(  StatusIDColor = 6,'Empty',  concat('Group: ',:groupType ,'-',:battery)) ,
	StartDate = DATEADD(hour,-6,getdate()), 
	EndDate = DATEADD(minute, :timeLeft ,getdate()),
	EventID = concat('Current_', :table ),
	tstamp = getdate(),
	TimeLeft =  :timeLeft,   
	Alarm =   :alarm ,
	Enabled =  :enabled ,
	 StatusIDSorting = :statusAuto,
	 StatusIDColor = :statusColor 
where StatusID = 1 and  ItemID =  :table 
