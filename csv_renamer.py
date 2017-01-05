# -*- coding: utf-8 -*-

import os
import csv

update = False

csv_path = u"C:\\Users\\Himura\\Desktop\\Фестиваль Hokori Tori - ПАТИ - программа.csv"
folder_paths = map(lambda x: u"D:\\Фесты\\Hokori Tori Christmas Party 2017\\" + x, [u'zad', u'mp3'])

if update:
    for folder_path in folder_paths:
        for file_name in os.listdir(folder_path):
            num = file_name.split('. ')[0] + '. '
            name = file_name[len(num):]
            if len(name) > 2:
                src = os.path.join(folder_path, num + name)
                dst = os.path.join(folder_path, name)
                os.rename(src, dst)
                print "[Num Removed]", name

with open(csv_path, 'r') as f:
    data = csv.reader(f)
    rows = [[unicode(cell.decode('utf-8')) for cell in row] for row in data]
head, rows = rows[0], rows[1:]

converter = {name: num for num, name in rows}

for folder_path in folder_paths:
    for file_name in os.listdir(folder_path):
        ext = "." + file_name.split('.')[-1]
        name = file_name[:-len(ext)]
        try:
            num = converter[name]
        except KeyError:
            print '[NOT FOUND IN CSV]', name
            continue
        src = os.path.join(folder_path, name + ext)
        dst = os.path.join(folder_path, "%02d. %s%s" % (int(num), name, ext))
        print src + "->" + dst
        os.rename(src, dst)