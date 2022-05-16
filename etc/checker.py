# -*- coding: utf-8 -*-

import os
import re
import csv

csv_path = r"C:\Users\glago\Desktop\AtomCosCon 22 - Заявки.csv"
id_row = '№'

folder_path = r"C:\Temp\AtomCosCon 2022\Files"
id_regex_filename = r"^(?P<id>\d{3})"


with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    head = reader.__next__()
    csv_data = {int(row[head.index(id_row)]):
                {head[i]: row[i].strip() for i in range(len(head)) if i != head.index(id_row)} for row in reader}

dir_data = dict()
for file_name in os.listdir(folder_path):
    dir_data[int(re.search(id_regex_filename, file_name).group("id"))] = file_name

for num, d in csv_data.items():
    if num not in dir_data.keys():
        print(f"[NO FILE] {num}. {d['Название номера']}")