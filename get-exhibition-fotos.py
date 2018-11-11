#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Himura Kazuto <himura@tulafest.ru>

from yaml import load
from lib.downloader import Downloader

if __name__ == '__main__':
    config = load(open('config.yml', 'r', encoding='utf-8').read())
    db_path = config['db_path']
    folder_path = config['folder_path']

    print_noms = ','.join([f'"{nom}"' for nom in config['print_noms']])
    main_foto_join, main_foto_if = '', ''
    if config['use_main_foto']:
        main_foto_join = f"""
            LEFT JOIN (SELECT request_section_id as m_rsid, 
                              value as main_foto FROM [values] 
                       WHERE title = '{config['print_title']}')
            ON m_rsid = request_section_id
        """
        main_foto_if = " || IFNULL(main_foto, '')"
    query = f"""
        SELECT request_id,
               update_time,
               list.title as nom,
               requests.number,
               voting_title,
               [values].title{main_foto_if} as file_type,
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


    def preprocess(num, dir_name, file_name):
        skip_by_field = "Не эту" in file_name or "персонажа" in file_name
        new_dir_name = dir_name.split('. ', 1)[0]
        new_file_name = file_name.replace(' ', '-')
        return skip_by_field, new_dir_name, new_file_name

    d = Downloader(preprocess)

    if d.get_lists(db_path, query):
        print('\nDownloading files...')
        d.download_files(folder_path, True, check_hash_if_exists=False)
