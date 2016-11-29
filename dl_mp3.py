import os
import json
import sqlite3
import urllib.parse

db_name = 'sqlite3_data.db'

with open('event_name.txt', 'r') as f:
    event_name = f.read()

data = dict()

print('Connecting to ' + db_name + '...')

db = sqlite3.connect(os.path.join(event_name, db_name), isolation_level=None)
c = db.cursor()

c.execute('PRAGMA encoding = "UTF-8"')

c.execute("SELECT value FROM settings WHERE key='id'")
event_id = int(c.fetchone()[0])

c.execute("""
SELECT  request_id,
        card_code || ' ' || voting_number || '. ' || voting_title AS name,
        value
FROM 'values', requests, list
WHERE   list.id = topic_id AND
        request_id = requests.id AND
        type = 'file' AND (
        'values'.title = 'Минус в формате mp3' OR
        'values'.title = 'Аудио-трек в формате mp3' OR
        'values'.title = 'Видеофайл' OR
        'values'.title = 'Аудио-трек в формате mp3 или видео') AND
        status = 'approved'
ORDER BY name
""")

images = c.fetchall()

name = ""
counter = 1
for row in images:
    prev_name = name
    request_id, name, data = row
    try:
        file = json.loads(data)
        if 'link' in file.keys():  # External site
            link = file['link']
            print("[LINK]", link, "->", name)
            continue
        else:
            src_filename = file['filename']
            file_ext = file['fileext']
        if prev_name == name:
            counter += 1
            filename = "%s [%d]" % (name, counter)
        else:
            filename = name
            counter = 1

        filename = filename.encode('cp1251', 'replace').decode('cp1251')
        filename = ''.join(i if i not in "\/:*?<>|" else "#" for i in filename) + file_ext
        file_url = '%s.cosplay2.ru/uploads/%d/%d/%s' % (event_name, event_id, request_id, src_filename)
        file_url = 'http://' + urllib.parse.quote(file_url)
        print("[OK]", file_url, "->", filename)

    except (TypeError, AttributeError) as e:
        print("[FAIL]", name + ":", e)

db.close()