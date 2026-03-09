select top (10000)  
	 t_stamp ,
	queryString

	
from  tableStatus 
where t_stamp > :startDate 
	and t_stamp < :endDate 
	and (
		statusID37 = 1 or
		statusID36  = 1 or
		statusID35  = 1 or
		statusID34  = 1 or
		statusID33  = 1 or
		statusID32  = 1 or
		statusID31  = 1 or
		statusID30  = 1 or
		statusID29  = 1 or
		statusID28  = 1 or
		statusID27  = 1 or
		statusID26  = 1 or
		statusID25  = 1 or
		statusID24  = 1 or
		statusID23  = 1 or
		statusID22  = 1 or
		statusID21  = 1 or
		statusID17  = 1 or
		statusID16  = 1 or
		statusID15  = 1 or
		statusID14  = 1 or
		statusID13  = 1 or
		statusID12  = 1 or
		statusID11  = 1 or
		statusID10  = 1 or
		statusID9  = 1 or
		statusID8  = 1 or
		statusID7  = 1 or
		statusID6  = 1 or
		statusID5  = 1 or
		statusID4  = 1 or
		statusID3  = 1 or
		statusID2  = 1 or
		statusID1  = 1 or
		statusID37 = 7 or
		statusID36  = 7 or
		statusID35  = 7 or
		statusID34  = 7 or
		statusID33  = 7 or
		statusID32  = 7 or
		statusID31  = 7 or
		statusID30  = 7 or
		statusID29  = 7 or
		statusID28  = 7 or
		statusID27  = 7 or
		statusID26  = 7 or
		statusID25  = 7 or
		statusID24  = 7 or
		statusID23  = 7 or
		statusID22  = 7 or
		statusID21  = 7 or
		statusID17  = 7 or
		statusID16  = 7 or
		statusID15  = 7 or
		statusID14  = 7 or
		statusID13  = 7 or
		statusID12  = 7 or
		statusID11  = 7 or
		statusID10  = 7 or
		statusID9  = 7 or
		statusID8  = 7 or
		statusID7  = 7 or
		statusID6  = 7 or
		statusID5  = 7 or
		statusID4  = 7 or
		statusID3  = 7 or
		statusID2  = 7 or
		statusID1  = 7
	)
	
	
	
	
	
Order by  t_stamp asc