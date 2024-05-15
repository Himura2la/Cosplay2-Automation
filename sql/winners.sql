SELECT DISTINCT win_title || ': ' || card_code ||' '|| voting_number ||'. '|| voting_title

FROM list, requests

WHERE
	list.id = topic_id
	AND	status in ('approved')
	AND win > 0

ORDER BY default_duration, win_title