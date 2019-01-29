#!/usr/bin/python3
# -*- coding: utf-8 -*-

import csv
import os
import sqlite3
from yaml import load

card_code_order = ["DGJ",
                   "DSJ",
                   "KA",
                   "S",
                   "DGO",
                   "DU",
                   "DSW",
                   "DGW",
                   "DA",
                   "K",
                   "INS",
                   "DSO",
                   "T"]

config = load(
    open(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'config.yml'), 'r',
         encoding='utf-8').read())
db_path = config['db_path']
output_file = r"C:\Users\glago\Desktop\participants.csv"

fio_joins = """
LEFT JOIN ( SELECT request_section_id as ln_rsid, value as last_name
            FROM [values] WHERE title = 'Фамилия')
    ON ln_rsid = request_section_id
LEFT JOIN ( SELECT request_section_id as fn_rsid, value as first_name
            FROM [values] WHERE title = 'Имя')
    ON fn_rsid = request_section_id
LEFT JOIN ( SELECT request_section_id as mn_rsid, value as mid_name
            FROM [values] WHERE title = 'Отчество')
    ON mn_rsid = request_section_id
"""

where = """
list.id = topic_id AND requests.id = request_id
    AND status != 'disapproved'
    AND section_title in ('Ваши данные', 'Остальные участники')
    AND card_code in (""" + ",".join([f"'{c}'" for c in card_code_order]) + """)
"""


def fetch_dict(cursor):
    return [{col: row[i] for i, col in enumerate((description[0] for description in c.description))}
            for row in cursor.fetchall()]


def get_numbers(cursor, fio):
    r = """
SELECT DISTINCT list.card_code, voting_number, voting_title
FROM list, requests, [values]
""" + fio_joins + """
WHERE """ + where + """
      AND last_name=? AND first_name=? AND mid_name=?
"""
    cursor.execute(r, fio)
    return [f"{s['card_code']} {s['voting_number']}"
            for s in sorted(fetch_dict(cursor), key=lambda s: card_code_order.index(s['card_code']))]


with sqlite3.connect(db_path, isolation_level=None) as db:
    c = db.cursor()
    c.execute('PRAGMA encoding = "UTF-8"')
    q = """
SELECT DISTINCT
    group_concat(distinct nick) as nick, city,
    group_concat(distinct phone) as phone,
    last_name, first_name, mid_name
FROM list, requests, [values]
""" + fio_joins + """
LEFT JOIN ( SELECT request_section_id as сt_rsid, value as city
            FROM [values] WHERE title = 'Город')
    ON сt_rsid = request_section_id
LEFT JOIN ( SELECT request_section_id as n_rsid, value as nick
            FROM [values] WHERE title LIKE 'Ник%')
    ON n_rsid = request_section_id
LEFT JOIN ( SELECT request_section_id as r_rsid, value as phone
            FROM [values] WHERE title LIKE 'Мобильный телефон%')
    ON r_rsid = request_section_id
WHERE """ + where + """
GROUP BY last_name, first_name, mid_name
"""
    c.execute(q)
    header = [description[0] for description in c.description] + ["nums"]
    rows = [list(p.values()) +
            get_numbers(c, (p['last_name'], p['first_name'], p['mid_name']))
            for p in fetch_dict(c)]

with open(output_file, 'w', newline='', encoding='utf=8') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(rows)
