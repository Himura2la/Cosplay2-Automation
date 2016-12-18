DROP TABLE IF EXISTS persons;
DROP TABLE IF EXISTS nicks; 
DROP TABLE IF EXISTS cities; 
DROP TABLE IF EXISTS f_names; 
DROP TABLE IF EXISTS l_names; 
DROP TABLE IF EXISTS m_names; 

CREATE TEMP TABLE nicks AS SELECT request_section_id AS id, value AS nick FROM 'values' WHERE title = 'Ник';
CREATE TEMP TABLE cities AS SELECT request_section_id AS id, value AS city FROM 'values' WHERE title = 'Город';
CREATE TEMP TABLE f_names AS SELECT request_section_id AS id, value FROM 'values' WHERE title = 'Имя';
CREATE TEMP TABLE l_names AS SELECT request_section_id AS id, value FROM 'values' WHERE title = 'Фамилия';
CREATE TEMP TABLE m_names AS SELECT request_section_id AS id, value FROM 'values' WHERE title = 'Отчество';

CREATE TEMP table persons as 
    SELECT 
		f_names.id, nick, 
		l_names.value as l_name, 
		f_names.value as f_name, 
		m_names.value as m_name, 
		city 
    FROM nicks, cities, f_names, l_names, m_names
    WHERE f_names.id = l_names.id and f_names.id = cities.id and f_names.id = nicks.id and f_names.id = m_names.id;

DROP TABLE nicks; DROP TABLE cities; DROP TABLE f_names; DROP TABLE l_names; DROP TABLE m_names; 

SELECT DISTINCT l_name, f_name, m_name, value FROM persons, [values], requests
WHERE request_section_id = persons.id AND
requests.id = request_id AND
[values].title = 'Номер группы ТулГУ (необязательно)' AND
status = 'approved'