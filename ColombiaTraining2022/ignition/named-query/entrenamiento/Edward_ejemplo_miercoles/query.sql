select top(:numero_resultados)
t_stamp as [fecha] ,
Expresion as [temperatura media] ,
Temp_Real as [temperatura real]
from Entrenamiento_Edward  
order by t_stamp desc