SELECT DISTINCT [json],
	requests.number, voting_title,
	"http://tulafest.cosplay2.ru/orgs/requests/request/" || requests.id as link,
	wish, exp

FROM list, requests, details

LEFT JOIN ( SELECT request_id as w_rid, value as wish
			FROM [values] 
			WHERE title = 'Пожелания')
	ON w_rid = requests.id  -- BEWARE MULTIPLE SECTIONS
	
LEFT JOIN ( SELECT request_id as e_rid, value as exp
			FROM [values] 
			WHERE title = 'Спецнавыки')
	ON e_rid = requests.id

WHERE
	list.id = topic_id AND requests.id = details.request_id
	AND card_code in ('VOL')

