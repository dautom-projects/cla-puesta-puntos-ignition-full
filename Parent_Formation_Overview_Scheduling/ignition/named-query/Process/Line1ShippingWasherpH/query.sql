SELECT  t_stamp ,ShippingWasherPHLine1 , :LowerValue as LowerBound ,:UpperValue as UpperBound
FROM production
where t_stamp <  getDate()
	and  t_stamp > DATEADD(day,-1,getDate()) and ShippingWasherPHLine1 is not null 	 
order by t_stamp 