/* COMENTARIO   */
SELECT TOP ( :Cantidad_de_Filas ) t_stamp, MES_Estado_maquina_start_time ,  MES_Estado_maquina_end_time,  MES_Estado_maquina,  MES_Codigo_parada,  MES_Mantto_preventivo,  MES_Mantto_correctivo,  MES_Cambios,  MES_Casino,  MES_Microparos,  MES_Otros_tiempos_de_parada
FROM 
     MES_Poly_Iny3_Paradas_Tabla
WHERE
     t_stamp 
     BETWEEN :Fecha_Inicial AND :Fecha_Final
ORDER BY
     t_stamp DESC
     