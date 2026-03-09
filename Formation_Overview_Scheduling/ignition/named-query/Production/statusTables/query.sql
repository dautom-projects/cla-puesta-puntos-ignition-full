select top (10000)  
	 t_stamp ,
	{queryString}

from  tableStatus 
where t_stamp > :startDate 
	and t_stamp < :endDate 
Order by  t_stamp asc