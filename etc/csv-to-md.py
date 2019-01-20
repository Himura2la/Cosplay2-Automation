# -*- coding: utf-8 -*-

import csv

id_row = 'number'
csv_path = r'/home/himura/Downloads/announcements.csv'

with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=';')
    head = reader.__next__()
    data = {row[head.index(id_row)]:
                {head[i]: row[i].strip() for i in range(len(head)) if i != head.index(id_row)} for row in reader}

for i, d in data.items():
    r = f"\n{d['card_code']} {i}\n{d['voting_title']}\n{d['announcement_title']}"
    print(r)
