SELECT t_stamp , 
	 Line2BattPerMin 
FROM production 
WHERE  t_stamp <  getDate()
	and  t_stamp > DATEADD(day,-1,getDate())
order by t_stamp desc