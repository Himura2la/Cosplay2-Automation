select list.title as 'Номинация',
		card_code as 'Код',
		number as '№', 
		'=HYPERLINK("http://tulafest.cosplay2.ru/orgs/requests/request/'||requests.id||'", "'||REPLACE(IFNULL(voting_title,'[Заявка без названия]'),'"',"'")||'")' as "Заявка"

from requests, list, [values]
where 	topic_id = list.id and
		card_code in ('ART', 'FC', 'V', 'VC') and
		status = 'approved' and
		request_id = requests.id and
		[values].title = 'Участие в конкурсе' and
		[values].value = 'В конкурсе'
order by list.title, voting_title