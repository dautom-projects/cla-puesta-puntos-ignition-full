SELECT t_stamp ,ShippingFinalWashTempLine2 ,:LowerValue as LowerBound ,:UpperValue as UpperBound
FROM production
WHERE   t_stamp <  getDate()
	and  t_stamp > DATEADD(day,-1,getDate()) and ShippingFinalWashTempLine2 is not null
	order by t_stamp