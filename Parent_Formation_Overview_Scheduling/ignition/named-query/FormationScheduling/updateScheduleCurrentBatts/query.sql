update currentSchedule 
set currentSchedule.label = IIF(  StatusIDColor = 6,'Empty',  concat('SKU: ',:battery)) ,
	StartDate = DATEADD(hour,-6,:currentTime), 
	EndDate = DATEADD(minute, :timeLeft ,:currentTime),
	EventID = concat('Current_', :table ),
	tstamp = :currentTime,
	TimeLeft =  :timeLeft,   
	Alarm =   :alarm ,
	Enabled =  :enabled ,
	 StatusIDSorting = :statusAuto,
	 StatusIDColor = :statusColor 
where StatusID = 1 and  ItemID =  :table 
