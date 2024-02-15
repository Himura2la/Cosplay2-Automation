# -*- coding: utf-8 -*-

import os
import re
import csv
import shutil
import unicodedata

csv_path = r"C:\Users\glago\Desktop\ToFu Market 18.02 - Программа.csv"
id_row = '№'

folder_paths = [r"C:\Users\glago\YandexDisk\Fests\ToFu\ToFu Market 5\Tracks"]
target_dir = r"C:\Events\tf5\Fest"
id_regex_filename = r"^(?P<id>\d{1,3})"
errors = ""

no_op = bool(1)


def make_name(d, r_id):
    return f"{d['# Вид выступления. Название номера']} (№{r_id})"


with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    head = reader.__next__()
    data = {row[head.index(id_row)]:
                {head[i]: row[i].strip() for i in range(len(head)) if i != head.index(id_row)} for row in reader if row[head.index(id_row)]}


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


for folder_path in folder_paths:
    processed_nums = set()
    print("\n" + folder_path + ":")
    for dir_name in os.listdir(folder_path):
        try:
            r_id = str(int(re.search(id_regex_filename, dir_name).group("id")))
            name_data = data[r_id]
        except KeyError:
            errors += f"\n[NOT FOUND IN CSV] {dir_name}"
            continue
        except AttributeError:
            errors += f"\n[DOES NOT MATCH] {dir_name}"
            continue

        new_name = to_filename(make_name(name_data, r_id))

        for file_name in os.listdir(os.path.join(folder_path, dir_name)):
            name, ext = file_name.rsplit('.', 1)
            ext = '.' + ext
            src = os.path.join(folder_path, dir_name, file_name)
            dst = os.path.join(target_dir, new_name + ext.lower())
            if src != dst:
                print(src + " -> \n" + dst + '\n')
                processed_nums.add(r_id)
                if not no_op:
                    try:
                        shutil.copy(src, dst)
                    except Exception as e:
                        print("FAILED TO RENAME:", e)

    print(errors)
    lost_files = set(data.keys()) - processed_nums
    for r_id in lost_files:
        print('[NO FILE]%s: %s' % (r_id, make_name(data[r_id], r_id)))


