SELECT 
requests.number,
list.title,
--card_code||' '||voting_number,
voting_title,
replace(group_concat('### '||[values].title||':\n'||value||'\n'), '\n,', '\n') as value

FROM
list, requests, [values]

WHERE
requests.id = request_id AND
list.id = topic_id AND
status = 'approved' AND
[values].value != '' AND
([values].title = 'Пожелания к организаторам' OR
 [values].title LIKE '%ценарий%' OR
 [values].title = 'Текст о выступлении')
 
group by requests.id
order by list.title