select top(:Cantidad_de_Filas ) 
 mes_table_ndx as [Item],
 t_stamp as [Fecha],
 COS_L4_Estado as [COS L4 Estado],
 COS_L4_Falla as [COS L4 Falla]

from   MES_Table 
order by  t_stamp desc