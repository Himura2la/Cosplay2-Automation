#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import csv
import sqlite3
from yaml import load

num_row = 'num'
voting_number_row = 'voting_number'

config = load(open('config.yml', 'r', encoding='utf-8').read())
db_path = config['db_path']
numberer_table = config['numberer_table_path']

with sqlite3.connect(db_path, isolation_level=None) as db:
    c = db.cursor()
    c.execute('PRAGMA encoding = "UTF-8"')
    c.execute('SELECT number, id FROM requests')
    request_ids = {num: r_id for num, r_id in c.fetchall()}

with open(numberer_table, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    head = reader.__next__()
    voting_numbers = {int(row[head.index(num_row)]): int(row[head.index(voting_number_row)]) for row in reader}


def set_number(request_id, voting_number):
    print(request_id, '->', voting_number)


for num, v_num in voting_numbers.items():
    r_id = request_ids[num]
    set_number(r_id, v_num)

