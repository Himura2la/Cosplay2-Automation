#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Himura Kazuto <himura@tulafest.ru>

from datetime import datetime
import os
from yaml import load  # pip install pyyaml

from lib.authenticator import Authenticator
from lib.fetcher import Fetcher
from lib.make_db import MakeDB

if __name__ == '__main__':
    config = load(open('config.yml', 'r', encoding='utf-8').read())

    event_name = config['event_name']
    c2_login = config['admin_cs2_name']
    c2_password = config['admin_cs2_password'] if 'admin_cs2_password' in config else None
    backup_dir = config['backups_path'] \
        if 'backups_path' in config and config['backups_path'] != "." \
        else os.path.dirname(os.path.realpath(__file__))

    if not os.path.isdir(backup_dir):
        os.makedirs(backup_dir)

    a = Authenticator(event_name, c2_login, c2_password, interactive=False)
    if not a.sign_in():
        exit()

    f = Fetcher(a.event_name, a.cookie)
    if not f.fetch_data():
        exit()
    if not f.fetch_etickets():
        exit()

    MakeDB(os.path.join(backup_dir, datetime.now().strftime('%y-%m-%d_%H-%M-%S.db')), f.data)
