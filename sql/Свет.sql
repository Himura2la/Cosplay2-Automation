SELECT 
card_code||' '||voting_number,
voting_title,
value

FROM
list, requests, [values]

WHERE
requests.id = request_id AND
list.id = topic_id AND
status = 'approved' AND
[values].title = 'Пожелания по сценическому свету (необязательно)'
