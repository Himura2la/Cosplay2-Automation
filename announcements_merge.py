# -*- coding: utf-8 -*-

import os
import csv
import sqlite3


csv_path = r"C:\Users\glago\Desktop\Announcement_blank.csv"
db_path = r"D:\Git\Cosplay2-Downloader\tulafest\sqlite3_data.db"


with open(csv_path, 'r', encoding='utf-8') as f:
    data = csv.reader(f)
    rows = [[cell for cell in row] for row in data]

print('Connecting to ' + os.path.abspath(db_path) + '...')

db = sqlite3.connect(db_path, isolation_level=None)
c = db.cursor()
c.execute('PRAGMA encoding = "UTF-8"')

c.execute("""
SELECT requests.number, voting_title
FROM list, requests
WHERE list.id = topic_id AND
      status != 'disapproved' AND
	  default_duration > 0
""")

voting_titles = {int(num): val for num, val in c.fetchall()}

for num, announcement in rows:
    num = int(num)
    print("№%d%s%s%s%s%s" % (num, os.linesep, voting_titles[num], os.linesep, announcement, os.linesep))
