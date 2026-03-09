UPDATE currentSchedule
SET
   [Table] =  :table ,
    ItemID =  :table ,
   StartDate = :startDate  ,
  EndDate =  :endDate 
FROM currentSchedule
where  EventID =  :eventID 
