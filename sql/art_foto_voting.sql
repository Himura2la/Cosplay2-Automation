SELECT DISTINCT
	COALESCE(
		REPLACE(REPLACE(sub_nom, 'Традиционный ', ''), 'Digital ', ''),
		list.title
	) AS nom,
	card_code AS nom_code,
	[number] AS '№', 
	'=HYPERLINK("https://tulafest.cosplay2.ru/cards/card/'||requests.id||'"; "'||REPLACE(IFNULL(voting_title,'[Заявка без названия]'),'"',"'")||'")' AS "Заявка"

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

ORDER BY nom
