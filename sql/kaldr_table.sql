
SELECT DISTINCT
	list.title as 'Раздел',
	number as 'Заявка №',
	card_code ||' '|| voting_number as 'Номер',
    fandom as 'Фэндом',
	duration as "Длительность (мин)",

    group_concat(distinct nick) as 'Ники',
	group_concat(distinct read_nick) as  'Транскрипции ников',
    ifnull(group_concat(distinct chars), single_char) as 'Персонажи',
    group_concat(distinct last_name||' '||first_name||' '||mid_name) as 'ФИО (+помощники)',
	group_concat(distinct city) as 'Города',
	group_concat(distinct team)||ifnull(' ['||read_team||']','') as 'Косбэнд',
	
	details,
	light,
	stuff
	
	

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
            FROM [values] WHERE title = 'Город' AND section_title NOT LIKE 'Помощник%')
    ON сt_rsid = request_section_id
LEFT JOIN ( SELECT request_section_id as n_rsid, value as nick
            FROM [values] WHERE title LIKE 'Ник%' AND section_title NOT LIKE 'Помощник%')
    ON n_rsid = request_section_id
LEFT JOIN ( SELECT request_section_id as rn_rsid, value as read_nick
            FROM [values] WHERE title LIKE 'Транскрипция ника%')
    ON rn_rsid = request_section_id
LEFT JOIN ( SELECT request_id as rt_rid, value as read_team
            FROM [values] WHERE title LIKE 'Транскрипция названия косбэнда%')
    ON rt_rid = request_id
LEFT JOIN ( SELECT request_section_id as ch_rsid, value as chars
            FROM [values] WHERE title = 'Имя персонажа' OR title = 'Откуда персонаж')
    ON ch_rsid = request_section_id
LEFT JOIN ( SELECT request_id as ch_rid, value as single_char
            FROM [values] WHERE title = 'Имя персонажа')
    ON ch_rid = request_id
LEFT JOIN ( SELECT request_id as fn_rid, value as fandom
            FROM [values] WHERE title LIKE 'Фэндом%')
    ON fn_rid = request_id
LEFT JOIN (	SELECT request_id as tm_rid, value as team FROM [values]
            WHERE	title LIKE 'Название косб%' OR
                    title LIKE '%команд%' )
    ON tm_rid = requests.id
LEFT JOIN ( SELECT request_id as t_rid, value as duration
			FROM [values] 
			WHERE title LIKE 'Продолжительность%')
	ON t_rid = requests.id

LEFT JOIN ( SELECT request_id as dsc_rid, value as details
            FROM [values] WHERE title = 'Описание номера')
    ON dsc_rid = request_id
LEFT JOIN ( SELECT request_id as lgt_rid, value as light
            FROM [values] WHERE title = 'Пожелания по сценическому свету (необязательно)')
    ON lgt_rid = request_id
LEFT JOIN ( SELECT request_id as stf_rid, value as stuff
            FROM [values] WHERE title = 'Оборудование и реквизит (необязательно)')
    ON stf_rid = request_id


	
WHERE
    list.id = topic_id AND requests.id = request_id
    AND status != 'disapproved'
    AND [values].title = 'Имя'  -- use sections with name
	AND default_duration > 0

GROUP BY list.title, number
ORDER BY voting_number
