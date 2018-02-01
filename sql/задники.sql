SELECT 
	card_code ||' '|| voting_number as num,
	IFNULL(list.title||' / '||nom, list.title) as nom,
	nicks,
	team,
	fandom,
	cahrs,
	IFNULL(item_title, s_artist||' - '||s_title||IFNULL(' (OST '||s_ost||')', '')) as title,
	cities

FROM list, requests

LEFT JOIN (	SELECT request_id as nc_rid, REPLACE(GROUP_CONCAT(DISTINCT value), ',', ', ') as nicks
			FROM [values]
				LEFT JOIN (SELECT request_section_id as r_rsid, value as [role] FROM [values] WHERE title = 'Роль') 
				ON r_rsid = request_section_id
			WHERE title LIKE 'Ник%' AND ([role] = 'Участник' OR [role] IS NULL)
			GROUP BY request_id)
	ON nc_rid = requests.id

LEFT JOIN (	SELECT request_id as ct_rid, REPLACE(GROUP_CONCAT(DISTINCT value), ',', ', ') as cities
			FROM [values]
				LEFT JOIN (SELECT request_section_id as r_rsid, value as [role] FROM [values] WHERE title = 'Роль') 
				ON r_rsid = request_section_id
			WHERE title = 'Город' AND ([role] = 'Участник' OR [role] IS NULL)
			GROUP BY request_id)
	ON ct_rid = requests.id
				
LEFT JOIN (	SELECT request_id as n_rid, value as nom FROM [values] 
			WHERE title = 'Подноминация')
	ON n_rid = requests.id
				 
LEFT JOIN (	SELECT request_id as f_rid, value as fandom FROM [values] 
			WHERE title LIKE 'Фэндом%')
	ON f_rid = requests.id

LEFT JOIN (	SELECT request_id as ch_rid, REPLACE(GROUP_CONCAT(DISTINCT value), ',', ', ') as cahrs FROM [values] 
			WHERE title = 'Имя персонажа' OR title = 'Персонаж'
			GROUP BY request_id)
	ON ch_rid = requests.id

LEFT JOIN (	SELECT request_id as a_rid, value as s_artist FROM [values] 
			WHERE title LIKE 'Исполнитель композиции%')
	ON a_rid = requests.id

LEFT JOIN (	SELECT request_id as t_rid, value as s_title FROM [values] 
			WHERE title = 'Название композиции')
	ON t_rid = requests.id

LEFT JOIN (	SELECT request_id as o_rid, value as s_ost FROM [values] 
			WHERE title = 'OST (необязательно)')
	ON o_rid = requests.id

LEFT JOIN (	SELECT request_id as tm_rid, value as team FROM [values] 
			WHERE	title LIKE 'Название косб%' OR
					title = 'Команда (необязательно)' OR
					title = 'Название команды (необязательно)')
	ON tm_rid = requests.id

LEFT JOIN (	SELECT request_id as it_rid, value as item_title FROM [values] 
			WHERE	title = 'Название номера (необязательно)' OR
					title = 'Название сценки')
	ON it_rid = requests.id


WHERE
	list.id = topic_id
	AND status != 'disapproved'
	AND default_duration > 0

GROUP BY voting_number
ORDER BY voting_number