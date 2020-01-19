SELECT	card_code as "Код",
		"№ " || requests.number as "№",
		contest as "Конкурс",
		'=HYPERLINK("http://tulafest.cosplay2.ru/orgs/requests/request/'||requests.id||'", "'||REPLACE(IFNULL(voting_title,'[Заявка без названия]'),'"',"'")||'")' as "Заявка",
		duration as "Длительность",
		cities as "Города",
		wish as "Пожелание по блоку"

FROM list, requests

LEFT JOIN ( SELECT request_id as con_rid, value as contest
			FROM [values] 
			WHERE title == 'Участие в конкурсе')
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
			WHERE title == 'Пожелание по расположению номера в программе (необязательно)')
	ON w_rid = requests.id
	
WHERE	list.id = topic_id
		AND status != 'disapproved'
		AND default_duration > 0

ORDER BY card_code