SELECT 
    hi.LineID AS itemId,
    hi.ID,
    CASE
        WHEN StartDateTime < :startDate THEN :startDate
        ELSE StartDateTime
    END AS startDate,
    CASE
        WHEN COALESCE(EndDateTime, NOW()) > :endDate THEN :endDate
        ELSE COALESCE(EndDateTime, NOW())
    END AS endDate,
    hi.ReasonName AS label,
    CASE
        WHEN hi.ReasonCode IN (0, 2, 3, 4, 7, 10003, 10004, 10005, 10006, 10007) THEN '#FF8A8A'
        WHEN hi.ReasonCode IN (5, 6, 10000, 10001) THEN '#FFFF8A'
        WHEN hi.ReasonCode = 1 THEN '#8AFF8A'
    END AS color,
    0.7 AS opacity
FROM 
    mes_core.statehistory hi
WHERE
    (
        hi.StartDateTime BETWEEN :startDate AND :endDate
        OR COALESCE(hi.EndDateTime, NOW()) BETWEEN :startDate AND :endDate
    )
