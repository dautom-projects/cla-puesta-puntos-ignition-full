/* COMENTARIO - VOLCADORA - NFR/ACABADO/Volcadora_Recetas_Queries  */
SELECT TOP (:Cantidad_de_Filas)
       t_stamp,
       No_Parte_Actual,
       Receta_Actual,
       No_Baterias_Actual,
       Angulo_Volteo_Actual,
       Tiempo_Volteo_Actual,
       No_Volteos_Actual,
       Angulo_Volcado_Actual,
       Tiempo_Volcado_Actual,
       Offset_Time_Volcado_Actual,
       Total_Time_Volcado_Actual,
       IGN_Comando_Historico
FROM Volcadora_Recetas_Tabla
WHERE
    t_stamp >= :Fecha_Inicial
    AND t_stamp <= :Fecha_Final
    
ORDER BY t_stamp DESC
     
    