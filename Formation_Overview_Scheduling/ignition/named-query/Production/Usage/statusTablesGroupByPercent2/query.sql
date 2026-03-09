

select Category, StatusCount
from
(

		select 
			count(case when statusID = 5 then 1 end) as [Charging],
			count(case when statusID = 4 then 1 end) as [ChargingComplete],
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
				statusID37 as [37],
				statusID36 as [36],
				statusID35 as [35],
				statusID34 as [34],
				statusID33 as [33],
				statusID32 as [32],
				statusID31 as [31],
				statusID30 as [30],
				statusID29 as [29],
				statusID28 as [28],
				statusID27 as [27],
				statusID26 as [26],
				statusID25 as [25],
				statusID24 as [24],
				statusID23 as [23],
				statusID22 as [22],
				statusID21 as [21]
			from tableStatus
			where t_stamp >  :startDate  and t_stamp < :endDate 
			--order by t_stamp desc
		) as cp
		UNPIVOT
		(
			statusID FOR status IN ([21],[22],[23],[24],[25],[26],[27],[28],[29],[30],[31],[32],[33],[34],[35],[36],[37])
		) as up

) as cp
UNPIVOT
(
	StatusCount for Category IN ([Charging],[ChargingComplete],[Unloading],[Empty],[Loading],[WaitingToPutOnCharge],[Alarm/Other])
) as up
--order by StatusCount desc

	
