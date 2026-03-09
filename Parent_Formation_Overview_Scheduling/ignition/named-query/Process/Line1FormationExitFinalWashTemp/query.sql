SELECT t_stamp ,  CONVERT(float,Line1FinalsWashTemp) as Line1FinalsWashTemp, :LowerValue as LowerBound ,:UpperValue as UpperBound
FROM production
WHERE t_stamp <  getDate()
	and  t_stamp > DATEADD(day,-1,getDate()) and  Line1FinalsWashTemp is not null  
order by t_stamp 