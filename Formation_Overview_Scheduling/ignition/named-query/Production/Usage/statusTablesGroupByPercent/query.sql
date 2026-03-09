

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
				statusID18 as [18],
				statusID17 as [17],
				statusID16 as [16],
				statusID15 as [15],
				statusID14 as [14],
				statusID13 as [13],
				statusID12 as [12],
				statusID11 as [11],
				statusID10 as [10],
				statusID9 as [9],
				statusID8 as [8],
				statusID7 as [7],
				statusID6 as [6],
				statusID5 as [5],
				statusID4 as [4],
				statusID3 as [3],
				statusID2 as [2],
				statusID1 as [1]
			from tableStatus
			where t_stamp >  :startDate  and t_stamp < :endDate 
			--order by t_stamp desc
		) as cp
		UNPIVOT
		(
			statusID FOR status IN ([1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15],[16],[17],[18])
		) as up

) as cp
UNPIVOT
(
	StatusCount for Category IN ([ChargingComplete],[Charging],[Loading],[Unloading],[Empty],[WaitingToPutOnCharge],[Alarm/Other])
) as up
order by StatusCount desc

	
