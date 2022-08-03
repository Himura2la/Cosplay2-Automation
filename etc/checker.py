# -*- coding: utf-8 -*-

import os
import re
import csv
import unicodedata

csv_path = r"C:\Users\glago\YandexDisk\Fests\AtomCosCon 2022\AtomCosCon 22 - Заявки.csv"
id_row = '#'

folder_path = r"C:\Users\glago\YandexDisk\Fests\AtomCosCon 2022\Tracks"
id_regex_filename = r"^(?P<id>\d{3})"


def make_name(d):
    return to_filename(f"{d['#']}. {d['Начало']}. {d['Категория']}. {d['Название номера']}")


def to_filename(string):
    filename = string.replace('й', "<икраткое>")
    filename = unicodedata.normalize('NFD', filename).encode('cp1251', 'replace').decode('cp1251')
    filename = filename.replace("<икраткое>", 'й')
    filename = filename.replace(':', "")\
                       .replace('|', "-").replace('/', "-").replace('\\', "-")\
                       .replace('"', "'")\
                       .replace('’', "'")\
                       .replace(' ,', ", ")\
                       .replace('  ', " ")
    filename = ''.join(i if i not in "*?<>" else '' for i in filename)
    return filename

with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    head = reader.__next__()
    csv_data = {int(row[head.index(id_row)]):
                {head[i]: row[i].strip() for i in range(len(head))} for row in reader if row[head.index(id_row)]}

dir_data = dict()
for file_name in os.listdir(folder_path):
    dir_data[int(re.search(id_regex_filename, file_name).group("id"))] = file_name

for num, d in csv_data.items():
    if num not in dir_data.keys():
        print(f"[NO FILE for № {d['№']} ] {make_name(d)}")