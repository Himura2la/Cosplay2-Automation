SELECT	"http://tulafest.cosplay2.ru/orgs/requests/request/" || requests.id as link,
		requests.number, list.title, contest,
		voting_title, duration, cities, wish

FROM list, requests

LEFT JOIN ( SELECT request_id as con_rid, value as contest
			FROM [values] 
			WHERE title == 'Участие в конкурсе')
	ON con_rid = requests.id

LEFT JOIN ( SELECT request_id as t_rid, CAST(value AS INT) || "m " || CAST(ROUND(value*60)%60 AS INT) || "s" as duration
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