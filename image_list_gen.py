import os
import sqlite3
import re

files_folder = 'img_numbered'
id_regex = re.compile(r"^(\d{3}) (\w{1,2})")

db_name = 'sqlite3_data.db'
with open('config.txt', 'r') as f:
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
SELECT card_code, voting_number
FROM   requests, list
WHERE list.id = topic_id AND
      status = 'approved' AND
      card_code NOT IN ("FG", "A", "F")
ORDER BY voting_number
""")


def split_name(name):
    res = re.search(id_regex, name)
    if res is not None:
        return res.group(1), name
    else:
        print("[WARNING] Unknown file '%s'" % name)
        return None, None

items = c.fetchall()
files = list(map(split_name, os.listdir(files_folder)))

nums_all = {int(number) for _, number in items}
nums_exist = {int(number): filename for number, filename in files if number is not None}

for item in sorted(list(nums_all)):
    if item in nums_exist:
        filename = nums_exist[item]
    else:
        filename = "Yuno.png"

    abs_path = os.path.join(os.getcwd(), files_folder, filename)
    print(abs_path)
    if not os.path.exists(abs_path):
        print("[WARNING] No such path!!!")
