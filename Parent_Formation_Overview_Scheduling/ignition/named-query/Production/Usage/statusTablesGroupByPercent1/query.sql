

select Category, StatusCount
from
(

		select 
			count(case when statusID = 5 then 1 end) as [Charging],
			count(case when statusID = 4 or statusID = 6 then 1 end) as [ChargingComplete],
			count(case when statusID = 2 then 1 end) as [Unloading],
			count(case when statusID = 1 then 1 end) as [Empty],
			count(case when statusID = 14 then 1 end) as [Loading],
			count(case when statusID = 11 then 1 end) as [WaitingToPutOnCharge],
			--count(case when statusID1 = 7 then 1 end) as [ReadyToUnload],
			count(case when statusID = 13 then 1 end) as [Alarm/Other]
		from
		(
			select
				t_stamp, 
				{queryString1}
			from tableStatus
			where t_stamp >  :startDate  and t_stamp < :endDate 
			--order by t_stamp desc
		) as cp
		UNPIVOT
		(
			statusID FOR status IN ({queryString2})
		) as up

) as cp
UNPIVOT
(
	StatusCount for Category IN ([Charging],[ChargingComplete],[Unloading],[Empty],[Loading],[WaitingToPutOnCharge],[Alarm/Other])
) as up
--order by StatusCount desc

	
