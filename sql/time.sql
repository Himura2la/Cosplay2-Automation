SELECT	list.title as "Номинация",
		requests.status,
		COUNT(value) as "Кол-во",
		ROUND(SUM(value), 2) || " (" || REPLACE(ROUND(SUM(value)) - 1, '.0', '') || "m " || REPLACE(round(SUM(value)*60)%60, '.0', '') || "s)" as "Длительность"

FROM list, requests, [values]

WHERE	list.id = topic_id AND
		requests.id = request_id AND
		[values].title LIKE 'Продолжительность%'

GROUP BY topic_id
ORDER BY status, topic_id