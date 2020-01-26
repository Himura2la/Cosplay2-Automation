select s_type, voting_title, s_link, s_title, s_desc from list, requests 

LEFT JOIN (	SELECT request_id as l_rid, value as s_link FROM [values] 
			WHERE title = 'Сайт/группа' OR title = 'Ссылка')
	ON l_rid = requests.id
	
LEFT JOIN (	SELECT request_id as t_rid, value as s_type FROM [values] 
			WHERE title = 'Тип зоны')
	ON t_rid = requests.id
	
LEFT JOIN (	SELECT request_id as a_rid, value as s_title FROM [values] 
			WHERE title LIKE 'Название%')
	ON a_rid = requests.id

LEFT JOIN (	SELECT request_id as d_rid, value as s_desc FROM [values] 
			WHERE title = 'Описание')
	ON d_rid = requests.id
	
where list.id = topic_id
and card_code in ('ACG', 'SY')
and status != 'disapproved'