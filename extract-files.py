#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time
import shutil
import sqlite3
from yaml import load, FullLoader

from lib.downloader import Downloader

no_op = bool(1)

config = load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.yml'), 'r', encoding='utf-8').read(), Loader=FullLoader)
db_path = config['db_path']
input_dir = config['folder_path']
output_dir = config['extracted_folder_path']

if not os.path.isdir(output_dir):
    os.makedirs(output_dir)

num_title_splitter = '. '
nums_in_filenames = False

skip_card_codes = 'AND card_code NOT IN (%s)' % ','.join([f'"{cc}"' for cc in config['not_scene_card_codes']]) \
                    if 'not_scene_card_codes' in config else ''

sql_queery = f"""
SELECT 
    requests.number as '№',
    card_code,
    list.title as nom,
    voting_number,
    voting_title,
    sound_start
FROM list, requests
LEFT JOIN (SELECT request_id, value as sound_start FROM [values]
           WHERE title LIKE 'Начало%')
    ON request_id = requests.id
WHERE list.id = topic_id
      AND status = 'approved'
      {skip_card_codes}
"""
num_field = '№'

video_exts = {'avi', 'mp4', 'mov', 'wmv', 'mkv'}
audio_exts = {'mp3', 'wav', 'flac', 'ogg', 'm4a', 'aac'}
img_exts = {'jpeg', 'png', 'jpg'}

# target_exts = img_exts
target_exts = video_exts | audio_exts

processed_log = ""
title_differences = ""
skipped_files = ""
errors = ""


def make_filename(data, num, dl_title=None):
    if num not in data:
        return False, num, None

    req_data = data[num]
    code = Downloader.to_filename(f"{req_data['voting_number']} {req_data['card_code']}")
    title = Downloader.to_filename(req_data['voting_title'])

    if dl_title:
        global title_differences
        if req_data['voting_title'] != title or req_data['voting_title'] != dl_title:
            title_differences += f"\n{code}" \
                                 f"\nDownloaded: {dl_title}" \
                                 f"\nExtracted:  {title}" \
                                 f"\nReal:       {req_data['voting_title']}"

    sound_start = 'Неизвестно'
    if req_data['sound_start']:
        sound_start = {
            'Трек начинается до выхода на сцену': 'Сразу',
            'Трек начинается до выхода на сцену (выход из за кулис под музыку)': 'Сразу',
            'Трек начинается после выхода на сцену (начало с точки)': 'С точки',
            'Трек содержит превью (выход из за кулис во время превью танца)': 'Превью',
            'Трек начинается после выноса реквизита и подготовки': 'Стафф'
        }[req_data['sound_start']]
    elif req_data['card_code'][0] == 'V':  # Videos
            sound_start = 'Сразу'
    title = f"[{sound_start}] {title}"

    title = Downloader.to_filename(f"{title} №{req_data['№']:d}")

    return True, code, title


print('Connecting to %s...' % os.path.abspath(db_path))
data, headers = [], []
with sqlite3.connect(db_path, isolation_level=None) as db:
    c = db.cursor()
    c.execute('PRAGMA encoding = "UTF-8"')
    c.execute(sql_queery)
    print('Fetching data...')
    data = c.fetchall()
    headers = [description[0] for description in c.description]
    print('Closing the database...')

data_dicts = [{headers[i]: val for i, val in enumerate(row)} for row in data]
data_by_num = {str(req[num_field]): req for req in data_dicts}

missing_files = {k for k, v in data_by_num.items()}

print('Processing files...')

prev_dir = ""
for dirpath, dirnames, filenames in os.walk(input_dir):
    for filename in filenames:
        if dirpath != prev_dir:
            prev_dir = dirpath
            rep = 1
        root, dir_name = os.path.split(dirpath)
        if dir_name.endswith('-not-extract'):
            continue
        if any([filename.endswith(ext) for ext in target_exts]):
            name = filename.rsplit('.', 1)[0] if nums_in_filenames else dir_name
            ext = filename.rsplit('.', 1)[1]
            if num_title_splitter:
                num, title = name.split(num_title_splitter, 1)
                num = num.lstrip('№')
            else:
                num, title = name, None
            num = num.lstrip('0')
            success, code, name = make_filename(data_by_num, num, title)
            if not success:
                msg = "|>>> ERROR <<<| Failed to make title for %s." % os.path.join(dirpath, filename).replace(input_dir, '.')
                errors += msg + '\n'
                print(msg)
                continue
            missing_files -= {num}
            new_filename = f"{code}. {name}.{ext}"
            if os.path.exists(os.path.join(output_dir, new_filename)):
                rep += 1
                new_filename = f"{code}. {name} ({rep}).{ext}"

            msg = f"{dir_name} | {filename} -> {new_filename}"
            processed_log += msg + '\n'
            print(msg)
            old_path = os.path.join(root, dir_name, filename)
            new_path = os.path.join(output_dir, new_filename)

            if not no_op:
                shutil.copy(old_path, new_path)
        else:
            skipped_files += f"{dir_name} | {filename}\n"


missing_files_msg = "\n".join([". ".join(make_filename(data_by_num, num)[1:]) for num in missing_files])
info_log = "\n--- Skipped by extension ---\n" + skipped_files + \
           "\n--- Title differences ---\n" + title_differences + \
           "\n--- Errors ---\n" + errors + \
           "\n--- Missing files ---\n" + missing_files_msg
print(info_log)
log_file = os.path.join(output_dir, time.strftime("log-%d%m%y%H%M%S.txt", time.localtime()))
open(log_file, 'w', encoding='utf-8').write((processed_log + info_log).replace('\n', os.linesep))
