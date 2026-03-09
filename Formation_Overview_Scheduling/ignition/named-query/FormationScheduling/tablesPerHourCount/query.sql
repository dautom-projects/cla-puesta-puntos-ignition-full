
select 'Tables Out Total' as [Table],[0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15],[16],[17],[18],[19],[20],[21],[22],[23],[24]
from
(
	SELECT ItemID as [Table],datediff(hour,getdate(),EndDate) as hourDiff--,[Label], StatusID
	FROM [Ignition].[dbo].[currentSchedule]
	where ItemID is not NULL
	and EndDate is not NULL
	and ( StatusID = 1 or StatusID = 2 )
	and ( StatusIDSorting <> 1 		--empty
		and StatusIDSorting <> 2	--unload mode
		and StatusIDSorting <> 11  	--waiting to put on charge
		and StatusIDSorting <> 14  	--load mode
		or StatusIDSorting is NULL) 
) as Src
PIVOT
(
	count([Table])
	for [hourDiff] in ([0],[1],[2],[3],[4],[5],[6],[7],[8],[9],[10],[11],[12],[13],[14],[15],[16],[17],[18],[19],[20],[21],[22],[23],[24])
) as Pvt


