#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Himura Kazuto <himura@tulafest.ru>


import os
import sqlite3
import sys
import csv
from yaml import load

root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
config = load(open(os.path.join(root, 'config.yml'), 'r', encoding='utf-8').read())

technical_plan_csv = f"{os.environ['USERPROFILE']}\\Desktop\\technical_plan.csv" if len(sys.argv) < 2 else sys.argv[1]
out_dir = os.path.split(technical_plan_csv)[0]

with open(technical_plan_csv, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    head = reader.__next__()
    csv_data = [[row[i].strip() for i in range(len(head))] for row in reader]


db = sqlite3.connect(config['db_path'], isolation_level=None)
c = db.cursor()
c.execute('PRAGMA encoding = "UTF-8"')
c.execute(open(os.path.join(root, 'sql', 'задники.sql'), 'r', encoding='utf-8').read())
header = [d[0] for d in c.description]
db_data = [{header[i]: val for i, val in enumerate(row)} for row in c.fetchall()]


for row in csv_data:
    num = f"{row[head.index('code')]} {row[head.index('num')]}".strip()
    if not num:
        continue
    title = row[head.index('voting_title')]
    try:
        cities = filter(lambda d: d['num'] == num, db_data).__next__()['cities']
    except StopIteration:
        print(f'[ERROR] {num} not found in DB !!!')
        continue
    row[head.index('voting_title')] += f' - {cities}'

with open(os.path.join(out_dir, 'technical_plan-supplemented.csv'), 'w', newline='', encoding='utf=8') as f:
    writer = csv.writer(f)
    writer.writerow(head)
    writer.writerows(csv_data)

human_plan = ''
for row in csv_data:
    info, time, code, num, voting_title = row
    if info:  # Доп. инфа
        human_plan += f'\n{time}\t{info}\n'
    else:  # Номер
        human_plan += f"{time}\t\t{code} {num}. {voting_title}\n"
open(os.path.join(out_dir, 'human_plan-supplemented.txt'), 'w', encoding='utf-8').write(human_plan)
