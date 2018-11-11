#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Himura Kazuto <himura@tulafest.ru>

from yaml import load
from lib.downloader import Downloader

if __name__ == '__main__':
    config = load(open('config.yml', 'r', encoding='utf-8').read())
    db_path = config['db_path']
    folder_path = config['folder_path']

    query = f"""
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


    def preprocess(num, dir_name, file_name):
        skip_files_with = config['not_scene_files']
        skip_by_field = any([s in file_name for s in skip_files_with])
        return skip_by_field, dir_name, file_name

    d = Downloader(preprocess)

    if d.get_lists(db_path, query):
        print('\nDownloading files...')
        d.download_files(folder_path, True, check_hash_if_exists=False)
