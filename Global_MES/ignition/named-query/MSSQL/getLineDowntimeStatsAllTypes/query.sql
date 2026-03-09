SELECT 
    COUNT(1) AS downtime_event,
    rt.description,
    TIMESTAMPDIFF(SECOND, :startDate, 
        CASE WHEN :endDate > NOW() THEN NOW() ELSE :endDate END) AS total_seconds,
    COALESCE(SUM(TIMESTAMPDIFF(SECOND,
        CASE WHEN event_start < :startDate THEN :startDate ELSE event_start END,
        CASE WHEN COALESCE(event_end, NOW()) > :endDate THEN :endDate ELSE COALESCE(event_end, NOW()) END)), 0) AS down_secs,
    COALESCE(
        (CAST(TIMESTAMPDIFF(SECOND, :startDate, :endDate) AS DECIMAL) -
        SUM(TIMESTAMPDIFF(SECOND,
            CASE WHEN event_start < :startDate THEN :startDate ELSE event_start END,
            CASE WHEN COALESCE(event_end, NOW()) > :endDate THEN :endDate ELSE COALESCE(event_end, NOW()) END))) / TIMESTAMPDIFF(SECOND, :startDate, :endDate), 1.0) AS availability
            
FROM downtime_event_v3 de
INNER JOIN equipment_v3 e ON e.id = de.equipment_id
INNER JOIN reason_v3 re ON re.id = de.reason_id
INNER JOIN reason_type_v3 rt ON rt.id = re.type_id
WHERE de.line_id = :lineId
AND ((event_start BETWEEN :startDate AND :endDate) OR (event_end BETWEEN :startDate AND :endDate))
GROUP BY  rt.description
ORDER BY  rt.description;
