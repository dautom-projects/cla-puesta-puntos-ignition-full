select top (10000)  t_stamp , FormationCurrentShift as [Formation Total], [ActualProd FormLine1] as [FormLine1] , [ActualProd FormLine2] as [FormLine2], :goalTarget as [Goal]
from  production 
where  t_stamp >  :startDate 
	and  t_stamp < :endDate 
order by t_stamp desc