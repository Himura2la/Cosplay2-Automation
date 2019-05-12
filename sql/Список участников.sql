
SELECT DISTINCT
    group_concat(distinct nick) as nick, city,
    group_concat(distinct phone) as phone,
    last_name, first_name, mid_name
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
LEFT JOIN ( SELECT request_section_id as r_rsid, value as phone
            FROM [values] WHERE title LIKE 'Мобильный телефон%')
    ON r_rsid = request_section_id
WHERE 
list.id = topic_id AND requests.id = request_id
    AND status != 'disapproved'
    AND section_title in ('Ваши данные', 'Остальные участники')
    AND card_code in ('ART','AA','SY','VOL','MM')

GROUP BY last_name, first_name, mid_name
