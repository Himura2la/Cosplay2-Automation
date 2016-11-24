import os
import json
import sqlite3

db_name = 'sqlite3_data.db'

with open('event_name.txt', 'r') as f:
    event_name = f.read()

data = dict()

print('Connecting to ' + db_name + '...')

db = sqlite3.connect(os.path.join(event_name, db_name), isolation_level=None)
c = db.cursor()

c.execute('PRAGMA encoding = "UTF-8"')

c.execute("""
SELECT card_code || ' ' || voting_number || '. ' || voting_title AS name,
       value
FROM 'values', requests, list
WHERE   list.id = topic_id AND
        request_id = requests.id AND
        type = 'image' AND
        'values'.title LIKE 'Изображени%'
ORDER BY name
""")

images = c.fetchall()

name = ""
counter = 1
for row in images:
    prev_name = name
    name, data = row
    try:
        file = json.loads(data)
        image_id = file['filename']

        if prev_name == name:
            counter += 1
            filename = "%s [%d]" % (name, counter)
        else:
            filename = name
            counter = 1
        filename = filename.encode('cp1251', 'replace').decode('cp1251')
        filename = ''.join(i if i not in "\/:*?<>|" else "#" for i in filename)
        print("[OK]", filename + " -> " + str(image_id))
    except TypeError as e:
        print("[FAIL]", name)

db.close()