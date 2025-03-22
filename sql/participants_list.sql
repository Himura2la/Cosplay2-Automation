
SELECT DISTINCT
--    group_concat(distinct status),
    nick,
    first_name,
	group_concat(distinct team) as team,
	group_concat(distinct card_code||' '||voting_number) as 'Номера',
    group_concat(distinct tg)||IFNULL(','||group_concat(distinct phone),'') as 'Telegram',
	group_concat(distinct '№ '|| number) as 'Заявки',
	group_concat(distinct list.title) as 'Разделы',
--	group_concat(distinct section_title) as 'Секции',
    
    ifnull(group_concat(distinct fandom), '')||coalesce(' - '||group_concat(distinct chars), single_char, '') as 'Косплей'

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
            FROM [values] WHERE title LIKE 'Фэндом%')
    ON fn_rid = request_id
LEFT JOIN ( SELECT request_id as t_rid, value as team
            FROM [values] WHERE (title LIKE '%студия%' OR title LIKE '%команд%' OR title LIKE '%косбэнд%') and title NOT LIKE '%ранскрипция%')
    ON t_rid = request_id
LEFT JOIN ( SELECT request_section_id as r_rsid, value as phone
            FROM [values] WHERE title = 'Мобильный телефон')
    ON r_rsid = request_section_id
LEFT JOIN ( SELECT request_section_id as tg_rsid, value as tg
            FROM [values] WHERE title = 'Telegram')
    ON tg_rsid = request_section_id
	
WHERE
    list.id = topic_id AND requests.id = request_id
    AND status != 'disapproved'
    AND [values].title IN ('Имя','Ник')  -- use sections with name
	AND card_code NOT IN ('FC')

GROUP BY first_name, nick
ORDER BY default_duration > 0 DESC, card_code, team, first_name
