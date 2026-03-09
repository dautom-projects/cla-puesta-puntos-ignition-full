UPDATE currentSchedule
SET
  currentSchedule.StartDate = :startDate  ,
  currentSchedule.EndDate =  :endDate ,
  currentSchedule.tstamp = getdate()
FROM currentSchedule
where  rowID =  :rowID 

