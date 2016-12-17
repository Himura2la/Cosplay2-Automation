SELECT 
card_code ||' '|| voting_number, nicks, team, list.title||' / '||nom, fandom, cahrs, s_artist||' - '||s_title||' (OST '||s_ost||')' as track, item_title, cities

FROM
list, requests

LEFT JOIN (SELECT request_id as nc_rid, REPLACE(GROUP_CONCAT(DISTINCT value), ',', ', ') as nicks FROM [values] 
				 WHERE title LIKE 'Ник%' AND 
				 section_title NOT LIKE '%помощниках'
				 GROUP BY request_id)
				 ON nc_rid = requests.id
LEFT JOIN (SELECT request_id as c_rid, REPLACE(GROUP_CONCAT(DISTINCT value), ',', ', ') as cities FROM [values] 
				 WHERE title = 'Город' AND 
				 section_title NOT LIKE '%помощниках'
				 GROUP BY request_id)
                ON c_rid = requests.id
LEFT JOIN (SELECT request_id as n_rid, value as nom FROM [values] 
				 WHERE title = 'Номинация' OR title = 'Тип номера')
				 ON n_rid = requests.id
LEFT JOIN (SELECT request_id as f_rid, value as fandom FROM [values] 
				 WHERE title LIKE 'Фэндом%')
				 ON f_rid = requests.id
LEFT JOIN (SELECT request_id as ch_rid, REPLACE(GROUP_CONCAT(DISTINCT value), ',', ', ') as cahrs FROM [values] 
				 WHERE title = 'Имя персонажа' OR title = 'Персонаж'
				 GROUP BY request_id)
				 ON ch_rid = requests.id
LEFT JOIN (SELECT request_id as a_rid, value as s_artist FROM [values] 
				 WHERE title LIKE 'Исполнитель композиции%')
				 ON a_rid = requests.id
LEFT JOIN (SELECT request_id as t_rid, value as s_title FROM [values] 
				 WHERE title = 'Название композиции')
				 ON t_rid = requests.id
LEFT JOIN (SELECT request_id as o_rid, value as s_ost FROM [values] 
				 WHERE title = 'Если является OST-ом, то откуда')
				 ON o_rid = requests.id
LEFT JOIN (SELECT request_id as tm_rid, value as team FROM [values] 
				 WHERE title LIKE 'Название косб%' OR
							 title = 'Команда (необязательно)' OR
							 title = 'Название команды (необязательно)')
				 ON tm_rid = requests.id
LEFT JOIN (SELECT request_id as it_rid, value as item_title FROM [values] 
				 WHERE title = 'Название номера' OR
							 title = 'Название сценки (необязательно)')
				 ON it_rid = requests.id
WHERE
list.id = topic_id AND
status = 'approved' AND
voting_number > 100

GROUP BY voting_number
ORDER BY voting_number