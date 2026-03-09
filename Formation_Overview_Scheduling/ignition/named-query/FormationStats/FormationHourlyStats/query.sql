SELECT t_stamp,FINE,FINW,FEXE,FEXW,PrevFINE,PrevFINW,PrevFEXE,PrevFEXW 
FROM ValTestTable
WHERE t_stamp >= GETDATE()-1 AND
      (datepart(HOUR, t_stamp) ) =   :PrevHour 
order by t_stamp desc

select top t_stamp,  
	format( dateadd(minute,75,dateadd(hour, datediff(hour, 0, t_stamp),0)),'ddd, M/d hh:mm tt')  as [Hour] , 
	max(FormationCurrentShift) as [Formation Exit Total]
from  production
where  t_stamp >  :startDate 
	and  t_stamp < :endDate  
group by 
	dateadd(hour, datediff(hour, 0, t_stamp),0)
order by 
	dateadd(hour, datediff(hour, 0, t_stamp),0)
