
SELECT DISTINCT
	list.title,
	card_code ||' '|| voting_number as code,
	'=HYPERLINK("http://tulafest.cosplay2.ru/orgs/requests/request/'||requests.id||'", "'||REPLACE(IFNULL(voting_title,'[Заявка без названия]'),'"',"'")||'")' as "Заявка",
    count(DISTINCT last_name || first_name || mid_name || city) as "Тел"
FROM list, requests, [values]

LEFT JOIN ( SELECT request_section_id as ln_rsid, value as last_name
            FROM [values] WHERE title = 'Фамилия')
    ON ln_rsid = request_section_id
LEFT JOIN ( SELECT request_section_id as fn_rsid, value as first_name
            FROM [values] WHERE title = 'Имя')
    ON fn_rsid = request_section_id
LEFT JOIN ( SELECT request_section_id as mn_rsid, value as mid_name
            FROM [values] WHERE title = 'Отчество')
    ON mn_rsid = request_section_id
LEFT JOIN ( SELECT request_section_id as сt_rsid, value as city
            FROM [values] WHERE title = 'Город')
    ON сt_rsid = request_section_id

WHERE 
list.id = topic_id AND requests.id = request_id
    AND status != 'disapproved'
    AND section_title in ('Ваши данные', 'Остальные участники', 'Другие косплееры (необязательно)', 'Соавторы (необязательно)')
    and (default_duration > 0 or card_code in ('V','VC','ART','FC'))


GROUP BY requests.id
order by default_duration DESC, code
