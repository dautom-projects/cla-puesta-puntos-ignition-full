SELECT
    1 as downtime_event,
    rt.description,
    TIMESTAMPDIFF(SECOND, :startDate, 
        CASE WHEN :endDate > NOW() THEN NOW() ELSE :endDate END) AS total_seconds,
    TIMESTAMPDIFF(SECOND, :startDate, 
        CASE WHEN :endDate > NOW() THEN NOW() ELSE :endDate END) AS down_secs,
    1 AS availability
FROM downtime_datalogger_v3 dd
INNER JOIN reason_v3 re ON re.id = dd.reason_id
INNER JOIN reason_type_v3 rt ON rt.id = re.type_id
WHERE dd.line_id = :lineId
AND (dd.t_stamp BETWEEN :startDate AND :endDate)
ORDER BY dd.downtime_datalogger_v3_ndx DESC
LIMIT 1 OFFSET 0;



