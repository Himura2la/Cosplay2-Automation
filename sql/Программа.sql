SELECT 
card_code ||' '|| voting_number ||'. '|| voting_title ||' ('||
REPLACE(GROUP_CONCAT(DISTINCT value), ',', ', ') ||')'

FROM
list, requests, [values]

WHERE
list.id = topic_id AND
requests.id = request_id AND
status = 'approved' AND
[values].title = 'Город' AND
voting_number > 100

GROUP BY voting_number
ORDER BY voting_number