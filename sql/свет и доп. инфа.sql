SELECT 
requests.number,
list.title,
--card_code||' '||voting_number,
voting_title,
replace(group_concat('### '||[values].title||':\n'||value||'\n'), '\n,', '\n') as text

FROM
list, requests, [values]

WHERE
requests.id = request_id AND
list.id = topic_id AND
status = 'approved' AND
[values].value != '' AND
([values].title = 'Пожелания по сценическому свету (необязательно)' OR
 [values].title = 'Описание номера')
 
group by requests.id
order by list.title
