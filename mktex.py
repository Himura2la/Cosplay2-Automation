#!python3
# coding:utf-8

import os
import sqlite3
import re
from yaml import load
from PIL import Image

configfile = open("config.yml", "r")
config = load(configfile.read())
configfile.close()
db_path = config['db_path']
tex_path = config['tex_path']
fest_path = config['folder_path']

target_dirs = config['print_noms']

print('Connecting to %s...' % os.path.basename(db_path))
db = sqlite3.connect(db_path, isolation_level=None)
c = db.cursor()
c.execute('PRAGMA encoding = "UTF-8"')
c.execute("SELECT value FROM settings WHERE key='id'")

texcode = ''


def opt(a, k, pre=''):
    return pre + a[k] if k in a else ''

def getfield(fields, config, options):
    for field in config[options]:
        try:
            return fields[field]
        except KeyError:
            continue
    return ''

for target_dir in target_dirs:
    nom = target_dir
    base_dir = os.path.join(fest_path, target_dir)
    for art_dir in os.listdir(os.path.join(fest_path, target_dir)):
        num = re.findall(r'\d+', art_dir.split('. ')[0])[0]
        num = int(num)
        art_path = os.path.join(base_dir, art_dir)
        files = os.listdir(art_path)
        if len(files) != 1 and config['use_main_foto']:
            texcode += "%% [!!!! ERROR !!!!] Not 1 file in %s\n" % art_dir
            continue
        if len(files) == 0:
            continue
        for imagefile in files:
            path = os.path.join(art_path, imagefile)
            if os.path.splitext(path)[1] == '.pdf':
                continue

            with Image.open(path) as img:
                w, h = img.size
                portrait = w < h
                square = (( max(w, h) - min (w, h) ) / min (w, h)) <= 0.25

            if config['image_pdf'] == True:
                path = os.path.splitext(path)[0]+'.pdf'

            c.execute("""
                SELECT section_title || '.' || title as key, 
                       REPLACE(GROUP_CONCAT(DISTINCT value), ',', ', ') as value,
                       status,
                       requests.id as url_id,
                       voting_number
                FROM requests, [values]
                WHERE requests.id = request_id
                AND requests.number = ?
                GROUP BY key
            """, (num,))
            fields = c.fetchall()
            try:
                status = fields[0][0]
            except IndexError:
                print("SQL returned no section titles for %s." % num)
                status = ""
                exit(-1)
            try:
                status = fields[0][2]
            except IndexError:
                print("Please set card names.")
                status = ""
            try:
                url_id = fields[0][3]
            except IndexError:
                print("Please set request IDs.")
                url_id = ""
            try:
                voting_number = fields[0][4]
            except IndexError:
                print("Please set voting numbers.")
                voting_number = 00
            fields = {key: val for key, val, _, _, _ in fields}

            if target_dir == 'Арт':
                if voting_number != None:
                    nnum = 'ART~%d' % voting_number
                else:
                    if config['dry_run']:
                        nnum = 'ART~%d' % num
            else:
                if voting_number != None:
                    nnum = 'FC~%d' % voting_number
                else:
                    if config['dry_run']:
                        nnum = 'FC~%d' % num

            try:
                nick = getfield(fields, config, 'name_fields')
                city = fields[config['city_field']]
                title = getfield(fields, config, 'name_fields')
                fandom = getfield(fields, config, 'fandom_fields')
                extra = getfield(fields, config, 'extra_fields')
                other_authors = getfield(fields, config, 'other_authors_fields')
            except KeyError as e:
                texcode += "%% [!!!! ERROR !!!!] No value for '%s' in '%s' (status: %s)\n" % (e.args[0], art_dir, status)
                continue

            if other_authors != None:
                extra += other_authors

            if portrait:
                if square:
                    texcode += '\\imgsquare'
                else:
                    texcode += '\\imgportrait'
            else:
                texcode += '\\imglandscape'
            texcode += '{%s}{%s, г.%s}{%s}{%s}{%s}{%s}{%s}\n' % (nnum, nick, city, title, nom, extra, url_id, path)

texcode.replace('&', '\&')

print(texcode)
open(tex_path, 'w', encoding='utf-8').write(texcode)
