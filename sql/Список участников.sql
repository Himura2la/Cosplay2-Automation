SELECT 
	last_name, first_name, mid_name, nick,
	city, tsu_num, vk

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

LEFT JOIN ( SELECT request_section_id as mn_rsid, value as mid_name
			FROM [values] 
			WHERE title = 'Отчество')
	ON mn_rsid = request_section_id
	
LEFT JOIN ( SELECT request_section_id as ln_rsid, value as last_name
			FROM [values] 
			WHERE title = 'Фамилия')
	ON ln_rsid = request_section_id


LEFT JOIN ( SELECT request_section_id as r_rsid, value as vk
			FROM [values] 
			WHERE title = 'Страничка ВКонтакте')
	ON r_rsid = request_section_id

 JOIN ( SELECT request_section_id as w_rsid, value as tsu_num
			FROM [values]
			WHERE title = 'Номер группы ТулГУ (необязательно)')
	ON w_rsid = request_section_id

WHERE
	list.id = topic_id AND requests.id = request_id
	AND	status != 'disapproved'
	AND	section_title in ("Участники", "Косплееры")

GROUP BY last_name, first_name, mid_name

order by voting_number