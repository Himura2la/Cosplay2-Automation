# -*- coding: utf-8 -*-

import csv

csv_path = r"/home/himura/Documents/acc21-data.csv"
id_row = "Номер"

with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    head = reader.__next__()
    d = {row[head.index(id_row)]:
                {head[i]: row[i].strip() for i in range(len(head)) if i != head.index(id_row)} for row in reader}

def p(t):
    return t.replace('\n', '\n\n')

print('# Волонтёрам\n\n')

for i in d:
    print(f"### {i}. [{d[i]['Начало']}] {d[i]['Категория']}: {d[i]['Название']}\n{p(d[i]['Помощь волонтёров'])}\n\n")


print('# Светосценарии\n\n')

for i in d:
    print(f"### {i}. [{d[i]['Начало']}] {d[i]['Категория']}: {d[i]['Название']}\n{p(d[i]['Светосценарий'])}\n\n")