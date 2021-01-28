# -*- coding: utf-8 -*-

import os
import re
import csv


tracks_dir = r'D:\Clouds\YandexDisk\Fests\Yuki no Odori 10\Fest\Tracks'
tracks_filenames_num_regex = r'№(\d{1,3})'

pages_dir = r'D:\Clouds\YandexDisk\Fests\Yuki no Odori 10\design\Zad\zad'
pages_filenames_page_regex = r'(\d{1,3})$'

page_to_num_csv = r"D:\Clouds\YandexDisk\Fests\Yuki no Odori 10\design\Zad\zad_data_img.csv"
page_col, num_col = 'page', '№'

no_op = bool(0)

src_files = os.listdir(tracks_dir)
num_to_name = {re.search(tracks_filenames_num_regex, name).group(1): name.rsplit('.', 1)[0] for name in src_files if re.search(tracks_filenames_num_regex, name)}

with open(page_to_num_csv, 'r', encoding='utf-16') as f:
    reader = csv.reader(f)
    head = reader.__next__()
    page_to_num = {row[head.index(page_col)]: row[head.index(num_col)] for row in reader if row}


for page_file_name in os.listdir(pages_dir):
    page_file_path = os.path.join(pages_dir, page_file_name)
    if not os.path.isfile(page_file_path):
        continue
    name, ext = page_file_name.rsplit('.', 1)
    page = re.search(pages_filenames_page_regex, name)
    if not page:
        continue
    page = page.group(1)

    if page not in page_to_num.keys():
        print('Page not in csv:', page_file_name)
        continue
    num = page_to_num[page]
    if num not in num_to_name.keys():
        print('Num', num, 'not in tracks for page', page_file_name)
        continue
    name = num_to_name[num]

    old = page_file_path
    new = os.path.join(pages_dir, name + '.' + ext)

    if old != new:
        print(old + " -> \n" + new + '\n')
        if not no_op:
            try:
                os.rename(old, new)
            except Exception as e:
                print("FAILED TO RENAME:", e)

