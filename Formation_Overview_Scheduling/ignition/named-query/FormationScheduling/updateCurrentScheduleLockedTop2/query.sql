declare @countLocked int = 0

--count how many locked in top 4
select @countLocked = sum(case when Locked = 1 then 1 else 0 end)
from (	
		SELECT Top(4) A.rowID,
		  A.[Table],
		  A.[Group],
		  A.DUFWRev,
		  A.StartDate,
		  cast( 
		  		concat(
		  				format(A.StartDate,'yyyy-MM-dd H:'),
		  				iif (CEILING(datepart(minute,A.StartDate) / 5.0) * 5 < 60, CEILING(datepart(minute,A.StartDate) / 5.0) * 5,'00')
		  				) 
		 				as datetime) 
		  	as StartTimeGroup,
		  A.EndDate,
		  A.FormHrs,
		  A.RefillAcid,
		  A.StartOrder,
		  A.Locked
		FROM currentSchedule A
		WHERE A.StatusID = 2 AND A.ItemID <= 40 AND A.ItemID > 20
		ORDER BY StartTimeGroup, A.StartOrder
) as data

select @countLocked

--update how many locked in top 4
if @countLocked < 4
begin

	with data as
	(
			SELECT Top(4) A.rowID,
		  A.[Table],
		  A.[Group],
		  A.DUFWRev,
		  A.StartDate,
		  cast( 
		  		concat(
		  				format(A.StartDate,'yyyy-MM-dd H:'),
		  				iif (CEILING(datepart(minute,A.StartDate) / 5.0) * 5 < 60, CEILING(datepart(minute,A.StartDate) / 5.0) * 5,'00')
		  				) 
		 				as datetime) 
		  	as StartTimeGroup,
		  A.EndDate,
		  A.FormHrs,
		  A.RefillAcid,
		  A.StartOrder,
		  A.Locked
		FROM currentSchedule A
		WHERE A.StatusID = 2 AND A.ItemID <= 37 AND A.ItemID >= 18
		ORDER BY StartTimeGroup, A.StartOrder
	)
	update data set Locked = 1
end

