# -*- coding: utf-8 -*-

import os
import re
import csv
import unicodedata

csv_path = r"C:\Users\himura\Desktop\AtomCosCon 21 - Заявки.csv"
id_row = 'id'

folder_paths = [r"D:\Events\Атом 2021\Files"]
id_regex_filename = r"^(?P<id>\d{3})"

no_op = bool(0)


def make_name(d, r_id):
    return f"{d['num']}. {d['start']}. {d['name']}"


with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    head = reader.__next__()
    data = {row[head.index(id_row)]:
                {head[i]: row[i].strip() for i in range(len(head)) if i != head.index(id_row)} for row in reader}


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
    for file_name in os.listdir(folder_path):
        if not os.path.isfile(os.path.join(folder_path, file_name)):
            continue
        name, ext = file_name.rsplit('.', 1)
        ext = '.' + ext
        try:
            r_id = re.search(id_regex_filename, name).group("id")
            name_data = data[r_id]
        except KeyError:
            print('[NOT FOUND IN CSV]', file_name)
            continue
        except AttributeError:
            print('[DOES NOT MATCH]', file_name)
            continue

        name = to_filename(make_name(name_data, r_id))

        src = os.path.join(folder_path, file_name)
        dst = os.path.join(folder_path, name + ext)
        if src != dst:
            print(src + " -> \n" + dst + '\n')
            if not no_op:
                try:
                    os.rename(src, dst)
                except Exception as e:
                    print("FAILED TO RENAME:", e)
        processed_nums.add(r_id)

    lost_files = set(data.keys()) - processed_nums
    for r_id in lost_files:
        print('[NO FILE]%s: %s' % (r_id, make_name(data[r_id], r_id)))
