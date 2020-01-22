SELECT 
[number],
list.title,
voting_title,
replace(group_concat('### '||[values].title||':\n'||value||'\n'), '\n,', '\n') as text

FROM
list, requests, [values]

WHERE
requests.id = request_id AND
list.id = topic_id AND
default_duration > 0 AND
status != 'disapproved' AND
[values].value != '' AND
([values].title = 'Описание номера' OR
 [values].title = 'Пожелания по сценическому свету (необязательно)')
 
group by requests.id
order by voting_number
