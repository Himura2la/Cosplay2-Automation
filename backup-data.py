#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Himura Kazuto <himura@tulafest.ru>

from datetime import datetime
import os

from lib.config import read_config
from lib.authenticator import Authenticator
from lib.fetcher import Fetcher
from lib.make_db import MakeDB
from lib.validator import Validator

if __name__ == '__main__':
    config = read_config()
    event_name = config['event_name']
    c2_login = config['admin_cs2_name']
    c2_password = config['admin_cs2_password'] if 'admin_cs2_password' in config else None
    backup_dir = config['backups_path'] \
        if 'backups_path' in config and config['backups_path'] != "." \
        else script_dir
    report_path = config['report_path'] if 'report_path' in config else None
    latest_backup_symlink = config['latest_backup_symlink'] if 'latest_backup_symlink' in config else None

    if not os.path.isdir(backup_dir):
        os.makedirs(backup_dir)

    a = Authenticator(event_name, c2_login, c2_password, interactive=False)
    if not a.sign_in():
        exit()

    f = Fetcher(a.event_name, a.cookie)
    if not f.fetch_data():
        exit()
    f.fetch_etickets()
    f.fetch_details()

    db_path = os.path.join(backup_dir, datetime.now().strftime('%y-%m-%d_%H-%M-%S.db'))
    MakeDB(db_path, f.data)

    if latest_backup_symlink:
        os.remove(latest_backup_symlink) if os.path.exists(latest_backup_symlink) else None
        try:
            os.symlink(db_path, latest_backup_symlink)
        except OSError:
            print('[WARNING] Failed to create a latest_backup_symlink!')

    if report_path:
        print('Validating...')
        report_md = "%s\n===\n\n" % os.path.basename(db_path)
        report_md += Validator().validate(db_path)
        try:
            import markdown
        except ImportError:
            print('[WARNING] Execute `pip install markdown` to generate true HTML !!!')
            report_html = '<pre>%s</pre>' % report_md
        else:
            print('Converting report to HTML...')
            report_html = markdown.markdown(report_md)
        report_html = '<!DOCTYPE html><html><head><meta charset="utf-8"></head>' \
                      '<body>%s</body></html>' % report_html
        print('Saving report...')
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report_html)
