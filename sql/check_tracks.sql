SELECT DISTINCT card_code ||' '|| voting_number ||'. '|| voting_title as title,
			    group_concat(v) as track

FROM list, requests, [values]

LEFT JOIN ( SELECT request_id as p_rid, value as v
			FROM [values] 
			WHERE title = 'Трек' OR title = 'Минусовка или видео')
	ON p_rid = request_id

WHERE
	list.id = topic_id AND requests.id = request_id AND
	default_duration > 0

GROUP BY request_id
HAVING track is NULL