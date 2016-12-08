import os
import sqlite3
import re
import shutil

db_name = 'sqlite3_data.db'
input_dir = 'zad'
with open('event_name.txt', 'r') as f:
    event_name = f.read()

output_dir = os.path.join(event_name, input_dir + '_numbered')
input_dir = os.path.join(event_name, input_dir)
id_regex = re.compile(r"^(?P<code>\w{1,2} \d{3})(?P<ext>\.\w{2,4})$")


def to_filename(string):
    filename = string.encode('cp1251', 'replace').decode('cp1251')
    filename = ''.join(i if i not in "\/*?<>|" else "#" for i in filename)
    filename = filename.replace(':', " -")
    filename = filename.replace('"', "'")
    return filename

print('Connecting to ' + db_name + '...')

db = sqlite3.connect(os.path.join(event_name, db_name), isolation_level=None)
c = db.cursor()
c.execute('PRAGMA encoding = "UTF-8"')

c.execute("""
SELECT card_code||' '||voting_number, number, voting_title
FROM list, requests
WHERE list.id = topic_id AND status = 'approved'
""")

response = c.fetchall()
titles = {k: v for k, _, v in response}
numbers = {k: v for k, v, _ in response}

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for file in os.listdir(input_dir):
    path = os.path.join(input_dir, file)
    if os.path.isfile(path):
        if re.search(id_regex, file) is None:
            continue
        match = re.search(id_regex, file)
        code, ext = match.group('code'), match.group('ext')
        card_code, id = code.split()
        new_filename = u"%03d %s. %s(№%s)%s" % (int(id), card_code, titles[code], numbers[code], ext)
        new_filename = to_filename(new_filename)

        new_path = os.path.join(output_dir, new_filename)

        print(path + "\n" + new_path)
        shutil.copy(path, new_path)
        print("Copied\n")