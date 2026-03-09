SELECT t_stamp ,  CAST(Line1AcidTemp as int) as Line1AcidTemp , :LowerValue as LowerBound ,:UpperValue as UpperBound
FROM production
WHERE  t_stamp <  getDate()
	and  t_stamp > DATEADD(day,-1,getDate()) and Line1AcidTemp is not null
order by t_stamp 