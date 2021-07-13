SELECT DISTINCT
	card_code||' '||voting_number||'. '||voting_title||' (№ '||requests.number||')' as num,
	replace(text,' (необязательно)','') as text

FROM list, requests

LEFT JOIN ( 
	SELECT request_id as p_rid, replace(group_concat('### '||[values].title||':\n'||value||'\n'), '\n,', '\n') as text
	FROM [values]
	WHERE title in (
		'Описание номера'
		,'Начало выступления'
		,'Оборудование и реквизит (необязательно)', 'Пожелания к организаторам'
--		,'Пожелания по сценическому свету (необязательно)'
	)
	group by request_id
)
ON p_rid = requests.id

WHERE
	list.id = topic_id
	AND	default_duration > 0
	AND	status = 'approved'
	AND card_code not in ('VC', 'V')

order by voting_number
