# -*- coding: utf-8 -*-

import os
import csv
import sqlite3


csv_path = r"C:\Users\glago\Desktop\Announcement_blank.csv"
db_path = r"D:\Clouds\YandexDisk\Fests\Yuki no Odori 7\db\tulafest\sqlite3_data.db"
out_file = r"C:\Users\glago\Desktop\check.txt"


with open(csv_path, 'r', encoding='utf-8') as f:
    data = csv.reader(f)
    rows = [[cell for cell in row] for row in data]

print('Connecting to ' + os.path.abspath(db_path) + '...')

db = sqlite3.connect(db_path, isolation_level=None)
c = db.cursor()
c.execute('PRAGMA encoding = "UTF-8"')

c.execute("""
SELECT
    requests.number as "№",
    voting_title as "Название карточки",
	--card_code ||' '|| voting_number as num,
	IFNULL(list.title||' / '||nom, list.title) as nom,
	nicks,
	team,
	fandom,
	cahrs,
	IFNULL(item_title, s_artist||' - '||s_title||IFNULL(' (OST '||s_ost||')', '')) as title,
	cities

FROM list, requests

LEFT JOIN (	SELECT request_id as nc_rid, REPLACE(GROUP_CONCAT(DISTINCT value), ',', ', ') as nicks
			FROM [values]
				LEFT JOIN (SELECT request_section_id as r_rsid, value as [role] FROM [values] WHERE title = 'Роль') 
				ON r_rsid = request_section_id
			WHERE title LIKE 'Ник%' AND ([role] = 'Участник' OR [role] IS NULL)
			GROUP BY request_id)
	ON nc_rid = requests.id

LEFT JOIN (	SELECT request_id as ct_rid, REPLACE(GROUP_CONCAT(DISTINCT value), ',', ', ') as cities
			FROM [values]
				LEFT JOIN (SELECT request_section_id as r_rsid, value as [role] FROM [values] WHERE title = 'Роль') 
				ON r_rsid = request_section_id
			WHERE title = 'Город' AND ([role] = 'Участник' OR [role] IS NULL)
			GROUP BY request_id)
	ON ct_rid = requests.id
				
LEFT JOIN (	SELECT request_id as n_rid, value as nom FROM [values] 
			WHERE title = 'Подноминация')
	ON n_rid = requests.id
				 
LEFT JOIN (	SELECT request_id as f_rid, value as fandom FROM [values] 
			WHERE title LIKE 'Фэндом%')
	ON f_rid = requests.id

LEFT JOIN (	SELECT request_id as ch_rid, REPLACE(GROUP_CONCAT(DISTINCT value), ',', ', ') as cahrs FROM [values]
			WHERE (title = 'Имя персонажа' OR title = 'Персонаж') AND section_title NOT LIKE "Изображени%"
			GROUP BY request_id)
	ON ch_rid = requests.id

LEFT JOIN (	SELECT request_id as a_rid, value as s_artist FROM [values] 
			WHERE title LIKE 'Исполнитель композиции%')
	ON a_rid = requests.id

LEFT JOIN (	SELECT request_id as t_rid, value as s_title FROM [values] 
			WHERE title = 'Название композиции')
	ON t_rid = requests.id

LEFT JOIN (	SELECT request_id as o_rid, value as s_ost FROM [values] 
			WHERE title = 'OST (необязательно)')
	ON o_rid = requests.id

LEFT JOIN (	SELECT request_id as tm_rid, value as team FROM [values] 
			WHERE	title LIKE 'Название косб%' OR
					title = 'Команда (необязательно)' OR
					title = 'Название команды (необязательно)')
	ON tm_rid = requests.id

LEFT JOIN (	SELECT request_id as it_rid, value as item_title FROM [values] 
			WHERE	title = 'Название номера (необязательно)' OR
					title = 'Название работы' OR
					title = 'Название сценки')
	ON it_rid = requests.id


WHERE
	list.id = topic_id
	AND status != 'disapproved'
	AND default_duration > 0

GROUP BY voting_number
ORDER BY voting_number
""")

def check_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return None

announcements = {int(rows[i][0]): rows[i][2] for i in range(len(rows)) if check_int(rows[i][0])}

headers = [description[0] for description in c.description]
result_txt = ""

for record in c.fetchall():
    
    for i, field in enumerate(headers):
        result_txt += "%s: %s%s" % (field, record[i], os.linesep) if record[i] else ""
        if i == 1:
            result_txt += "Объявление: %s%s" % (announcements[record[headers.index('№')]], os.linesep)
    result_txt += os.linesep

print(result_txt)
open(out_file, 'w', encoding='utf-8').write(result_txt)