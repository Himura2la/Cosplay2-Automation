SELECT 
card_code, voting_number, value,
voting_title

FROM
list, requests, [values]

WHERE
requests.id = request_id AND
list.id = topic_id AND
status = 'approved' AND
[values].title in ('Номинация', 'Тип номера')
