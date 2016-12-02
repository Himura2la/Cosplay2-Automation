import os
import sqlite3
import re
import shutil

db_name = 'sqlite3_data.db'
input_dir = 'mp3'
with open('event_name.txt', 'r') as f:
    event_name = f.read()

input_dir = os.path.join(event_name, input_dir)
output_dir = os.path.join(input_dir, 'out')
id_regex = re.compile(r"^№ (\d{1,3})\. (.*)(\.\w{2,4})$")

print('Connecting to ' + db_name + '...')

db = sqlite3.connect(os.path.join(event_name, db_name), isolation_level=None)
c = db.cursor()
c.execute('PRAGMA encoding = "UTF-8"')

c.execute("""
SELECT requests.number, card_code||' '||voting_number as id
FROM list, requests
WHERE list.id = topic_id AND status = 'approved'
""")

response = c.fetchall()
ids = {k: v for k, v in response}

for record in os.listdir(input_dir):
    if os.path.isdir(os.path.join(input_dir, record)):
        dir_name = record
        files = os.listdir(os.path.join(input_dir, record))
    else:
        dir_name = ""
        files = [record]

    for f in files:
        if re.search(id_regex, f) is None:
            continue
        num, name, ext = re.search(id_regex, f).groups()
        card_code, id = ids[int(num)].split()

        new_filename = u"%03d %s. %s%s" % (int(id), card_code, name, ext)

        old_path = os.path.join(input_dir, dir_name, f)
        new_path = os.path.join(output_dir, new_filename)

        print(old_path + "\n" + new_path)
        # shutil.copy(old_path, new_path)
        print("Copied\n")