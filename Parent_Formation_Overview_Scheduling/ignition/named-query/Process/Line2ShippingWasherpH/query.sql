SELECT  t_stamp ,ShippingWasherPHLine2 , :LowerValue as LowerBound ,:UpperValue as UpperBound
FROM production
WHERE   t_stamp <  getDate()
	and  t_stamp > DATEADD(day,-1,getDate())  and ShippingWasherPHLine2 is not null
	order by t_stamp