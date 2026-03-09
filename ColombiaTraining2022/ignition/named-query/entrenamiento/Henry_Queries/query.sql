select top(:Cantidad_de_Filas ) 
 mes_table_ndx as [Item],
 t_stamp as [Fecha],
 MES_Product_Count as [Produccion],
 Expresion_Double as [Expresion doble]

from MES_table 
order by  t_stamp desc