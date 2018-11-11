#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Himura Kazuto <himura@tulafest.ru>

import argparse
import sqlite3
from yaml import load

from include.downloader import Downloader

if __name__ == "__main__":
    config = load(open("config.yml", "r", encoding='utf-8').read())
    db_path = config['db_path']
    folder_path = config['folder_path']

    scene_query = f"""
        SELECT request_id,
               list.title as nom,
               requests.number,
               voting_title,
               [values].title as file_type,
               value as file
        FROM [values], requests, list
        WHERE   list.id = topic_id AND
                request_id = requests.id AND
                type IN ('file', 'image') AND
                list.default_duration > 0 AND
                status != 'disapproved'
        ORDER BY [values].title
    """

    print_noms = ','.join([f'"{nom}"' for nom in config['print_noms']])
    main_foto_join, main_foto_if = '', ''

    if config['use_main_foto']:
        print_title = config['print_title']
        main_foto_join = f"""
            LEFT JOIN (SELECT request_section_id as m_rsid, 
                              value as main_foto FROM [values] 
                       WHERE title = '{print_title}')
            ON m_rsid = request_section_id
        """
        main_foto_if = " || IFNULL(main_foto, '') as file_type"
    art_foto_query = f"""
        SELECT request_id,
               list.title as nom,
               requests.number,
               voting_title,
               [values].title{main_foto_if},
               value as file
        FROM [values], requests, list
        {main_foto_join}
        WHERE   list.id = topic_id AND
                request_id = requests.id AND
                status != 'disapproved' AND
                type IN ('file', 'image') AND
                nom IN ({print_noms})
        ORDER BY request_id
    """


    def preprocess_scene(num, dir_name, file_name):
        skip_files_with = config['not_scene_files']
        skip_by_field = any([s in file_name for s in skip_files_with])
        return skip_by_field, dir_name, file_name


    def preprocess_for_pdf(num, dir_name, file_name):
        skip_by_field = "Не эту" in file_name or "персонажа" in file_name
        new_dir_name = dir_name.split('. ', 1)[0]
        new_file_name = file_name.replace(' ', '-')
        return skip_by_field, new_dir_name, new_file_name


    if config['get_files'] == 'scene':
        d = Downloader(preprocess_scene)
        query = scene_query
    else:
        d = Downloader(preprocess_for_pdf)
        query = art_foto_query

    if d.get_lists(db_path, query):
        db = sqlite3.connect(db_path, isolation_level=None)
        c = db.cursor()
        c.execute('PRAGMA encoding = "UTF-8"')

        print('\nDownloading files...')
        d.download_files(folder_path, True, check_hash_if_exists=False)
