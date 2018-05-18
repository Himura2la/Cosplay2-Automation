import os
import sqlite3
import re
import shutil

db_name = 'sqlite3_data.db'
input_dir = 'img'
event_name = 'tulafest'

output_dir = os.path.join(event_name, input_dir + '_numbered')
input_dir = os.path.join(event_name, input_dir)
id_regex = re.compile(r"^№ (?P<num>\d{1,3})\. (?P<name>.*)(?P<ext>\.\w{2,4})$")

print('Connecting to ' + db_name + '...')

db = sqlite3.connect(os.path.join(event_name, db_name), isolation_level=None)
c = db.cursor()
c.execute('PRAGMA encoding = "UTF-8"')

c.execute("""
SELECT requests.number, card_code||' '||voting_number as id, IFNULL(sound_start, "Неизвестно")
FROM list, requests
LEFT JOIN (SELECT request_id, value as sound_start FROM [values]
           WHERE title LIKE 'Начало%')
    ON request_id = requests.id
WHERE list.id = topic_id AND
      status = 'approved'
""")

response = c.fetchall()
ids = {k: v for k, v, _ in response}
sound_starts = {k: v for k, _, v in response}

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

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
        match = re.search(id_regex, f)
        num, name, ext = int(match.group('num')), match.group('name'), match.group('ext')
        try:
            card_code, id = ids[num].split()
            id = int(id)
        except KeyError:
            print('[WARNING] Extra file:' + f + os.linesep)
            continue

        sound_start = {'Неизвестно': '',
                       'До выхода на сцену': ' [G]',
                       'После выхода на сцену': ' [W]'}[sound_starts[num]]

        new_filename = u"%03d %s%s. %s(№%d)%s" % (id, card_code, sound_start, name, num, ext)

        old_path = os.path.join(input_dir, dir_name, f)
        new_path = os.path.join(output_dir, new_filename)

        print(old_path + "\n" + new_path)
        shutil.copy(old_path, new_path)
        print("Copied\n")