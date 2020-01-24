SELECT DISTINCT
	card_code||' '||voting_number || '. ' || voting_title as num,
	text

FROM list, requests

LEFT JOIN ( 
	SELECT request_id as p_rid, replace(group_concat('### '||[values].title||':\n'||value||'\n'), '\n,', '\n') as text
	FROM [values]
	WHERE title = 'Оборудование и реквизит (необязательно)' OR title = 'Описание номера'
	group by request_id
)
ON p_rid = requests.id

WHERE
	list.id = topic_id
	AND	default_duration > 0
	AND	status = 'approved'
	AND card_code not in ('VC', 'V')

order by voting_number
