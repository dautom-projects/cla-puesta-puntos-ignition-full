DECLARE @startDate as datetime 
IF  (:setAuto  = 0  or  :startTime is NULL)
	BEGIN
		select top 1 @startDate =  EndDate from currentSchedule
		where  ItemID =  :table and  ( StatusID = 1 or StatusID = 2 )
		order by  EndDate  desc, rowID desc
		
		set @startDate = DATEADD(minute, :addTime,@startDate)
	END
ELSE
	BEGIN
		set @startDate =  :startTime
	END


insert into currentSchedule ( tstamp , StatusID ,  ItemID , StartDate , EndDate , Label,  DUFWRev, [Group], FormProg , FormHrs ,  RefillAcid,  BathLevel,  Priority ,  [Table], Qty,
	 TableAlias1 , DateSched , Shift , InRoom , ProdOrder , LegacyNumber , Pos , GpoDoof, Batch , StartOrder )
values (
	getdate(),
	2,
	:table ,
	@startDate, 
	DATEADD(minute, :timeLeft ,@startDate), 
	:label,
	:sku ,
	:group ,
	:formProg ,
	:formHours  ,
	:refillAcid ,
	:bathLevel ,
	:priority,
	:table,
	:qty,
	 :eastWest , :date , :shift , :inRoom , :prodOrder , :legacy , :pos , :gpoDoof , :batch,:startOrder
	
	)



update currentSchedule 
set 
	eventID = rowID
 where  rowID = SCOPE_IDENTITY()
 