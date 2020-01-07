#!python3
# coding:utf-8

import os
import re
import sqlite3
from yaml import load, FullLoader
from PIL import Image  # pip install Pillow

config = load(
    open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.yml'), 'r', encoding='utf-8').read(), Loader=FullLoader)
db_path = config['db_path']
tex_path = config['tex_path']
fest_path = config['folder_path']
target_dirs = config['print_noms']
texcode = ''

print('Connecting to %s...' % os.path.basename(db_path))
db = sqlite3.connect(db_path, isolation_level=None)
c = db.cursor()
c.execute('PRAGMA encoding = "UTF-8"')
c.execute("SELECT value FROM settings WHERE key='id'")


def get_field(req_num, titles, sections=None):
    titles = ','.join([f"'{t}'" for t in titles])
    sections_where = "AND section_title IN (%s)" % ','.join([f"'{s}'" for s in sections]) if sections else ''
    query = f"""
        SELECT REPLACE(GROUP_CONCAT(DISTINCT value), ',', ', ') as value
        FROM list, requests, `values`
        WHERE list.id = topic_id AND requests.id = request_id
          AND requests.number = ?
          AND `values`.title in ({titles})
          {sections_where}
    """
    c.execute(query, (req_num,))
    res = c.fetchone()[0]
    return res if res else ''


texcode = r'\renewcommand{\festurl}{https://%s.cosplay2.ru}' % config['event_name']

for target_dir in target_dirs:
    base_dir = os.path.join(fest_path, target_dir)
    for img_name in os.listdir(base_dir):
        img_path = os.path.join(base_dir, img_name)
        num = int(img_name.split('.', 1)[0])
        with Image.open(img_path) as img:
            w, h = img.size
            portrait = w < h
            square = ((max(w, h) - min(w, h)) / min(w, h)) <= 0.3
        c.execute("""
            SELECT requests.id, card_code, voting_number
            FROM list, requests
            WHERE list.id = topic_id
            AND requests.number = ?
        """, (num,))
        req_id, card_code, voting_number = c.fetchone()

        nom = get_field(num, config['nom_fields'])
        nicks = get_field(num, config['nick_fields'], config['authors_sections'])
        cities = get_field(num, config['city_fields'], config['authors_sections'])
        title = get_field(num, config['title_fields'])
        fandom = get_field(num, config['fandom_fields'])
        team = get_field(num, config['team_fields'])
        other_authors_nicks = get_field(num, config['nick_fields'], config['other_authors_sections'])
        other_authors_teams = get_field(num, config['team_fields'], config['other_authors_sections'])

        req_code = f'{card_code}~{voting_number}'
        authors = f'{nicks}~({"косбэнд " if not re.search("косб[эе]нд", team, re.I) else ""}{team})' if team else nicks
        authors += f'~({cities})'
        if other_authors_nicks or other_authors_teams:
            authors += f'. Фотограф{"ы" if "," in other_authors_nicks or other_authors_teams else ""}:~'
            authors += f'{other_authors_nicks}~(команда~{other_authors_teams})' if other_authors_teams else other_authors_nicks

        if fandom and fandom in title:
            if fandom == title:
                fandom = ''
            else:
                title = re.sub(rf'^(.*)\W*{fandom}\W*(.*)$', r'\1\2', title)
        img_path = img_path.replace(os.sep, '/')
        chunk = '\n    '.join(('{%s}' % field for field in (nom, req_code, title, fandom, authors, req_id, img_path)))
        texcode += '\n' + (('\\imgsquare' if square else '\\imgportrait') if portrait else '\\imglandscape') + '\n    '
        texcode += chunk.replace('\\', ' \\textbackslash ')\
                        .replace(r'&', r'\&')\
                        .replace(r'_', r'\_')\
                        .replace(r'^', r'\^{}')

print(texcode)
# open(tex_path, 'w', encoding='utf-8').write(texcode)
