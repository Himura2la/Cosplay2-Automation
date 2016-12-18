#!/usr/bin/python3
# Author: Himura Kazuto <himura@tulafest.ru>
# Date: December 2016

import hashlib
import json
import os
import sqlite3
from urllib import request
from urllib import parse

from get_data import Authenticator


class Downloader:
    def __init__(self, img_folder, files_folder, art_folder):
        self.__img_folder = img_folder
        self.__files_folder = files_folder
        self.__art_folder = art_folder
        self.images = None
        self.files = None
        self.art = None
        self.event_name = None
        self.event_id = None

    def get_lists(self, db_path):
        if not os.path.isfile(db_path):
            print('Database ' + db_path + ' not exists...')
            return False

        print('Connecting to ' + db_path + '...')

        db = sqlite3.connect(db_path, isolation_level=None)
        c = db.cursor()

        c.execute('PRAGMA encoding = "UTF-8"')
        c.execute("SELECT value FROM settings WHERE key='id'")
        self.event_id = int(c.fetchone()[0])

        c.execute("SELECT value FROM settings WHERE key='subdomain'")
        self.event_name = c.fetchone()[0]

        print('Collecting images...')
        c.execute("""
        SELECT request_id,
               '№ '||number || '. ' || voting_title AS name,
               value
        FROM   [values], requests, list
        WHERE  list.id = topic_id AND
               request_id = requests.id AND
               type = 'image' AND
               [values].title LIKE 'Изображени%' AND
               status = 'approved'
        ORDER BY name
        """)
        self.images = c.fetchall()

        print('Collecting files...')
        c.execute("""
        SELECT request_id,
                '№ '||number || '. ' || voting_title AS name,
                value
        FROM [values], requests, list
        WHERE   list.id = topic_id AND
                request_id = requests.id AND
                type = 'file' AND (
                [values].title = 'Минус в формате mp3' OR
                [values].title = 'Аудио-трек в формате mp3' OR
                [values].title = 'Видеофайл' OR
                [values].title = 'Аудио-трек в формате mp3 или видео') AND
                status = 'approved'
        ORDER BY name
        """)
        self.files = c.fetchall()

        print('Collecting art...')
        c.execute("""
        SELECT request_id,
               card_code||' '||voting_number || ' №'||number || '. ' || voting_title AS name,
               value
        FROM [values], requests, list
        WHERE   list.id = topic_id AND
                request_id = requests.id AND
                type = 'file' AND
                card_code IN ("A", "F") AND
                status = 'approved'
        ORDER BY name
        """)
        self.art = c.fetchall()

        db.close()
        print('Database', db_path, 'safely closed...')
        return True

    def download_images(self, actual_download=True):
        if not os.path.exists(self.__img_folder) and actual_download:
            os.makedirs(self.__img_folder)
        name = ""
        counter = 1
        for row in self.images:
            prev_name = name
            request_id, name, data = row
            try:
                file = json.loads(data)
                image_id = file['filename']

                if prev_name == name:
                    counter += 1
                    filename = self.__to_filename("%s [%d].jpg" % (name, counter))
                else:
                    filename = self.__to_filename(name + '.jpg')
                    counter = 1
                file_url = 'http://%s.cosplay2.ru/uploads/%d/%d/%d.jpg' % (self.event_name, self.event_id,
                                                                           request_id, image_id)
                print("[OK]", file_url + " -> " + filename)
                if actual_download:
                    request.urlretrieve(file_url, os.path.join(self.__img_folder, filename))
            except TypeError as e:
                print("[FAIL]", name + ":", e)

    def download_files(self, actual_download=True, check_hash_if_exists=True):
        self.__download_files(self.files, self.__files_folder, actual_download, check_hash_if_exists)

    def download_art(self, actual_download=True, check_hash_if_exists=True):
        self.__download_files(self.art, self.__art_folder, actual_download, check_hash_if_exists)

    def __download_files(self, file_list, folder, actual_download=True, check_hash_if_exists=True):
        links_file = 'links.txt'
        links = []
        name = ""
        all_files = ""
        counter = 1

        if actual_download:
            if not os.path.exists(folder):
                os.makedirs(folder)
            all_files = "\n".join(os.listdir(folder))

        for row in file_list:
            prev_name = name
            request_id, name, data = row
            try:
                name = self.__to_filename(name)
                file = json.loads(data)
                if 'link' in file.keys():  # External site
                    if name in all_files:
                        print('[WARNING]', name, "exists and was downloaded by link. Can't check.")
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
                filename += file_ext
                path = os.path.join(folder, filename)
                file_url = 'http://' + parse.quote('%s.cosplay2.ru/uploads/%d/%d/%s' % (self.event_name, self.event_id,
                                                                                        request_id, src_filename))
                dl = True
                if os.path.isfile(path):
                    print('[WARNING]', filename, 'exists. ', end='')
                    if check_hash_if_exists:
                        if self.__md5(file_url) == self.__md5(path):
                            print('The same as remote. Skipping...')
                            dl = False
                        else:
                            print('And differs from the remote one. Updating...')
                    else:
                        print('Configured not to check. Skipping...')
                        dl = False
                if dl:
                    print("[OK]", file_url, "->", filename)
                    if actual_download:
                        request.urlretrieve(file_url, path)
            except (TypeError, AttributeError) as e:
                print("[FAIL]", name + ":", e)
        if actual_download:
            with open(os.path.join(folder, links_file), 'w') as f:
                f.writelines(links)
        else:
            print("\n--- LINKS ---")
            print(''.join(links))

    @staticmethod
    def __to_filename(string):
        filename = string.encode('cp1251', 'replace').decode('cp1251')
        filename = ''.join(i if i not in "\/*?<>|" else "#" for i in filename)
        filename = filename.replace(':', " -")
        filename = filename.replace('"', "'")
        return filename

    @staticmethod
    def __md5(uri):
        remote = True
        if uri.find("http://") == 0 or uri.find("https://") == 0:
            file = request.urlopen(uri)
        else:
            file = open(uri, 'rb')
        hash = hashlib.md5()
        for chunk in iter(lambda: file.read(4096), b""):
            hash.update(chunk)
        if not remote:
            file.close()
        return hash.hexdigest()

if __name__ == "__main__":
    print()
    a = Authenticator()
    a.sign_in()

    db_path = os.path.join(a.event_name, 'sqlite3_data.db')
    folders = map(lambda x: os.path.join(a.event_name, x), ['img', 'mp3', 'art'])

    print()
    d = Downloader(*folders)
    d.get_lists(db_path)

    print('\nDownloading images...')
    d.download_images(False)

    print('\nDownloading files...')
    d.download_files(False)

    print('\nDownloading art and fotocosplay...')
    d.download_art(False)


