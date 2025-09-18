#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Himura Kazuto <himura@tulafest.ru>

import os
import sqlite3
import sys

from lib.config import read_config
from lib.fetcher import Fetcher
from lib.make_db import MakeDB

if __name__ == '__main__':
    config = read_config()
    event_name = config['event_name']
    db_path = config['db_path']
    sql = config['sql_after_get'].strip() if 'sql_after_get' in config else None

    all_data = len(sys.argv) > 1 and sys.argv[1] == '-a'

    f = Fetcher()
    if not f.fetch_data():
        exit()

    if all_data:
        if not f.fetch_etickets():
            exit()
        if not f.fetch_details():
            exit()

    print('\nCreating ' + db_path + '...')
    MakeDB(db_path, f.data)

    if sql:
        from tabulate import tabulate

        print('\nConnecting to ' + db_path + ' again...')
        with sqlite3.connect(db_path, isolation_level=None) as db:
            c = db.cursor()
            c.execute('PRAGMA encoding = "UTF-8"')
            c.execute(sql)
            print(tabulate(c.fetchall(), headers=[description[0] for description in c.description], tablefmt='grid'))
