#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Himura Kazuto <himura@tulafest.ru>

from yaml import load  # pip install pyyaml

from lib.authenticator import Authenticator
from lib.fetcher import Fetcher

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
    if not f.fetch_etickets():
        exit()

    etickets = f.data['etickets']
    paid_etickets = [t for t in etickets if t['etickets_paymethod']]

    print('Я вам посылку принёс, только я вам её не отдам!')  # TODO: Save somehow
