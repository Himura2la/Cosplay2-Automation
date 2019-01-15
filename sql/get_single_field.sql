SELECT DISTINCT phone

FROM list, requests, [values]

LEFT JOIN ( SELECT request_section_id as p_rsid, value as phone
			FROM [values] 
			WHERE title = 'Мобильный телефон')
	ON p_rsid = request_section_id

WHERE
	list.id = topic_id AND requests.id = request_id
	AND	status in ('waiting', 'materials')
	AND card_code not in ('SY', 'VOL')

