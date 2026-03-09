SELECT  nombresDeTurnoPresente, SUM( prodCount_LlenadorSLI )
FROM  produccion_formacionPorTurno 
where nombresDeTurnoPresente <> ''
group by  nombresDeTurnoPresente 