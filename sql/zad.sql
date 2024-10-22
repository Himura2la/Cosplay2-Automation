SELECT
    number as '№',
    card_code ||' '|| voting_number as num,
    ifnull(list.title||' / '||nom, list.title) as nom,

    CASE ifnull(length(team),0)
        WHEN 0 THEN nicks
        ELSE IIF(card_code LIKE 'D%', 'Косбэнд ', 'Команда ')||team||IIF(studio IS NULL, '', ' ('||studio||')')||': '||nicks
    END as 'Участник',


    value1
	||
    IIF(value2 IS NULL, '', ' - '||value2)
	||
	IIF(value3 IS NULL, '', ' - '||value3) as 'title',
	
    voting_title

FROM list, requests

LEFT JOIN (	SELECT request_id as nc_rid, REPLACE(GROUP_CONCAT(DISTINCT value), ',', ', ') as nicks
            FROM [values]
            WHERE title LIKE 'Ник%'
              AND section_title NOT LIKE 'Помощник%'
            GROUP BY request_id)
    ON nc_rid = requests.id

LEFT JOIN (	SELECT request_id as ct_rid, REPLACE(GROUP_CONCAT(DISTINCT value), ',', ', ') as cities
            FROM [values]
            WHERE title = 'Город'
              AND section_title NOT LIKE 'Помощник%'
            GROUP BY request_id)
    ON ct_rid = requests.id

LEFT JOIN (	SELECT request_id as n_rid, value as nom FROM [values]
            WHERE title = 'Подноминация')
    ON n_rid = requests.id

LEFT JOIN (	SELECT request_id as f_rid, value as value1 FROM [values]
            WHERE title LIKE 'Фэндом%'
               OR title LIKE 'Исполнитель%')
    ON f_rid = requests.id

LEFT JOIN (	SELECT request_id as ch_rid, REPLACE(GROUP_CONCAT(DISTINCT value), ',', ', ') as value2 FROM [values]
            WHERE (title in ('Имя персонажа','Персонаж','OST (необязательно)'))
              AND section_title NOT LIKE 'Изображени%'
              AND section_title NOT LIKE 'Фотографии%'
            GROUP BY request_id)
    ON ch_rid = requests.id


LEFT JOIN (	SELECT request_id as ti_rid, REPLACE(GROUP_CONCAT(DISTINCT value), ',', ', ') as value3 FROM [values] 
            WHERE title LIKE 'Название%'
              AND title NOT LIKE '%косб%'
              AND title NOT LIKE '%команд%'
            GROUP BY request_id)
    ON ti_rid = requests.id


LEFT JOIN (	SELECT request_id as tm_rid, value as team FROM [values]
            WHERE	title LIKE 'Название косб%' OR
                    title LIKE '%команд%' )
    ON tm_rid = requests.id

LEFT JOIN (	SELECT request_id as ds_rid, value as studio FROM [values]
            WHERE	title LIKE 'Танцевальная студия%')
    ON ds_rid = requests.id

WHERE
    list.id = topic_id
    AND status != 'disapproved'
    AND (default_duration > 0 OR card_code IN ('AGR', 'V', 'VC'))

GROUP BY voting_number
ORDER BY voting_number
