SELECT	wish as "Номинация",
		"" as code,
		requests.number as "№",
		'=HYPERLINK("https://atom23.cosplay2.ru/orgs/requests/request/'||requests.id||'", "'||REPLACE(IFNULL(voting_title,'[Заявка без названия]'),'"',"'")||'")' as "Заявка"

FROM list, requests

LEFT JOIN ( SELECT request_id as con_rid, value as contest
			FROM [values] 
			WHERE title == 'Приоритет заявки (необязательно)')
	ON con_rid = requests.id

LEFT JOIN ( SELECT request_id as t_rid, value as duration
			FROM [values] 
			WHERE title LIKE 'Продолжительность%')
	ON t_rid = requests.id

LEFT JOIN ( SELECT request_id as с_rid, REPLACE(GROUP_CONCAT(DISTINCT value), ',', ', ') as cities
			FROM [values] 
			WHERE title == 'Город'
			GROUP BY request_id)
	ON с_rid = requests.id

LEFT JOIN ( SELECT request_id as w_rid, value as wish
			FROM [values] 
			WHERE title == 'Номинация')
	ON w_rid = requests.id

LEFT JOIN ( SELECT request_id as b_rid, value as bodies
			FROM [values] 
			WHERE title == 'Количество участников')
	ON b_rid = requests.id
	
WHERE	list.id = topic_id
		AND status != 'disapproved'
--		AND default_duration > 0
		AND card_code LIKE 'FC'

ORDER BY wish, card_code, requests.number
