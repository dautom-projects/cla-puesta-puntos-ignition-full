SELECT 
	ReasonName,
	SUM(
		TIMESTAMPDIFF(MINUTE,
			GREATEST(StartDatetime, :startDate),
			LEAST(IFNULL(EndDateTime, :endDate), :endDate)
		)
	) AS total_minutes
FROM 
	statehistory
WHERE
	LineID = :lineId
	AND (
		StartDatetime < :endDate
		AND (EndDateTime IS NULL OR EndDateTime > :startDate)
	)
GROUP BY ReasonName
ORDER BY total_minutes DESC
LIMIT 5;