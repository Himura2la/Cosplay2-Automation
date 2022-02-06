#!python3
# coding:utf-8

import csv
from operator import contains
import os
import re
import sqlite3
from yaml import load, FullLoader
from PIL import Image  # pip install Pillow
import qrcode


fest_path = r'C:\Events\tulafest'
target_dirs = [ 'yno11-fles' ]

qr_dir = r'C:\Events\tulafest\qr'
out_dir = r'C:\Events\tulafest\2'


root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
config = load(
    open(os.path.join(root_dir, 'config.yml'), 'r', encoding='utf-8').read(),
    Loader=FullLoader)
db_path = config['db_path']
print('Connecting to %s...' % os.path.basename(db_path))
db = sqlite3.connect(db_path, isolation_level=None)
c = db.cursor()
c.execute("SELECT value FROM settings WHERE key='subdomain'")
event_subdomain = c.fetchone()[0]
qr_prefix = f'https://{event_subdomain}.cosplay2.ru/cards/card/'


def get_field(req_num, titles, sections=None):
    titles = ','.join([f"'{t}'" for t in titles])
    sections_where = "AND section_title IN (%s)" % ','.join([f"'{s}'" for s in sections]) if sections else ''
    query = f"""
        SELECT REPLACE(GROUP_CONCAT(DISTINCT value), ',', ', ')
        FROM list, requests, `values`
        WHERE list.id = topic_id AND requests.id = request_id
          AND requests.number = ?
          AND `values`.title in ({titles})
          AND IFNULL(value, '') != ''
          {sections_where}
    """
    c.execute(query, (req_num,))
    res = c.fetchone()[0]
    return res.replace('  ', ' ') if res else ''

def format_team(team_value):
    return team_value if "://" in team_value else f"команда {team_value}"

with open(os.path.join(out_dir, 'landscape.csv'), 'w', newline='', encoding='utf=8') as vl:
    landscape_writer = csv.writer(vl)
    with open(os.path.join(out_dir, 'portrait.csv'), 'w', newline='', encoding='utf=8') as vp:
        portrait_writer = csv.writer(vp)
        header = ['nom', 'req_code', 'title', 'authors', 'img_path', 'qr']
        landscape_writer.writerow(header)
        portrait_writer.writerow(header)

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

                competition = get_field(num, ["Участие в конкурсе"])
                nom = get_field(num, config['nom_fields'])
                if competition == "Вне конкурса":
                    nom = f'{nom} ({competition})'
                nicks = get_field(num, config['nick_fields'], config['authors_sections'])
                cities = get_field(num, config['city_fields'], config['authors_sections'])
                title = get_field(num, config['title_fields'])
                fandom = get_field(num, config['fandom_fields'])
                team = get_field(num, config['team_fields'], config['general_sections'])
                other_authors_nicks = get_field(num, config['nick_fields'], config['other_authors_sections'])
                other_authors_teams = get_field(num, config['team_fields'], config['other_authors_sections'])

                req_code = f'{card_code} {voting_number}'
                authors = f'{nicks} ({"косбэнд " if not re.search("косб[эе]нд|cosband", team, re.I) else ""}{team})' if team else nicks
                authors += f'. {cities}' if team else f' ({cities})'
                if other_authors_nicks or other_authors_teams:
                    authors += f'. Фотограф{"ы" if "," in other_authors_nicks else ""}: '
                    authors += f'{other_authors_nicks} ({format_team(other_authors_teams)})' if other_authors_teams else other_authors_nicks
                authors = authors.replace("https://", "").replace("http://", "")

                if fandom and fandom in title:
                    if fandom == title:
                        fandom = ''
                    else:
                        title = re.sub(rf'^(.*)\W*{fandom}\W*(.*)$', r'\1\2', title)
                img_path = img_path.replace(os.sep, '/')

                if fandom.strip() and title.strip():
                    title = f'{fandom} - {title}'
                elif fandom.strip():
                    title = fandom


                qr_img_path = os.path.join(qr_dir, f'{req_id}.png')
                qrcode.make(f'{qr_prefix}{req_id}').save(qr_img_path)
                row = (nom, req_code, title, authors, img_path, qr_img_path)

                if square or portrait:
                    portrait_writer.writerow(row)
                else:
                    landscape_writer.writerow(row)
