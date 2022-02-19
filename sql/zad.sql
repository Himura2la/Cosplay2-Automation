SELECT 
    number as '№',
	card_code ||' '|| voting_number as num,
	ifnull(list.title||' / '||nom, list.title) as nom,
	CASE ifnull(length(team),0) WHEN 0 THEN nicks ELSE 'Косбэнд '||team||': '||nicks END as 'Участник',
	voting_title,
	fandom as 'Фэндом/OST',
	chars || ifnull(' - '||item_title,'') as 'Персонажи/Название',
	cities

FROM list, requests

LEFT JOIN (	SELECT request_id as nc_rid, REPLACE(GROUP_CONCAT(DISTINCT value), ',', ', ') as nicks
			FROM [values]
				LEFT JOIN (SELECT request_section_id as r_rsid, value as [role] FROM [values] WHERE title = 'Роль') 
				ON r_rsid = request_section_id
			-- TODO: Improve
			WHERE title LIKE 'Ник%' AND ([role] LIKE 'Участник%' OR [role] LIKE '%Скрипка%' OR [role] LIKE 'Пев%' OR [role] IS NULL)
			GROUP BY request_id)
	ON nc_rid = requests.id

LEFT JOIN (	SELECT request_id as ct_rid, REPLACE(GROUP_CONCAT(DISTINCT value), ',', ', ') as cities
			FROM [values]
				LEFT JOIN (SELECT request_section_id as r_rsid, value as [role] FROM [values] WHERE title = 'Роль') 
				ON r_rsid = request_section_id
			-- TODO: Improve
			WHERE title = 'Город' AND ([role] LIKE 'Участник%' OR [role] LIKE '%Скрипка%' OR [role] LIKE 'Пев%' OR [role] IS NULL)
			GROUP BY request_id)
	ON ct_rid = requests.id
				
LEFT JOIN (	SELECT request_id as n_rid, value as nom FROM [values] 
			WHERE title = 'Подноминация')
	ON n_rid = requests.id
				 
LEFT JOIN (	SELECT request_id as f_rid, value as fandom FROM [values] 
			WHERE title LIKE 'Фэндом%' OR title = 'OST (необязательно)')
	ON f_rid = requests.id

LEFT JOIN (	SELECT request_id as ch_rid, REPLACE(GROUP_CONCAT(DISTINCT value), ',', ', ') as chars FROM [values] 
			WHERE (title in ('Имя персонажа','Персонаж') OR title LIKE 'Исполнитель%')
			  AND section_title NOT LIKE 'Изображени%'
			  AND section_title NOT LIKE 'Фотографии%'
			GROUP BY request_id)
	ON ch_rid = requests.id


LEFT JOIN (	SELECT request_id as tm_rid, value as team FROM [values] 
			WHERE	title LIKE 'Название косб%' OR
					title = 'Команда (необязательно)' OR
					title = 'Название команды (необязательно)')
	ON tm_rid = requests.id

LEFT JOIN (	SELECT request_id as it_rid, value as item_title FROM [values] 
			WHERE title IN ('Название номера (необязательно)','Название работы','Название сценки','Название композиции'))
	ON it_rid = requests.id

WHERE
	list.id = topic_id
	AND status != 'disapproved'
	AND (default_duration > 0 OR card_code IN ('V', 'VC'))

GROUP BY voting_number
ORDER BY voting_number