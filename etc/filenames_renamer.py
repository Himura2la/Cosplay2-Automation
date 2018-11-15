# -*- coding: utf-8 -*-

import os
import re


src_dir = r'D:\Clouds\YandexDisk\Fests\Mira Kamen 2018\Fest'
src_filenames_num_regex = r'^(\d{3})'

dst_dir = r'D:\Fests Local\Mira Kamen 2018\презентация'
dst_filenames_num_regex = r'^(\d{3})'

no_op = bool(1)

src_files = os.listdir(src_dir)
names = {re.search(src_filenames_num_regex, name).group(1): name.rsplit('.', 1)[0] for name in src_files}

for file_name in os.listdir(dst_dir):
    if not os.path.isfile(os.path.join(dst_dir, file_name)):
        continue
    name, ext = file_name.rsplit('.', 1)
    ext = '.' + ext
    num = re.search(dst_filenames_num_regex, name).group(1)

    if num not in names.keys():
        print('Skip', file_name)
        continue

    old = os.path.join(dst_dir, file_name)
    new = os.path.join(dst_dir, names[num] + ext)

    if old != new:
        print(old + " -> \n" + new + '\n')
        if not no_op:
            try:
                os.rename(old, new)
            except Exception as e:
                print("FAILED TO RENAME:", e)

