SELECT '' || card_code || ' ' || voting_number || '. ' || list.title as num,
		voting_title,
		group_concat(distinct tr)
		
FROM list, requests, [values]

LEFT JOIN ( SELECT request_section_id as p_rsid, value as tr
			FROM [values] 
			WHERE title LIKE 'Транскрипция %')
	ON p_rsid = request_section_id

WHERE
	list.id = topic_id AND requests.id = request_id
	AND	status != 'disapproved'
	AND default_duration > 0

GROUP BY request_id
	
ORDER BY voting_number
