SELECT nombresDeTurnoPresente, SUM( prodCount_LlenadorSLI )
FROM  produccion_formacionPorTurno 
where nombresDeTurnoPresente <> '' and  t_stamp > :diaDeEmpezar 
group by  nombresDeTurnoPresente 