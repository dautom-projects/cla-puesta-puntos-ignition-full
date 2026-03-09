/* COMENTARIO   */
SELECT TOP ( :Cantidad_de_Filas ) t_stamp, Multitester_SKU, Test_Result_PLT1, Test_Result_PLT2
FROM 
     Multitester_PLT_Tabla
WHERE
     t_stamp 
         BETWEEN :Fecha_Inicial AND :Fecha_Final
ORDER BY
     t_stamp DESC
     
    