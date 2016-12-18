import os
import sqlite3
import re

files_folder = 'H:\ownCloud\DATA\Yuki no Odori 2016\Fest\mp3_numbered'
id_regex = re.compile(r"^№ (\d{1,3})\. (.*)\.\w{2,4}$")
code_regex = re.compile(r"(\d{3}) (\w{1,2})\. (.*?)\(№(\d{1,3})\)")

db_name = 'sqlite3_data.db'
with open('event_name.txt', 'r') as f:
    event_name = f.read()

files_folder = os.path.join(event_name, files_folder)

data = dict()

print('Connecting to ' + db_name + '...')

db = sqlite3.connect(os.path.join(event_name, db_name), isolation_level=None)
c = db.cursor()

c.execute('PRAGMA encoding = "UTF-8"')

c.execute("SELECT value FROM settings WHERE key='id'")
event_id = int(c.fetchone()[0])

c.execute("""
SELECT card_code, voting_number, number, value, voting_title, requests.id
FROM   requests, list
LEFT JOIN (SELECT request_id, value FROM [values] WHERE title IN ('Номинация', 'Тип номера'))
          ON request_id = requests.id
WHERE list.id = topic_id AND
      status = 'approved' AND
      card_code NOT IN ("FG", "A", "F")
""")


def split_name(name):
    res = re.search(code_regex, name)
    if res is not None:
        return res.groups()
    else:
        print("[WARNING] Unknown file '%s'" % name)
        return None, None, None, None

items = c.fetchall()
files = list(map(split_name, os.listdir(files_folder)))

nums_all = {int(number) for _, _, number, _, _, _ in items}
nums_exist = {int(number) for _, _, _, number in files if number is not None}

nums_absent = nums_all - nums_exist  # The whole program in a single line

items_absent = ["[ABSENT] %s %d № %d. (%s) %s [http://tulafest.cosplay2.ru/orgs/requests/request/%d]" %
                (card_code, voting_number, number, nom, voting_title, req_id)
                for card_code, voting_number, number, nom, voting_title, req_id in items
                if number in nums_absent]

[print(i) for i in items_absent]

