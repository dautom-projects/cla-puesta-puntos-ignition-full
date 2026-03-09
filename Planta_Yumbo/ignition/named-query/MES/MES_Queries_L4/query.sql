select top(:Cantidad_de_Filas ) 
 mes_table_L4_ndx as [Item],
 t_stamp as [Fecha],
 COS_L4_Estado as [COS_L4_Estado],
 COS_L4_Falla as [COS_L4_Falla]

from   MES_Table_L4   
order by  t_stamp desc