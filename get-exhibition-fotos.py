#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Himura Kazuto <himura@tulafest.ru>

import os
from yaml import load
from lib.downloader import Downloader

if __name__ == '__main__':
    config = load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.yml'), 'r', encoding='utf-8').read())
    db_path = config['db_path']
    folder_path = config['folder_path']
    not_scene_nom_codes = config['not_scene_nom_codes']
    print_photo_title = config['print_photo_title'] if 'print_photo_title' in config else None

    not_scene_nom_codes = ','.join([f"'{nom}'" for nom in not_scene_nom_codes])
    main_foto_join, main_foto_where = [''] * 2
    if print_photo_title:
        main_foto_join = f"""
            LEFT JOIN ( SELECT request_section_id as m_rsid,
                              value as main_foto
                        FROM [values]
                        WHERE title = '{print_photo_title}' )
            ON m_rsid = request_section_id
        """
        main_foto_where = "AND main_foto == 'YES'"
    query = f"""
        SELECT request_id,
               update_time,
               list.title as nom,
               requests.number,
               voting_title,
               [values].title,
               value as file
        FROM [values], requests, list
        {main_foto_join}
        WHERE   list.id = topic_id
            AND request_id = requests.id
            AND status != 'disapproved'
            AND type IN ('file', 'image')
            AND card_code IN ({not_scene_nom_codes})
            {main_foto_where}
        ORDER BY request_id
    """


    def preprocess(num, dir_name, file_name):
        new_dir_name = ''  # No subdirectory for each file
        new_file_name = dir_name.replace(' ', '-').replace('--', '-').replace('--', '-')
        return False, new_dir_name, new_file_name

    d = Downloader(preprocess)

    if d.get_lists(db_path, query):
        print('\nDownloading files...')
        d.download_files(folder_path)
