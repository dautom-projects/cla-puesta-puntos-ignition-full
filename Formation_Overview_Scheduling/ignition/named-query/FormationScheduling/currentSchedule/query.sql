SELECT currentSchedule.EventID,
  currentSchedule.ItemID,
  currentSchedule.StartDate,
  currentSchedule.EndDate,
  CASE
  	when (ROW_NUMBER() OVER (ORDER BY StartDate)) = 35 then concat('(NEXT1) ',currentSchedule.Label) --first row after number of tables
  	when (ROW_NUMBER() OVER (ORDER BY StartDate)) = 36 then concat('(NEXT2) ',currentSchedule.Label) --second row after number of tables
  	when currentSchedule.StatusIDColor = 1 then 'Empty'
  	when currentSchedule.StatusIDColor = 8 then 'Waiting to Put on Charge'
  	when currentSchedule.StatusIDColor = 6 then 'Loading'
  	else currentSchedule.Label
  END as Label,
  'color(0,0,0,255)' as [Foreground],
  CASE
  	when currentSchedule.EventID not like '%Current%' then 'color(71,255,255,255)' --main blue
  	when currentSchedule.StatusIDColor = 1 then 'color(255,71,255,255)' --light purple
  	when currentSchedule.StatusIDColor = 2 then 'color(255,255,255,255)' --white
  	when currentSchedule.StatusIDColor = 3 then 'color(255,140,0,255)' --dark orange
  	when currentSchedule.StatusIDColor = 4 then 'color(255,172,71,255)' --light orange
  	when currentSchedule.StatusIDColor = 5 then 'color(71,255,71,255)' --bright green
  	when currentSchedule.StatusIDColor = 6 then 'color(0,0,255,150)' --bright blue
  	when currentSchedule.StatusIDColor = 8 then 'color(255,245,74,255)' --yellow
  	when currentSchedule.StatusIDColor = 7 then 'color(255,71,71,255)' --red
  	when currentSchedule.StatusIDColor = 0 then 'color(213,213,213,255)' --gray
  	else						 'color(213,213,213,255)' --gray
  END as [Background],
  
  0 as [LeadTime],
  
'color(255,255,0,255)' as [LeadColor],
  -1 as  [PctDone]
FROM currentSchedule
where   ItemID IS NOT NULL and ItemID >= :line1Min and ItemID <= :line2Max
	and ( StatusID = 1 or StatusID = 2 )
order by StartDate asc,ItemID asc