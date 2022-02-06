SELECT DISTINCT
	list.title AS 'Номинация',
	card_code AS 'Код',
	[number] AS '№', 
	'=HYPERLINK("http://tulafest.cosplay2.ru/orgs/requests/request/'||requests.id||'"; "'||REPLACE(IFNULL(voting_title,'[Заявка без названия]'),'"',"'")||'")' AS "Заявка",
	sub_nom AS 'Подноминация'

FROM requests, list, [values]

LEFT JOIN (
	SELECT request_id AS sn_rid, value AS sub_nom
	FROM [values] 
	WHERE title = 'Номинация'
) ON sn_rid = request_id

LEFT JOIN (
	SELECT request_id AS comp_rid, value AS competition
	FROM [values] 
	WHERE title = 'Участие в конкурсе'
) ON comp_rid = request_id

WHERE topic_id = list.id AND
	  request_id = requests.id AND
	  card_code in ('ART', 'FC', 'V', 'VC') AND
	  [status] = 'approved' AND
	  competition = 'В конкурсе'
--order by list.title, voting_title
ORDER BY list.title, sub_nom, [number]
