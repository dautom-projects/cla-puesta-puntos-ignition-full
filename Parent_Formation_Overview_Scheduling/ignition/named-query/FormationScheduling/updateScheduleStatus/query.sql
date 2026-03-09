select *
from currentSchedule
where  ItemID  =  :table 
	and StatusID = 2


update currentSchedule 
set 
	StatusID = :statusID , 
	tstamp = getdate()
where  ItemID  =  :table 
	and StatusID = 2 
	
