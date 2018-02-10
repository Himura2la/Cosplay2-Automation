#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time
import shutil
import sqlite3

db_path = r"D:\Clouds\YandexDisk\Fests\Yuki no Odori 7\db\tulafest\sqlite3_data.db"

input_dir = r"D:\Clouds\YandexDisk\Fests\Yuki no Odori 7\files_by_folder"
output_dir = r"D:\Fests Local\Yuki no Odori 7\Tracks"

sql_queery = """
SELECT 
    requests.number as '№',
    card_code,
    voting_number,
    voting_title,
    sound_start
FROM list, requests
LEFT JOIN (SELECT request_id, value as sound_start FROM [values]
           WHERE title LIKE 'Начало%')
    ON request_id = requests.id
WHERE list.id = topic_id AND
      status = 'approved' AND
      default_duration > 0
"""


# https://github.com/Himura2la/FestEngine/blob/36ca9fd60fa3139f342f7b479406211980ce22b8/src/constants.py#L49
vid_exts = {'avi', 'mp4', 'mov', 'wmv', 'mkv'}
aud_exts = {'mp3', 'wav', 'flac', 'ogg', 'm4a', 'aac'}
img_exts = {'jpeg', 'png', 'jpg'}

# target_exts = img_exts
target_exts = vid_exts | aud_exts

processed_log = ""
title_differences = ""
skipped_files = ""

def make_filename(data, num, title=None):
    req_data = data[num]
    code = "%d %s" % (req_data['voting_number'], req_data['card_code'])

    if title:
        global title_differences
        if req_data['voting_title'] != title:
            title_differences += "%s\nReal: %s\nFile: %s\n" % (code, req_data['voting_title'], title)
    else:
        title = req_data['voting_title']

    sound_start = 'Неизвестно'
    if req_data['sound_start']:
        sound_start = {
            'Трек начинается до выхода на сцену (выход из за кулис под музыку)': 'Сразу',
            'Трек начинается после выхода на сцену (начало с точки, трек начинается вместе с танцем)': 'С точки',
            'Трек начинается после выхода на сцену (начало с точки)': 'С точки',
        }[req_data['sound_start']]
    elif req_data['card_code'][0] == 'V':  # Videos
            sound_start = 'Сразу~'
    elif req_data['card_code'][0] == 'T':  # Dances
            sound_start = 'С точки~'

    title = "[%s] %s №%d" % (sound_start, title, num)

    return code, title


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
data_by_num = {req['№']: req for req in data_dicts}

missing_files = {k for k, v in data_by_num.items()}

print('Processing files...')

prev_dir = ""
for dirpath, dirnames, filenames in os.walk(input_dir):
    for filename in filenames:
        if dirpath != prev_dir:
            prev_dir = dirpath
            rep = 1
        root, dir_name = os.path.split(dirpath)
        if any([filename.endswith(ext) for ext in target_exts]):
            ext = filename.rsplit('.', 1)[1]
            num, title = dir_name.split(". ", 1)
            num = int(num)
            missing_files -= {num}
            code, name = make_filename(data_by_num, num, title)
            new_filename = "%s. %s.%s" % (code, name, ext)
            if os.path.exists(os.path.join(output_dir, new_filename)):
                rep += 1
                new_filename = "%s. %s (%d).%s" % (code, name, rep, ext)

            msg = "%s | %s -> %s" % (dir_name, filename, new_filename)
            processed_log += msg + '\n'
            print(msg)
            old_path = os.path.join(root, dir_name, filename)
            new_path = os.path.join(output_dir, new_filename)

            shutil.copy(old_path, new_path)
        else:
            skipped_files += "%s | %s\n" % (dir_name, filename)


missing_files_msg = "\n".join([". ".join(make_filename(data_by_num, num)) for num in missing_files])
info_log = "\n--- Skipped by extension ---\n" + skipped_files + \
           "\n--- Title differences ---\n" + title_differences + \
           "\n--- Missing files ---\n" + missing_files_msg
print(info_log)
log_file = os.path.join(output_dir, time.strftime("log-%d%m%y%H%M%S.txt", time.localtime()))
open(log_file, 'w', encoding='utf-8').write((processed_log + info_log).replace('\n', os.linesep))
