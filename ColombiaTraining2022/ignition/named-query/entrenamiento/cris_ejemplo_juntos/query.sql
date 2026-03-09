select top(:top ) *
from test_entrenamiento
where  Nivel_Real >  :nivel_minimo 
order by t_stamp desc