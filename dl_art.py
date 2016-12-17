import os
import json
import sqlite3
import hashlib
import urllib.parse
import urllib.request

check_hash_if_exists = False

db_name = 'sqlite3_data.db'
art_folder = 'art'
with open('event_name.txt', 'r') as f:
    event_name = f.read()

art_folder = os.path.join(event_name, art_folder)


def to_filename(string):
    filename = string.encode('cp1251', 'replace').decode('cp1251')
    filename = ''.join(i if i not in "\/*?<>|" else "#" for i in filename)
    filename = filename.replace(':', " -")
    filename = filename.replace('"', "'")
    return filename

data = dict()

print('Connecting to ' + db_name + '...')

db = sqlite3.connect(os.path.join(event_name, db_name), isolation_level=None)
c = db.cursor()

c.execute('PRAGMA encoding = "UTF-8"')

c.execute("SELECT value FROM settings WHERE key='id'")
event_id = int(c.fetchone()[0])

c.execute("""
SELECT request_id,
       card_code||' '||voting_number || ' №'||number || '. ' || voting_title AS name,
       value
FROM 'values', requests, list
WHERE   list.id = topic_id AND
        request_id = requests.id AND
        type = 'file' AND
        card_code IN ("A", "F") AND
        status = 'approved'
ORDER BY name
""")

images = c.fetchall()

db.close()
print(db_name + ' was safely closed...')

print("Let's load!")

if not os.path.exists(art_folder):
    os.makedirs(art_folder)


links = []

name = ""
counter = 1
for row in images:
    prev_name = name
    request_id, name, data = row
    try:
        name = to_filename(name)
        file = json.loads(data)
        if 'link' in file.keys():  # External site
            link = "[LINK] %s -> %s" % (file['link'], name)
            print(link)
            links.append(link + os.linesep)
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

        path = os.path.join(art_folder, filename + file_ext)

        file_url = '%s.cosplay2.ru/uploads/%d/%d/%s' % (event_name, event_id, request_id, src_filename)
        file_url = 'http://' + urllib.parse.quote(file_url)

        if os.path.isfile(path):
            print('[WARNING]', filename, 'exists. ', end='')
            print('Configured not to check. Skipping.')
        else:
            print("[OK]", file_url, "->", filename)
            urllib.request.urlretrieve(file_url, path)

    except (TypeError, AttributeError) as e:
        print("[FAIL]", name + ":", e)


with open(os.path.join(art_folder, 'links.txt'), 'w') as f:
    f.writelines(links)