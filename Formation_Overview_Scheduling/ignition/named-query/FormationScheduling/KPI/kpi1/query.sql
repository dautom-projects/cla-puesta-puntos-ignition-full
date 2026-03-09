SELECT 
	count(case when (ItemID >= :line1Min and ItemID <= :line1Max and StatusID = 2) then 1 end) as NumberOfFutureEventsLine1,
	count(case when (ItemID >= :line2Min and ItemID <=  :line2Max and StatusID = 2) then 1 end) as NumberOfFutureEventsLine2,
	count(case when (ItemID >= :line1Min and ItemID <= :line1Max and (StatusIDSorting = 2 or StatusIDSorting = 3 or StatusIDSorting = 4)) then 1 end) as NumberOfReadyTablesLine1, -- 4=charge comp, 2=unload mode, 3=ready to unload, 
	count(case when (ItemID >= :line2Min and ItemID <=  :line2Max and (StatusIDSorting = 2 or StatusIDSorting = 3 or StatusIDSorting = 4)) then 1 end) as NumberOfReadyTablesLine2, -- 4=charge comp, 2=unload mode, 3=ready to unload, 
	max(case when (ItemID >= :line1Min and ItemID <= :line1Max and StatusID = 1) then TimeLeft end) as MaxTimeLeftLine1,
	max(case when (ItemID >= :line2Min and ItemID <= :line2Max and StatusID = 1) then TimeLeft end) as MaxTimeLeftLine2
FROM currentSchedule
where   ItemID IS NOT NULL and ItemID >= :line1Min and ItemID <= :line2Max
	and (StatusID = 1 or StatusID = 2 )