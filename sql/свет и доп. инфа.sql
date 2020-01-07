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
status = 'approved' AND
[values].value != '' AND
([values].title = 'Пожелания к организаторам' OR
 [values].title = 'Описание')
 
group by requests.id
order by voting_number
