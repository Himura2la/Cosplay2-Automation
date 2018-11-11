#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import json
import time
import hashlib
import sqlite3
import unicodedata

from urllib import request
from urllib import parse

class Downloader:
    def __init__(self, preprocess_func=None):
        def preprocess_sample(num, dir_name, file_name):
            skip = False
            return skip, dir_name, file_name

        if preprocess_func:
            self.preprocess = preprocess_func
        else:
            self.preprocess = preprocess_sample
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
            name = name.replace('  ', ' ')
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
        filename = string.replace('й', "<икраткое>")
        filename = unicodedata.normalize('NFD', filename).encode('cp1251', 'replace').decode('cp1251')
        filename = filename.replace("<икраткое>", 'й')
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
