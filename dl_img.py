import os
import json
import sqlite3
import urllib.request

db_name = 'sqlite3_data.db'
img_folder = 'img'
with open('event_name.txt', 'r') as f:
    event_name = f.read()

img_folder = os.path.join(event_name, img_folder)

data = dict()

print('Connecting to ' + db_name + '...')

db = sqlite3.connect(os.path.join(event_name, db_name), isolation_level=None)
c = db.cursor()

c.execute('PRAGMA encoding = "UTF-8"')

c.execute("SELECT value FROM settings WHERE key='id'")
event_id = int(c.fetchone()[0])

c.execute("""
SELECT request_id,
       /*card_code||' '||voting_number*/ '№ '||number || '. ' || voting_title AS name,
       value
FROM 'values', requests, list
WHERE   list.id = topic_id AND
        request_id = requests.id AND
        type = 'image' AND
        'values'.title LIKE 'Изображени%' AND
        status = 'approved'
ORDER BY name
""")

images = c.fetchall()
db.close()
print(db_name + ' was safely closed...')

print("Let's load!")

if not os.path.exists(img_folder):
    os.makedirs(img_folder)

name = ""
counter = 1
for row in images:
    prev_name = name
    request_id, name, data = row
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
        filename = ''.join(i if i not in "\/*?<>|" else "#" for i in filename) + '.jpg'
        filename = filename.replace(':', " -")
        filename = filename.replace('"', "'")
        file_url = 'http://%s.cosplay2.ru/uploads/%d/%d/%d.jpg' % (event_name, event_id, request_id, image_id)

        print("[OK]", file_url + " -> " + filename)
        urllib.request.urlretrieve(file_url, os.path.join(img_folder, filename))

    except TypeError as e:
        print("[FAIL]", name + ":", e)
