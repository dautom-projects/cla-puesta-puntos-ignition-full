/* COMENTARIO   */
SELECT TOP (:Cantidad_de_Filas)
       t_stamp,
       Referencia_Index,
       Referencia_Actual,
       Nivel_Maximo,
       Nivel_Minimo,
       Celda_1,
       Celda_2,
       Celda_3,
       Celda_4,
       Celda_5,
       Celda_6,
       Cabezal
FROM Llenadora_InicialHD_Cabezales_Tabla
WHERE
    t_stamp >= :Fecha_Inicial
    AND t_stamp <= :Fecha_Final

ORDER BY t_stamp DESC   