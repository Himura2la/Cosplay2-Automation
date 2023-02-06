SELECT requests.id, voting_title, REPLACE(GROUP_CONCAT(DISTINCT nick), ',', ', ') as nicks, fandom, r_title, team
FROM list, requests

LEFT JOIN ( SELECT request_section_id as nc_rsid, request_id as nc_rid, value as nick
			FROM [values]
			WHERE title LIKE 'Ник%')
	ON nc_rid = requests.id

LEFT JOIN ( SELECT request_section_id as rl_rsid, request_id as rl_rid, section_title as role
			FROM [values])
	ON rl_rsid = nc_rsid

LEFT JOIN ( SELECT request_id as f_rid, value as fandom
			FROM [values]
			WHERE title LIKE "Фэндом%" OR title = "OST (необязательно)")
	ON f_rid = requests.id

LEFT JOIN ( SELECT request_id as cb_rid, value as team
			FROM [values]
			WHERE title LIKE "%команды%" OR title LIKE "%косбенда%" OR title LIKE "%косбэнда%")
	ON cb_rid = requests.id

LEFT JOIN ( SELECT request_id as rt_rid, GROUP_CONCAT(distinct value) as r_title
			FROM [values]
			WHERE (title LIKE "Название%" OR title LIKE "Исполнитель%") AND
			title NOT LIKE "%команды%" AND NOT title LIKE "%косбенда%" AND NOT title LIKE "%косбэнда%"
			GROUP BY rt_rid)
	ON rt_rid = requests.id


WHERE list.id = topic_id
  AND role NOT LIKE 'Помощник%'
  AND (default_duration > 0 AND card_code NOT IN ('V', 'VC'))
  AND status = 'approved'

GROUP BY requests.id
