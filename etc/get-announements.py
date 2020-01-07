# -*- coding: utf-8 -*-

import os
import sqlite3
from yaml import load, FullLoader

root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
config = load(open(os.path.join(root, 'config.yml'), 'r', encoding='utf-8').read(), Loader=FullLoader)
db_path = config['db_path']
db = sqlite3.connect(db_path, isolation_level=None)
c = db.cursor()
c.execute('PRAGMA encoding = "UTF-8"')
c.execute(open(os.path.join(root, 'sql', 'check_announcements.sql'), 'r', encoding='utf-8').read())
header = [d[0] for d in c.description]
data = [{header[i]: val for i, val in enumerate(row)} for row in c.fetchall()]

for d in data:
    r = f"\n[{d['card_code']} {d['voting_number']}] {d['title']}\n{d['voting_title']}\n{d['announcement_title']}"
    print(r)
