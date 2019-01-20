# -*- coding: utf-8 -*-

import csv
import sqlite3
from yaml import load

root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
config = load(open(os.path.join(root, 'config.yml'), 'r', encoding='utf-8').read())
db_path = config['db_path']
db = sqlite3.connect(db_path, isolation_level=None)
c = db.cursor()

c.execute('PRAGMA encoding = "UTF-8"')
c.execute("SELECT value FROM settings WHERE key='id'")

c.execute(open(os.path.join(root, 'sql', 'check_announcements.sql'), 'r', encoding='utf-8').read())

#get data

for i, d in data.items():
    r = f"\n{d['card_code']} {i}\n{d['voting_title']}\n{d['announcement_title']}"
    print(r)
