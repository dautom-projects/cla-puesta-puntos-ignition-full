SELECT top( :resultados )
 test as [prueba],
  t_stamp [fechaa],
  Temp_Real as [temperatura] ,
   Temp_Real as [valor]
FROM tabla_temperatura_molde
order by t_stamp desc
