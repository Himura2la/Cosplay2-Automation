SELECT DISTINCT
    card_code||' '||voting_number||'. '||voting_title||' (№ '||requests.number||')' as num,
    text

FROM list, requests

LEFT JOIN (
    SELECT
        request_id,
        group_concat(
            '### ' || replace(title,' (необязательно)','') || x'0a' || value || x'0a',
            x'0a'
        ) as text
    FROM (
        SELECT request_id, [values].title, value
        FROM [values]
        WHERE title in (
            'Описание номера'
            ,'Начало выступления'
    --		,'Оборудование и реквизит (необязательно)', 'Пожелания к организаторам'
            ,'Пожелания по сценическому свету (необязательно)'
        )
        ORDER BY CASE title
            WHEN 'Начало выступления' THEN 0
            WHEN 'Оборудование и реквизит (необязательно)' THEN 1
            WHEN 'Пожелания к организаторам' THEN 2
            WHEN 'Описание номера' THEN 10
        END
    )
    GROUP BY request_id
) AS texts
  ON texts.request_id = requests.id

WHERE
    list.id = topic_id
    AND	default_duration > 0
    AND	status = 'approved'
    AND card_code not in ('VC', 'V')

ORDER BY voting_number



