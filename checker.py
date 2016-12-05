import os
import sqlite3
import re

files_folder = 'img'
id_regex = re.compile(r"^№ (\d{1,3})\. (.*)\.\w{2,4}$")

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
SELECT  card_code, voting_number, number, voting_title, requests.id
FROM    requests, list
WHERE   list.id = topic_id AND
        status = 'approved' AND
        card_code NOT IN ("FG", "A", "F")
""")

items = c.fetchall()
files = list(map(lambda f: re.search(id_regex, f).groups(), os.listdir(files_folder)))

nums_all = {int(number) for _, _, number, _, _ in items}
nums_exist = {int(number) for number, _ in files}

nums_absent = nums_all - nums_exist

items_absent = ["%s %d № %d. %s [http://tulafest.cosplay2.ru/orgs/requests/request/%d]" %
                   (card_code, voting_number, number, voting_title, req_id)
                for card_code, voting_number, number, voting_title, req_id in items
                if number in nums_absent]

[print(i) for i in items_absent]

