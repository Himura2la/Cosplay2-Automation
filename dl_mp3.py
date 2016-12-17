import os
import json
import sqlite3
import hashlib
import urllib.parse
import urllib.request

check_hash_if_exists = False

db_name = 'sqlite3_data.db'
mp3_folder = 'mp3'
with open('config.txt', 'r') as f:
    event_name = f.read()

mp3_folder = os.path.join(event_name, mp3_folder)


def md5(uri):
    remote = True
    if uri.find("http://") == 0 or uri.find("https://") == 0:
        file = urllib.request.urlopen(uri)
    else:
        file = open(uri, 'rb')
    hash = hashlib.md5()
    for chunk in iter(lambda: file.read(4096), b""):
        hash.update(chunk)
    if not remote:
        file.close()
    return hash.hexdigest()


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
SELECT  request_id,
        /*card_code||' '||voting_number*/ '№ '||number || '. ' || voting_title AS name,
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

db.close()
print(db_name + ' was safely closed...')

print("Let's load!")

if not os.path.exists(mp3_folder):
    os.makedirs(mp3_folder)

all_files = "\n".join(os.listdir(mp3_folder))

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
            if name in all_files:
                print('[WARNING]', name, "exists and was downloaded by link. Can't check this.")
            else:
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

        path = os.path.join(mp3_folder, filename + file_ext)

        file_url = '%s.cosplay2.ru/uploads/%d/%d/%s' % (event_name, event_id, request_id, src_filename)
        file_url = 'http://' + urllib.parse.quote(file_url)

        dl = True
        if os.path.isfile(path):
            print('[WARNING]', filename, 'exists. ', end='')
            if check_hash_if_exists:
                if md5(file_url) == md5(path):
                    print('The same as remote. Skipping.')
                    dl = False
                else:
                    print('And differs from the remote one. Updating.')
            else:
                print('Configured not to check. Skipping.')
                dl = False
        if dl:
            print("[OK]", file_url, "->", filename)
            #urllib.request.urlretrieve(file_url, path)

    except (TypeError, AttributeError) as e:
        print("[FAIL]", name + ":", e)


with open(os.path.join(mp3_folder, 'links.txt'), 'w') as f:
    f.writelines(links)