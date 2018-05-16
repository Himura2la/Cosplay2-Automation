select list.title, number || '. ' || voting_title, *
from requests, list, [values]
where 	topic_id = list.id and
		card_code in ('ART', 'FC') and
		status = 'approved' and
		request_id = requests.id and
		[values].title = 'Участие в конкурсе' and
		[values].value = 'В конкурсе'