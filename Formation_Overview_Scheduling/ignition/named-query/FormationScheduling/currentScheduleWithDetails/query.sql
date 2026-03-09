SELECT 
  currentSchedule.EndDate ,
  currentSchedule.ItemID,
  currentSchedule.[Group],
   currentSchedule.RefillAcid,
   Label 
FROM currentSchedule
where  ( StatusID = 1 or StatusID = 2) and ItemID > 0
order by EndDate asc