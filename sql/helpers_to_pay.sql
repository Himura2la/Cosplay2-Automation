SELECT
	'https://tulafest.cosplay2.ru/orgs/requests/request/' || request_id as r,
	COUNT([value]) as n

FROM list, requests, [values]

WHERE list.id = topic_id AND requests.id = request_id
  AND section_title LIKE 'Помощник%' AND [values].title = 'Фамилия'
  AND status = 'approved'

GROUP BY request_id
HAVING n > 1
ORDER BY n DESC
