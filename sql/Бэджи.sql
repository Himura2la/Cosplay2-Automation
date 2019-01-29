SELECT 
	group_concat(distinct card_code),
	REPLACE(group_concat(distinct card_code || ' ' || voting_number), ',', ', ') as nums,
	group_concat(distinct nick) as nick, first_name, last_name,
	city, section_title

	
FROM list, requests, [values]

LEFT JOIN ( SELECT request_section_id as сt_rsid, value as city
			FROM [values] 
			WHERE title = 'Город')
	ON сt_rsid = request_section_id

LEFT JOIN ( SELECT request_section_id as n_rsid, value as nick
			FROM [values] 
			WHERE title LIKE 'Ник%')
	ON n_rsid = request_section_id
	
LEFT JOIN ( SELECT request_section_id as fn_rsid, value as first_name
			FROM [values] 
			WHERE title = 'Имя')
	ON fn_rsid = request_section_id
	
LEFT JOIN ( SELECT request_section_id as ln_rsid, value as last_name
			FROM [values] 
			WHERE title = 'Фамилия')
	ON ln_rsid = request_section_id

LEFT JOIN ( SELECT request_section_id as w_rsid, value as will_be
			FROM [values]
			WHERE title = 'Приедет ли этот человек на фестиваль?')
	ON w_rsid = request_section_id

WHERE
	list.id = topic_id AND requests.id = request_id
	AND	status != 'disapproved'
	AND	section_title in ("Ваши данные","Помощники (необязательно)","Остальные участники","Другие косплееры (необязательно)","Соавторы (необязательно)","Члены команды","Представители","Авторы")
	AND	NOT (list.card_code in ('ART', 'FC', 'VC', 'V') and (will_be IS NULL or will_be = 'NO')) -- who did not told they won't come

GROUP BY last_name, first_name, city

order by last_name