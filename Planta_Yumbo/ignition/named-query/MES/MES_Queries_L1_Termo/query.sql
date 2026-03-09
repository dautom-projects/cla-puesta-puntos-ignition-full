select top(:Cantidad_de_Filas ) 
 mes_table_L1_ndx as [Item],
 t_stamp as [Fecha],
 COS_L1_Estado as [COS L1 Estado],
 COS_L1_Falla as [COS L1 Falla]

from   MES_Table_L1   
order by  t_stamp desc