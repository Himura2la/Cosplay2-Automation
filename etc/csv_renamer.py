# -*- coding: utf-8 -*-

import os
import csv
import unicodedata

csv_path = r"D:\Clouds\YandexDisk\Fests\АтомКосКон2018\data.csv"
num_row = '№'

folder_paths = [r"D:\Clouds\YandexDisk\Fests\АтомКосКон2018\src"]
num_sep = '. '
subnum_sep = '-'


def make_name(d, num, subnum):
    if subnum:
        return f"{num:#03d}. {d['Ник/Косбенд']} - {d['Фандом']} ({subnum})"
    else:
        return f"{num:#03d}. {d['Ник/Косбенд']} - {d['Фандом']}"

# if update:
#     for folder_path in folder_paths:
#         for file_name in os.listdir(folder_path):
#             num = file_name.split(num_sep)[0]
#             name = file_name[len(num) + len(num_sep):]
#             if len(name) > 2:
#                 src = os.path.join(folder_path, num + name)
#                 dst = os.path.join(folder_path, name)
#                 # os.rename(src, dst)
#                 print("[Num Removed]", name)


with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    head = reader.__next__()
    data = {int(row[head.index(num_row)]):
                {head[i]: row[i].strip() for i in range(len(head)) if i != head.index(num_row)} for row in reader}


def to_filename(string):
    filename = unicodedata.normalize('NFD', string).encode('cp1251', 'replace').decode('cp1251')
    filename = filename.replace(':', " -")\
                       .replace('|', ";").replace('/', ";").replace('\\', ";")\
                       .replace('"', "'")
    filename = ''.join(i if i not in "*?<>" else '' for i in filename)
    return filename


for folder_path in folder_paths:
    for file_name in os.listdir(folder_path):
        ext = '.' + file_name.rsplit('.', 1)[-1]
        num = file_name.split(num_sep, 1)[0]
        # name = file_name[:-len(ext)][len(num + num_sep):]

        if subnum_sep in num:
            subnum = num.rsplit(subnum_sep, 1)[-1]
            num = int(num[:-len(subnum) - 1])
            subnum = int(subnum)
        else:
            try:
                num, subnum = int(num), None
            except ValueError:
                print('[NUM NOT FOUND]', file_name)
                continue

        try:
            name_data = data[num]
        except KeyError:
            print('[NOT FOUND IN CSV]', file_name)
            continue

        name = to_filename(make_name(name_data, num, subnum))

        src = os.path.join(folder_path, file_name)
        dst = os.path.join(folder_path, name + ext)
        if src != dst:
            print(src + " -> \n" + dst + '\n')
            os.rename(src, dst)
