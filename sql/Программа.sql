SELECT 
card_code ||' '|| voting_number ||'. '|| voting_title ||' ('||
REPLACE(GROUP_CONCAT(DISTINCT value), ',', ', ') ||')'

FROM
list, requests

LEFT JOIN (SELECT request_id, value FROM [values] 
				 WHERE title = 'Город' AND 
							 section_title NOT LIKE '%помощниках')
				ON request_id = requests.id

WHERE
list.id = topic_id AND
requests.id = request_id AND
status = 'approved' AND
voting_number > 100

GROUP BY voting_number
ORDER BY voting_number