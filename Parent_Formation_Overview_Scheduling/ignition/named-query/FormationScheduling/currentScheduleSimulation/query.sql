SELECT 
    EndDate,
    ItemID,
  sum(360) OVER (
		ORDER BY EndDate
	) as Qty

FROM currentSchedule
where   ItemID IS NOT NULL and ItemID >= 0 and ItemID <= 100
	and ( StatusID = 1 or StatusID = 2 )
	and ( ItemID =  :table or  :table = -1)
order by EndDate asc