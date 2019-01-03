#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import json
import time
import sqlite3
import unicodedata

from urllib import request
from urllib import parse


class Downloader:
    SKIP_DOWNLOAD = 0
    CHECK_UPDATES_ONLY = 1
    DOWNLOAD_UPDATED_REQUESTS = 2
    FORCE_DOWNLOAD_ALL = 3

    def __init__(self, preprocess_func=None):
        def preprocess_sample(num, dir_name, file_name):
            skip = False
            return skip, dir_name, file_name

        self.preprocess = preprocess_func if preprocess_func else preprocess_sample
        self.data = None
        self.event_name = None
        self.event_id = None
        self.log_infos, self.log_errors, self.log_links = '', '', ''

    def get_lists(self, db_path, query):
        """`query` should SELECT the following fields:
            [request_id, update_time, nom, num, title, file_type, file]"""

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

    def download_files(self, folder, action=DOWNLOAD_UPDATED_REQUESTS):
        run_time = time.strftime('%d%m%y%H%M%S', time.localtime())
        log_file = os.path.join(folder, 'log-%s.txt' % run_time)
        self.log_infos, self.log_errors, self.log_links = '', '', ''
        paths = set()
        name = ""
        counter = 0

        new_update_time = {}
        request_updates_path = os.path.join(folder, 'requests-update-time.json')

        if os.path.isfile(request_updates_path):
            existing_update_time = json.load(open(request_updates_path, 'r', encoding='utf-8'), parse_int=True)
            os.rename(request_updates_path, request_updates_path.replace('.', '-bkp-%s.' % run_time))
        else:
            existing_update_time = None

        for row in self.data:
            prev_name = name
            request_id, update_time, nom, num, title, file_type, file = row
            name = self.to_filename('%0.3d. %s' % (int(num), title if title else 'No title'))
            name = name.replace('  ', ' ')
            nom, file_type = self.to_filename(nom), self.to_filename(file_type)
            download_skipped_by_preprocessor, dir_name, file_name = self.preprocess(int(num), name, file_type)
            display_path = ' | '.join([nom, dir_name, file_name])
            if download_skipped_by_preprocessor:
                self.log_info('SKIP: ' + display_path)
                continue
            dir_path = os.path.join(folder, nom, dir_name)
            try:
                is_img = False
                if not file:
                    self.log_error('No file for %s.' % display_path)
                    continue
                file = json.loads(file)
                new_update_time[request_id] = update_time  # assuming it's the same for all request files
                if 'link' in file.keys():  # External site
                    file_exists = file_name in [name.split('.', 1)[0] for name in os.listdir(dir_path)] \
                                    if os.path.exists(dir_path) else False
                    request_up_to_date = existing_update_time \
                                            and str(request_id) in existing_update_time \
                                            and existing_update_time[str(request_id)] == update_time
                    if file_exists:
                        self.log_info(display_path + ' exists. ', inline=True)
                        if request_up_to_date:
                            self.log_info('And the request did not update. Skipping...', head=False)
                        else:
                            self.log_info('And the request updated. You should update it!', head=False)

                    if not file_exists or (file_exists and not request_up_to_date):
                        self.log_link("%s -> %s" % (file['link'], display_path))
                        link_dir_path = os.path.join(folder, nom, dir_name)
                        if not os.path.exists(dir_path) \
                                and not os.path.exists(link_dir_path) \
                                and action >= self.DOWNLOAD_UPDATED_REQUESTS:
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
                if os.path.isfile(path) or os.path.isfile(path + '_'):  # This makes a file invisible for extractor
                    self.log_info(display_path + ' exists. ', inline=True)
                    if action in (self.CHECK_UPDATES_ONLY, self.DOWNLOAD_UPDATED_REQUESTS) and existing_update_time:
                        if str(request_id) in existing_update_time \
                                and existing_update_time[str(request_id)] == update_time:
                            self.log_info('And the request did not update. Skipping...', head=False)
                            download_required = False
                        else:
                            self.log_info('And the request updated. Updating...', head=False)
                    else:
                        self.log_info('Configured not to check or no data on updates. Skipping...', head=False)
                        download_required = False
                if download_required:
                    if path not in paths:
                        paths.add(path)
                    else:
                        self.log_error("!!!! %s was about to overwrite. Check your SQL query!!!" % path)
                        break
                    self.log_info(("DL: " + file_url + " -> " + path), inline=True)
                    if action >= self.DOWNLOAD_UPDATED_REQUESTS:
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
        if action >= self.DOWNLOAD_UPDATED_REQUESTS:
            json.dump(new_update_time, open(request_updates_path, 'w', encoding='utf-8'), indent=4)

        with open(log_file, 'w', encoding='utf-8') as f:
            f.write("ERRORS:" + os.linesep + self.log_errors + os.linesep)
            f.write("LINKS:" + os.linesep + self.log_links + os.linesep)
            f.write("INFO:" + os.linesep + self.log_infos + os.linesep)
        if self.log_errors:
            print("\n--- ERRORS ---")
            print(self.log_errors)
        if self.log_links:
            print("\n--- LINKS ---")
            print(self.log_links)

    @staticmethod
    def to_filename(string):
        filename = string.replace('й', '<икраткое>').replace('Й', '<ИКРАТКОЕ>')\
                         .replace('ё', '<ио>')      .replace('Ё', '<ИО>')
        filename = unicodedata.normalize('NFD', filename).encode('cp1251', 'replace').decode('cp1251')
        filename = filename.replace('<икраткое>', 'й').replace('<ИКРАТКОЕ>', 'Й')\
                           .replace('<ио>', 'ё')      .replace('<ИО>', 'Ё')
        filename = filename.replace(':', ' -') \
            .replace('|', ';').replace('/', ';').replace('\\', ';') \
            .replace('"', "'")
        filename = ''.join(i if i not in '*?<>' else '' for i in filename)
        return filename
