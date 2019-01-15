SELECT	list.title as "Номинация",
		requests.status,
		COUNT(value) as "Кол-во",
		CAST(SUM(value) AS INT) || "m " || CAST(ROUND(SUM(value)*60)%60 AS INT) || "s (" || ROUND(SUM(value), 2) || "m)" as "Длительность"
FROM list, requests, [values]
WHERE	list.id = topic_id AND requests.id = request_id
		 AND [values].title LIKE 'Продолжительность%'
		 AND status != 'disapproved'
GROUP BY status, topic_id
ORDER BY status