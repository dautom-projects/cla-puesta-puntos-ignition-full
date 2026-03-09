SELECT t_stamp ,  CONVERT(float,Line1RecircTankPH) as Line1RecircTankPH , :LowerValue as LowerBound ,:UpperValue as UpperBound
FROM production
WHERE t_stamp <  getDate()
	and  t_stamp > DATEADD(day,-1,getDate()) and  Line1RecircTankPH is not null
order by t_stamp 	
	
	
	