SELECT	card_code || " " || voting_number as "№",
		fandom_type,
		REPLACE(IFNULL(voting_title,'[Заявка без названия]'),'"',"'") as "Заявка",
		CAST(round(duration * 60) as int) as "Длит. (сек)",
		IFNULL(bodies, 1) as "Тел",
		track_start,
		track_end,
		vol_help

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

LEFT JOIN ( SELECT request_id as b_rid, value as bodies
			FROM [values] 
			WHERE title == 'Количество участников')
	ON b_rid = requests.id

	
LEFT JOIN ( SELECT request_id as ts_rid, value as track_start
			FROM [values] 
			WHERE title == 'Начало выступления')
	ON ts_rid = requests.id

	
LEFT JOIN ( SELECT request_id as ft_rid, value as fandom_type
			FROM [values] 
			WHERE title == 'Тип источника')
	ON ft_rid = requests.id

LEFT JOIN ( SELECT request_id as te_rid, value as track_end
			FROM [values] 
			WHERE title == 'Наличие задержек после выступления')
	ON te_rid = requests.id
	
LEFT JOIN ( SELECT request_id as vh_rid, value as vol_help
			FROM [values] 
			WHERE title == 'Пожелания по сценическому свету')
	ON vh_rid = requests.id


WHERE	list.id = topic_id
		AND status != 'disapproved'
		AND default_duration > 0
		AND card_code NOT LIKE 'V%'

ORDER BY card_code, voting_number