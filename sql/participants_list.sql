
SELECT DISTINCT
    group_concat(distinct status),
    group_concat(distinct nick) as 'Ник',
    first_name,
	team,
    group_concat(distinct phone) as 'Telegram',
	group_concat(distinct '№ '|| number) as 'Заявки',
	group_concat(distinct list.title) as 'Разделы', group_concat(distinct section_title) as 'Секции',
    group_concat(distinct fandom) as 'Фэндомы',
    ifnull(group_concat(distinct chars), single_char) as 'Персонажи'

FROM list, requests, [values]

LEFT JOIN ( SELECT request_section_id as fn_rsid, value as first_name
            FROM [values] WHERE title = 'Имя')
    ON fn_rsid = request_section_id
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
            FROM [values] WHERE title LIKE 'Название%' AND section_title = 'Общая информация')
    ON fn_rid = request_id
LEFT JOIN ( SELECT request_id as t_rid, value as team
            FROM [values] WHERE title LIKE '%команд%' OR title LIKE '%косбэнд%')
    ON t_rid = request_id
LEFT JOIN ( SELECT request_section_id as r_rsid, value as phone
            FROM [values] WHERE title = 'Telegram')
    ON r_rsid = request_section_id

WHERE
    list.id = topic_id AND requests.id = request_id
    AND status != 'disapproved'
    AND [values].title = 'Имя'  -- use sections with name

GROUP BY nick, first_name

