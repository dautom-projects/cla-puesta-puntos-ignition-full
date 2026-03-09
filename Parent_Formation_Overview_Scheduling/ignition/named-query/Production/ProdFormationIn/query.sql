select top (10000)  
	t_stamp , 
	FormationInCurrentShift as [FormationInTotal], 
	[ActualProd FormInLine1]  as [FormInLine1] , 
	[ActualProd FormInLine2] as [FormInLine2], 
	:goalTarget as [Goal]
from  production 
where  t_stamp >  :startDate 
	and  t_stamp < :endDate 
order by t_stamp desc