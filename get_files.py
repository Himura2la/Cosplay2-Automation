#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Himura Kazuto <himura@tulafest.ru>

import argparse
import hashlib
import json
import os
import sqlite3
from urllib import request
from urllib import parse

from get_data import Authenticator


class Downloader:
    def __init__(self, preprocess_func=None):
        def preprocess_sample(num, dir_name, file_name):
            """ :returns (skip, dir_name, file_name) """
            return False, dir_name, file_name

        self.preprocess = preprocess_func if preprocess_func else preprocess_sample
        self.data = None
        self.event_name = None
        self.event_id = None

    def get_lists(self, db_path, query):
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
        c.execute(query)
        self.data = c.fetchall()

        db.close()
        print('Database', db_path, 'safely closed...')
        return True

    def download_files(self, folder, download_allowed_by_arg=True, check_hash_if_exists=True):
        links_file = 'links.txt'
        links = []
        filenames = set()
        name = ""
        all_files = ""
        counter = 1

        for row in self.data:
            prev_name = name
            request_id, nom, num, title, file_type, file = row
            name = "%0.3d. %s" % (int(num), title if title else "No title")
            try:
                filename = os.path.join(self.__to_filename(nom),
                                        self.__to_filename(name),
                                        self.__to_filename(file_type))
                is_img = False
                if not file:
                    print('[WARNING] No file for', filename, '.')
                    continue
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
                download_required = True
                if os.path.isfile(path):
                    print('[WARNING]', filename, 'exists. ', end='')
                    if check_hash_if_exists:
                        if self.__md5(file_url) == self.__md5(path):
                            print('The same as remote. Skipping...')
                            download_required = False
                        else:
                            print('And differs from the remote one. Updating...')
                    else:
                        print('Configured not to check. Skipping...')
                        download_required = False
                if download_required:
                    if filename not in filenames:
                        filenames.add(filename)
                    else:
                        print("[CRYTICAL]", filename, "was about to overwrite. Check your SQL query!!!")
                        break
                    download_skipped_by_preprocessor, dir_name, file_name = \
                        self.preprocess(int(num), os.path.split(path)[0], os.path.basename(path))
                    filename = os.path.join(dir_name, file_name)
                    print("[SKIP]" if download_skipped_by_preprocessor else "[OK]", file_url, "->", filename)
                    if download_allowed_by_arg and not download_skipped_by_preprocessor:
                        if not os.path.isdir(dir_name):
                            os.makedirs(dir_name)
                        request.urlretrieve(file_url, filename)

            except (TypeError, AttributeError) as e:
                print("[FAIL]", name + ":", e)
        if download_allowed_by_arg:
            with open(os.path.join(folder, links_file), 'w', encoding='utf-8') as f:
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--event_name", dest="event_name", help='Your event URL is EVENT_NAME.cosplay2.ru',
                        required=True)
    parser.add_argument("--db_path", dest="db_path", help='Path to the database (default: EVENT_NAME/sqlite3_data.db)')

    args = parser.parse_args()

    event_name = args.event_name
    db_path = args.db_path if args.db_path else os.path.join('.', event_name, 'sqlite3_data.db')

    scene_query = """
        SELECT request_id,
               list.title as nom,
               requests.number,
               voting_title,
               [values].title as file_type,
               value as file
        FROM [values], requests, list
        WHERE   list.id = topic_id AND
                request_id = requests.id AND
                (type = 'file' OR type = 'image') AND
                nom NOT IN ('Аккредитация фотографов', 'Арт', 'Фотокосплей')
        ORDER BY [values].title
    """

    art_foto_query = """
        SELECT request_id,
               list.title as nom,
               requests.number,
               voting_title,
               [values].title || IFNULL(main_foto, '') as file_type,
               value as file
        FROM [values], requests, list
            LEFT JOIN (SELECT request_section_id as m_rsid, value as main_foto FROM [values] 
                       WHERE title = 'Какую фотографию печатать?')
                       ON m_rsid = request_section_id
        WHERE   list.id = topic_id AND
                request_id = requests.id AND
                (type = 'file' OR type = 'image') AND
                nom IN ('Арт', 'Фотокосплей')
        ORDER BY request_id
    """


    def preprocess_scene(num, dir_name, file_name):
        skip_files_with = ['Видеозапись репетиции', 'Фотография участник', 'Демо-запись', 'Оригинальная композиция']
        skip_by_field = any([s in file_name for s in skip_files_with])

        return skip_by_field, dir_name, file_name

    def preprocess_for_pdf(num, dir_name, file_name):
        skip_by_field = "Не эту" in file_name or "персонажа" in file_name
        new_dir_name = dir_name.split('. ', 1)[0]
        new_file_name = file_name.replace(' ', '-')
        return skip_by_field, new_dir_name, new_file_name

    d = Downloader(preprocess_for_pdf)
    if d.get_lists(db_path, art_foto_query):
        db = sqlite3.connect(db_path, isolation_level=None)
        c = db.cursor()
        c.execute('PRAGMA encoding = "UTF-8"')

        print('\nDownloading files...')
        d.download_files(event_name, True)
