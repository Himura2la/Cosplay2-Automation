SELECT 
card_code, voting_number ,
'=HYPERLINK("https://main.datakeep.ru/event/media/'||voting_number||'.jpg"; "'||REPLACE(IFNULL(voting_title,'[Заявка без названия]'),'"',"'")||'")' AS "Заявка"

FROM requests, list, [values]

LEFT JOIN (
	SELECT request_id AS comp_rid, value AS competition
	FROM [values] 
	WHERE title = 'Участие в конкурсе'
) ON comp_rid = request_id

WHERE
list.id = topic_id AND
requests.id = request_id AND
status = 'approved' AND
default_duration > 0 AND
competition = 'В конкурсе'

GROUP BY voting_number
ORDER BY voting_number