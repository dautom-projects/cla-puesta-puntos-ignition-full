SELECT t_stamp , CAST(Line2AcidTemp as int) as Line2AcidTemp, :LowerValue as LowerBound ,:UpperValue as UpperBound
FROM production
WHERE   t_stamp <  getDate()
	and  t_stamp > DATEADD(day,-1,getDate()) and Line2AcidTemp is not null
	order by t_stamp