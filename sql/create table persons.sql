CREATE TEMP TABLE nicks AS SELECT request_section_id AS id, value AS nick FROM 'values' WHERE title = 'Ник';
CREATE TEMP TABLE cities AS SELECT request_section_id AS id, value AS city FROM 'values' WHERE title = 'Город';
CREATE TEMP TABLE f_names AS SELECT request_section_id AS id, value FROM 'values' WHERE title = 'Имя';
CREATE TEMP TABLE l_names AS SELECT request_section_id AS id, value FROM 'values' WHERE title = 'Фамилия';

CREATE table persons as 
    SELECT f_names.id, nick, f_names.value as f_name, l_names.value as l_name, city 
    FROM nicks, cities, f_names, l_names 
    WHERE f_names.id = l_names.id and f_names.id = cities.id and f_names.id = nicks.id;

DROP TABLE nicks; DROP TABLE cities; DROP TABLE f_names; DROP TABLE l_names;