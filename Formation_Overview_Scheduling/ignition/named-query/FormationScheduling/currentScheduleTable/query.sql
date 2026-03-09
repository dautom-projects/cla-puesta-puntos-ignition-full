SELECT currentSchedule.rowID,
  currentSchedule.tstamp,
  currentSchedule.StatusID,
  currentSchedule.EventID,
  currentSchedule.Batch,  
  currentSchedule.ItemID,
  currentSchedule.StartDate,
  currentSchedule.EndDate ,
  currentSchedule.[Group]
FROM currentSchedule
where  ItemID = :table and ( StatusID = 1 or StatusID = 2)
order by StatusID asc, StartDate asc