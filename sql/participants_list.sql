
SELECT DISTINCT
	'' as 'Тут',
    group_concat(distinct nick) as 'Ник',
	'' as 'Роль',
	'' as 'Гримёрка',
    last_name, first_name, mid_name, city,
    ''''||group_concat(distinct phone) as 'Телефон',
	group_concat(distinct list.title) as 'Разделы', group_concat(distinct section_title) as 'Секции',
    group_concat(distinct fandom) as 'Фэндомы',
    ifnull(group_concat(distinct chars), single_char) as 'Персонажи',
	IIF(sum(default_duration) > 0, '1', '') as 'Участвует в программе',
	group_concat(distinct '№ '|| number) as 'Заявки',
	group_concat(distinct card_code ||' '|| voting_number) as 'Номера'

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
LEFT JOIN ( SELECT request_section_id as n_rsid, value as nick
            FROM [values] WHERE title LIKE 'Ник%')
    ON n_rsid = request_section_id
LEFT JOIN ( SELECT request_section_id as ch_rsid, value as chars
            FROM [values] WHERE title = 'Имя персонажа' OR title = 'Откуда персонаж')
    ON ch_rsid = request_section_id
LEFT JOIN ( SELECT request_id as ch_rid, value as single_char
            FROM [values] WHERE title = 'Имя персонажа')
    ON ch_rid = request_id
LEFT JOIN ( SELECT request_id as fn_rid, value as fandom
            FROM [values] WHERE title LIKE 'Фэндом%')
    ON fn_rid = request_id
LEFT JOIN ( SELECT request_section_id as r_rsid, value as phone
            FROM [values] WHERE title LIKE 'Мобильный телефон%')
    ON r_rsid = request_section_id

WHERE
    list.id = topic_id AND requests.id = request_id
    AND status != 'disapproved'
    AND [values].title = 'Имя'  -- use sections with name
	AND NOT (list.card_code in ('ART', 'FC', 'MEM', 'V', 'VC'))
--	AND default_duration > 0

GROUP BY last_name, first_name, mid_name, city
ORDER BY last_name
