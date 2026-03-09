select top( :numero_de_resultados ) 
 t_stamp as [Fecha],
  Temp_Real as [Temperatura Real] ,
   expresion_doble as  [Expresion doble]

from  entrenamiento_cris 
order by  t_stamp desc