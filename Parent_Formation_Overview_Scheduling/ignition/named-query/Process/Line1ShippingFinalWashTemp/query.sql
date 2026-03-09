SELECT t_stamp ,  ShippingFinalWashTempLine1 , :LowerValue as LowerBound ,:UpperValue as UpperBound
FROM production
WHERE   t_stamp <  getDate()
	and  t_stamp > DATEADD(day,-1,getDate())
order by t_stamp 
  
