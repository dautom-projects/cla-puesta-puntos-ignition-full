SELECT 
	ReasonName, COUNT(ID) AS count
FROM 
	statehistory
WHERE
	LineID = :lineId
	AND (
		StartDatetime < :endDate
		AND (EndDateTime IS NULL OR EndDateTime > :startDate)
	)
GROUP BY ReasonName
ORDER BY COUNT(ID) DESC
LIMIT 5;
