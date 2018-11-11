#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Himura Kazuto <himura@tulafest.ru>

import sqlite3
from getpass import getpass
from yaml import load  # pip install pyyaml

from include.authenticator import Authenticator
from include.fetcher import Fetcher
from include.makedb import MakeDB

if __name__ == '__main__':
    config = load(open('config.yml', 'r', encoding='utf-8').read())

    event_name = config['event_name']
    c2_login = config['admin_cs2_name']
    c2_password = config['admin_cs2_password'] if 'admin_cs2_password' in config else None
    db_path = config['db_path']
    sql = config['sql_after_get'].strip() if 'sql_after_get' in config else None

    a = Authenticator(event_name, c2_login, c2_password)
    if not a.sign_in():
        exit()

    print()
    f = Fetcher(a.event_name, a.cookie)
    if not f.fetch():
        exit()

    print()
    MakeDB(db_path, f.data)

    if sql:
        from tabulate import tabulate

        print('\nConnecting to ' + db_path + ' again...')
        with sqlite3.connect(db_path, isolation_level=None) as db:
            c = db.cursor()
            c.execute('PRAGMA encoding = "UTF-8"')
            c.execute(sql)
            print(tabulate(c.fetchall(), headers=[description[0] for description in c.description], tablefmt='grid'))
