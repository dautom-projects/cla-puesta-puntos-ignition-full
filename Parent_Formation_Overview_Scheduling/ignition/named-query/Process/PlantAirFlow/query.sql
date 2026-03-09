SELECT  t_stamp , PlantAirSCFM 
FROM production 
WHERE  t_stamp <=  getDate() and  t_stamp >= DATEADD(Hour,-12,getDate()) and PlantAirSCFM is not Null
order by t_stamp desc