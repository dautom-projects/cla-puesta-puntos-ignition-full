SELECT currentSchedule.rowID,
    currentSchedule.EventID,
    currentSchedule.EndDate ,
  currentSchedule.tstamp,
  currentSchedule.StatusID,
  currentSchedule.ItemID,
  currentSchedule.Alarm,
  currentSchedule.Enabled,
  currentSchedule.StatusIDSorting 
FROM currentSchedule
where  ItemID = :table and ( StatusID = 1 or StatusID = 2)
order by EndDate desc