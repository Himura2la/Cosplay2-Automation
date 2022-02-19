SELECT
	REPLACE(group_concat(distinct card_code || ' ' || voting_number), ',', ', ') as nums,
	group_concat(distinct nick) as nick,
	ifnull(last_name, '') || ' ' || ifnull(first_name, '') || ' ' || ifnull(middle_name, '') as full_name,
	city,
	group_concat(distinct section_title) as section_titles,
	group_concat(distinct details),
	sum(default_duration) as scene,
	group_concat(distinct card_code)
	
FROM list, requests, [values]

LEFT JOIN ( SELECT request_section_id as n_rsid, value as nick
			FROM [values] 
			WHERE title LIKE 'Ник%')
	ON n_rsid = request_section_id
	
LEFT JOIN ( SELECT request_section_id as ln_rsid, value as last_name
			FROM [values] 
			WHERE title = 'Фамилия')
	ON ln_rsid = request_section_id
	
LEFT JOIN ( SELECT request_section_id as fn_rsid, value as first_name
			FROM [values] 
			WHERE title = 'Имя')
	ON fn_rsid = request_section_id

LEFT JOIN ( SELECT request_section_id as mn_rsid, value as middle_name
			FROM [values] 
			WHERE title = 'Отчество')
	ON mn_rsid = request_section_id

LEFT JOIN ( SELECT request_section_id as сt_rsid, value as city
			FROM [values] 
			WHERE title = 'Город')
	ON сt_rsid = request_section_id

LEFT JOIN ( SELECT request_id as det_rid, value as details
			FROM [values] 
			WHERE title in ('Название', 'Команда (необязательно)', 'Название мероприятия', 'Волонтёрское объединение (необязательно)'))
	ON det_rid = request_id
	
LEFT JOIN ( SELECT request_section_id as w_rsid, value as will_be
			FROM [values]
			WHERE title = 'Посещение фестиваля')
	ON w_rsid = request_section_id

WHERE
	list.id = topic_id AND requests.id = request_id
	AND	status != 'disapproved'
	AND	[values].title = 'Имя'  -- only sections with name
	AND NOT (list.card_code in ('ART', 'FC', 'VC', 'V') and (will_be IS NULL or will_be = 'Нет'))

GROUP BY full_name, city

order by section_title