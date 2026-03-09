select top (10000)  
	format( dateadd(minute,75,dateadd(hour, datediff(hour, 0, t_stamp),0)),'ddd, M/d hh:mm tt')  as [Hour] , 
	max(FormationInCurrentShift) as [Formation In Total]
from  production
where  t_stamp >  :startDate 
	and  t_stamp < :endDate  
group by 
	dateadd(hour, datediff(hour, 0, t_stamp),0)
order by 
	dateadd(hour, datediff(hour, 0, t_stamp),0)
