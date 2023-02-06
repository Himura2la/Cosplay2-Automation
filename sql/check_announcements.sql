SELECT '## ' || card_code || ' ' || voting_number || '. ' || list.title as num,
		voting_title, announcement_title

FROM list, requests

WHERE
	list.id = topic_id
	AND	status in ('approved')
	AND default_duration > 0

ORDER BY voting_number
