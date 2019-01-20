SELECT number, card_code, title, voting_title, announcement_title

FROM list, requests

WHERE
	list.id = topic_id
	AND	status in ('approved')
	AND default_duration > 0

