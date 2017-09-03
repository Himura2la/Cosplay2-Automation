#!/usr/bin/python3
# -*- coding: utf-8 -*-
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
    def __init__(self):
        self.data = None
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

        print('Querying...')
        c.execute("""
               SELECT request_id,
               list.title,
               requests.number,
               team,
               nicks,
               name,
               [values].title,
               value
        FROM [values], requests, list

        LEFT JOIN (SELECT request_id as nc_rid, REPLACE(GROUP_CONCAT(DISTINCT value), ',', ', ') as nicks FROM [values] 
                 WHERE title LIKE 'Отображаемое всем имя%'
                 GROUP BY request_id)
                 ON nc_rid = requests.id

        LEFT JOIN (SELECT request_id as tm_rid, value as team FROM [values] 
                 WHERE title = 'Название команды (как пишется)' OR 
                       title = 'Название команды')
                 ON tm_rid = requests.id
                
        LEFT JOIN (SELECT request_id as f_rid, value as name FROM [values] 
                 WHERE title LIKE 'Название%' AND
                       title NOT LIKE '%команды%' AND
                       title NOT LIKE '%источника танца%' AND
                       title NOT LIKE '%русскими буквами')
                 ON f_rid = requests.id

        WHERE   list.id = topic_id AND
                request_id = requests.id AND
                (type = 'file' OR type = 'image') AND
                status = 'approved'
        ORDER BY [values].title
        """)
        self.data = c.fetchall()

        db.close()
        print('Database', db_path, 'safely closed...')
        return True

    def download_files(self, folder, actual_download=True, check_hash_if_exists=True):
        links_file = 'links.txt'
        links = []
        name = ""
        all_files = ""
        counter = 1

        for row in self.data:
            prev_name = name
            request_id, nom, num, team, nicks, title, file_type, file = row
            name = "№%s. %s" % (num, team if nicks.count(',') > 2 else nicks)
            if title:
                name += " - %s" % title
            try:
                filename = os.path.join(self.__to_filename(nom),
                                        self.__to_filename(name),
                                        self.__to_filename(file_type))
                is_img = False
                file = json.loads(file)
                if 'link' in file.keys():  # External site
                    if name in all_files:
                        print('[INFO]', name, "was manually created.")
                    else:
                        link = "[LINK] %s -> %s" % (file['link'], filename)
                        print(link)
                        links.append(link + os.linesep)
                    continue
                else:
                    src_filename = file['filename']
                    if 'fileext' in file:
                        file_ext = file['fileext']
                    else:
                        file_ext = '.jpg'
                        is_img = True

                if prev_name == name:
                    counter += 1
                    filename += str(counter)
                filename += file_ext
                path = os.path.join(folder, filename)
                file_url = 'http://' + parse.quote('%s.cosplay2.ru/uploads/%d/%d/%s' % (self.event_name, self.event_id,
                                                                                        request_id, src_filename))
                if is_img:
                    file_url += '.jpg'  # Yes, it works
                do_download = True
                if os.path.isfile(path):
                    print('[WARNING]', filename, 'exists. ', end='')
                    if check_hash_if_exists:
                        if self.__md5(file_url) == self.__md5(path):
                            print('The same as remote. Skipping...')
                            do_download = False
                        else:
                            print('And differs from the remote one. Updating...')
                    else:
                        print('Configured not to check. Skipping...')
                        do_download = False
                if do_download:
                    print("[OK]", file_url, "->", filename)
                    if actual_download:
                        if not os.path.isdir(os.path.split(path)[0]):
                            os.makedirs(os.path.split(path)[0])
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

    print()
    d = Downloader()
    d.get_lists(db_path)

    print('\nDownloading files...')
    d.download_files(a.event_name, False)
