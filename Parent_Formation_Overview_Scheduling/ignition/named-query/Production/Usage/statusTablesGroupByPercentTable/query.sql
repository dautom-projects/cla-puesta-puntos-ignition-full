
DECLARE @SQL nvarchar(max)
declare @pmain varchar(max)
declare @p2go varchar(max)
declare @p3go varchar(max)
declare @endDate varchar(max)
declare @startDate varchar(max)

set @pmain = :pmainString 
set @p2go = :p2String 
set @p3go = :p3String 
set @endDate =  :endDate 
set @startDate =  :startDate 
 
 
SET @SQL = 'select Category, StatusCount as ' + quotename(@p2go) + '
from
(

		select 
			count(case when statusID = 5 then 1 end) as [Charging],
			count(case when statusID = 4 or statusID = 3 then 1 end) as [ChargingComplete],
			count(case when statusID = 2 then 1 end) as [Unloading],
			count(case when statusID = 1 then 1 end) as [Empty],
			count(case when statusID = 14 then 1 end) as [Loading],
			count(case when statusID = 11 then 1 end) as [WaitingToPutOnCharge],
			--count(case when statusID = 6 then 1 end) as [ReadyToUnload],
			count(case when statusID = 13 then 1 end) as [Alarm/Other]
		from
		(
			'+ @pmain + '
			from tableStatus
			where t_stamp > ''' + @startDate + '''   and t_stamp < ''' + @endDate + '''
		) as cp
		UNPIVOT
		(
			statusID FOR status IN ('+ quotename(@p3go) +')
		) as up

) as cp
UNPIVOT
(
	StatusCount for Category IN ([Charging],[ChargingComplete],[Unloading],[Empty],[Loading],[WaitingToPutOnCharge],[Alarm/Other])
) as up

'
 
EXEC (@SQL)



	
