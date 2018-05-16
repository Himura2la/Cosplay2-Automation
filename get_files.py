#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Himura Kazuto <himura@tulafest.ru>

import argparse
import hashlib
import json
import os
import time
import sqlite3
from urllib import request
from urllib import parse

import unicodedata


class Downloader:
    def __init__(self, preprocess_func=None):
        def preprocess_sample(num, dir_name, file_name):
            """ :returns (skip, dir_name, file_name) """
            return False, dir_name, file_name

        self.preprocess = preprocess_func if preprocess_func else preprocess_sample
        self.data = None
        self.event_name = None
        self.event_id = None
        self.log_infos, self.log_errors = "", ""

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

    def log_info(self, msg, inline=False, head=True):
        msg = '[INFO] ' + msg if head else msg
        if inline:
            print(msg, end='', flush=True)
            self.log_infos += msg
        else:
            print(msg)
            self.log_infos += msg + os.linesep

    def log_error(self, msg):
        print('[ERROR] ' + msg)
        self.log_errors += msg + os.linesep

    def log_link(self, msg):
        print('[LINK] ' + msg)
        self.log_links += msg + os.linesep

    def download_files(self, folder, download_allowed_by_arg=True, check_hash_if_exists=True):
        log_file = os.path.join(folder, time.strftime("log-%d%m%y%H%M%S.txt", time.localtime()))
        self.log_infos, self.log_errors, self.log_links = '', '', ''
        paths = set()
        name = ""
        counter = 0

        for row in self.data:
            prev_name = name
            request_id, nom, num, title, file_type, file = row
            name = self.__to_filename("%0.3d. %s" % (int(num), title if title else "No title"))
            nom, file_type = self.__to_filename(nom), self.__to_filename(file_type)
            download_skipped_by_preprocessor, dir_name, file_name = self.preprocess(int(num), name, file_type)
            display_path = ' | '.join([nom, dir_name, file_name])
            if download_skipped_by_preprocessor:
                self.log_info("SKIP: " + display_path)
                continue
            dir_path = os.path.join(folder, nom, dir_name)
            try:
                is_img = False
                if not file:
                    self.log_error('No file for %s.' % display_path)
                    continue
                file = json.loads(file)
                if 'link' in file.keys():  # External site
                    self.log_link("%s -> %s" % (file['link'], display_path))
                    link_dir_path = os.path.join(folder, nom, '[LINK]' + dir_name)
                    if not os.path.exists(dir_path) and not os.path.exists(link_dir_path) and download_allowed_by_arg:
                        os.makedirs(link_dir_path)
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
                    file_name += '-' + str(counter)
                file_name += file_ext
                path = os.path.join(dir_path, file_name)
                file_url = 'http://' + parse.quote('%s.cosplay2.ru/uploads/%d/%d/%s' % (self.event_name, self.event_id,
                                                                                        request_id, src_filename))

                if is_img:
                    file_url += '.jpg'  # Yes, it works this way
                download_required = True
                if os.path.isfile(path):
                    self.log_info(path + ' exists. ', inline=True)
                    if check_hash_if_exists:
                        if self.__md5(file_url) == self.__md5(path):
                            self.log_info('The same as remote. Skipping...', head=False)
                            download_required = False
                        else:
                            self.log_info('And differs from the remote one. Updating...', head=False)
                    else:
                        self.log_info('Configured not to check. Skipping...', head=False)
                        download_required = False
                if download_required:
                    if path not in paths:
                        paths.add(path)
                    else:
                        self.log_error("!!!! %s was about to overwrite. Check your SQL query!!!" % path)
                        break
                    self.log_info(("DL: " + file_url + " -> " + path), inline=True)
                    if download_allowed_by_arg:
                        if not os.path.isdir(dir_path):
                            os.makedirs(dir_path)
                        request.urlretrieve(file_url, path)
                        self.log_info(' [OK]', head=False)
                    else:
                        self.log_info(' [READY]', head=False)
            except (TypeError, AttributeError, request.HTTPError) as e:
                print("[FAIL]", name + ":", e)

        if not os.path.isdir(folder):
            os.makedirs(folder)
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write("ERRORS:" + os.linesep + self.log_errors + os.linesep)
            f.write("LINKS:" + os.linesep + self.log_links + os.linesep)
            f.write("INFO:" + os.linesep + self.log_infos + os.linesep)
        if self.log_links:
            print("\n--- LINKS ---")
            print(self.log_links)

    @staticmethod
    def __to_filename(string):
        filename = unicodedata.normalize('NFD', string).encode('cp1251', 'replace').decode('cp1251')
        filename = filename.replace(':', " -") \
            .replace('|', ";").replace('/', ";").replace('\\', ";") \
            .replace('"', "'")
        filename = ''.join(i if i not in "*?<>" else '' for i in filename)
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
    parser.add_argument("db_path", help='Path to the database', nargs=1)
    parser.add_argument("-o", help='Target directory (default: Fest)', default='Fest')

    args = parser.parse_args()

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
                nom NOT IN ('Аккредитация фотографов', 'Арт', 'Фотокосплей') AND
                status != 'disapproved'
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


    def preprocess_scene_all_data(num, dir_name, file_name):
        skip_files_with = ['Демо-запись']
        skip_by_field = any([s in file_name for s in skip_files_with])

        return skip_by_field, dir_name, file_name

    def preprocess_scene_tracks_only(num, dir_name, file_name):
        skip_files_with = ['Видеозапись репетиции', 'Фотография', 'Демо-запись', 'Оригинальная композиция']
        skip_by_field = any([s in file_name for s in skip_files_with])

        return skip_by_field, dir_name, file_name

    def preprocess_for_pdf(num, dir_name, file_name):
        skip_by_field = "Не эту" in file_name or "персонажа" in file_name
        new_dir_name = dir_name.split('. ', 1)[0]
        new_file_name = file_name.replace(' ', '-')
        return skip_by_field, new_dir_name, new_file_name

    d = Downloader(preprocess_scene_tracks_only)
    if d.get_lists(args.db_path[0], scene_query):
        db = sqlite3.connect(args.db_path[0], isolation_level=None)
        c = db.cursor()
        c.execute('PRAGMA encoding = "UTF-8"')

        print('\nDownloading files...')
        d.download_files(args.o, True, check_hash_if_exists=False)
