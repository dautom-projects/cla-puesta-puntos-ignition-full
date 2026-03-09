SELECT t_stamp , CONVERT(float,Line2RecircTankPH) as Line2RecircTankPH , :LowerValue as LowerBound ,:UpperValue as UpperBound
FROM production
WHERE   t_stamp <  getDate()
	and  t_stamp > DATEADD(day,-1,getDate()) and Line2RecircTankPH is not null
	order by t_stamp 