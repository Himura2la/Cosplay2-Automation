#!python3
# coding:utf-8

import os
import sqlite3
from PIL import Image

db_path = "/media/himura/Data/Git/Cosplay2-Downloader/tulafest/sqlite3_data.db"
fest_path = "/media/himura/Data/Fests Local/Yuki no Odori 7/Files/tulafest"
target_dirs = ['Арт', 'Фотокосплей']

print('Connecting to %s...' % os.path.basename(db_path))
db = sqlite3.connect(db_path, isolation_level=None)
c = db.cursor()
c.execute('PRAGMA encoding = "UTF-8"')
c.execute("SELECT value FROM settings WHERE key='id'")

texcode = ''


def opt(a, k, pre=''):
    return pre + a[k] if k in a else ''


for target_dir in target_dirs:
    base_dir = os.path.join(fest_path, target_dir)
    for art_dir in os.listdir(os.path.join(fest_path, target_dir)):
        art_path = os.path.join(base_dir, art_dir)
        files = os.listdir(art_path)
        if len(files) != 1:
            texcode += "%% [!!!! ERROR !!!!] Not 1 file in %s\n" % art_dir
            continue
        path = os.path.join(art_path, files[0])

        with Image.open(path) as img:
            w, h = img.size
            portrait = w < h

        num = art_dir

        c.execute("""
            SELECT section_title || '.' || title as key, 
                   REPLACE(GROUP_CONCAT(DISTINCT value), ',', ', ') as value,
                   status
            FROM requests, [values]
            WHERE requests.id = request_id
            AND requests.number = ?
            GROUP BY key
        """, (num,))
        fields = c.fetchall()
        status = fields[0][2]
        fields = {key: val for key, val, _ in fields}

        authors_cat = 'Авторы' if target_dir == 'Арт' else 'Косплееры'
        try:
            nom = fields['Информация о работе.Номинация']
            contest = fields['Информация о работе.Участие в конкурсе']
            nicks = fields[authors_cat + '.Ник']
            city = fields[authors_cat + '.Город']
            title = opt(fields, 'Информация о работе.Название работы')
            fandom = opt(fields, 'Информация о работе.Фэндом(ы)')
            photographer_nick = opt(fields, 'Фотографы (необязательно).Ник')
            photographer_name = opt(fields, 'Фотографы (необязательно).Имя') + opt(fields, 'Фотографы (необязательно).Фамилия', ' ')
            photographer_team = opt(fields, 'Фотографы (необязательно).Команда/сообщество фотографов (необязательно)')
        except KeyError as e:
            texcode += "%% [!!!! ERROR !!!!] No value for '%s' in '%s' (status: %s)\n" % (e.args[0], art_dir, status)
            continue
        
        title = "%s (%s)" % (title, fandom) if title and fandom else title if title \
                                            else fandom if fandom else "Без названия"

        nom = nom if contest == 'В конкурсе' else contest
        extra = ''
        if photographer_nick or photographer_name or photographer_team:
            if photographer_nick or photographer_name:
                photographer = photographer_nick if photographer_nick else photographer_name
                if photographer_team:
                    photographer = "%s (%s)" % (photographer, photographer_team)
            else:
                photographer = photographer_team
            extra += 'Фотограф(ы): %s' % photographer

        texcode += '\\imgportrait' if portrait else '\\imglandscape'
        texcode += '{%s}{%s, г.%s}{%s}{%s}{%s}{%s}\n' % (num, nicks, city, title, nom, extra, path)

print(texcode)
open('images.tex', 'w', encoding='utf-8').write(texcode)
