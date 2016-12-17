SELECT 
REPLACE(GROUP_CONCAT(DISTINCT card_code||' '||voting_number), ',', ', ') AS numbers, 
nick, 
f_name||' '||l_name AS name, 
city, 
section_title

FROM
list, requests, 'values', persons

WHERE
requests.id = request_id AND
list.id = topic_id AND
persons.id = request_section_id AND
status = 'review' AND
section_title != 'Информация о фотографах'

GROUP BY name
ORDER BY nick