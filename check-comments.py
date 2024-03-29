#!/usr/bin/python3
# -*- coding: utf-8 -*-

target = "status in ('approved') and default_duration > 0 and card_code not like 'V%'"
org_user_ids = [
    3209  # Himura
]
show_org_comments = True

from lib.authenticator import Authenticator
from lib.api import Cosplay2API, Requester
import os
import csv
import sqlite3
from time import sleep
from lib.config import read_config

config = read_config()
db_path, event_name = config['db_path'], config['event_name']
c2_login, c2_password = config['admin_cs2_name'], config['admin_cs2_password'] if 'admin_cs2_password' in config else None
api = Cosplay2API(event_name)

with sqlite3.connect(db_path, isolation_level=None) as db:
    c = db.cursor()
    c.execute('PRAGMA encoding = "UTF-8"')
    c.execute(f"""
        SELECT DISTINCT
            requests.id,
            '[' || status || '] ' || card_code || ' ' || voting_number || ' (№' || number || ')' || IFNULL('. ' || voting_title, '') AS details
        FROM requests, list, [values]
        WHERE topic_id = list.id
          AND request_id = requests.id
          AND {target}""")
    target_requests = [(r_id, details) for r_id, details in c.fetchall()]

a = Authenticator(event_name, c2_login, c2_password)
if not a.sign_in():
    exit()
r = Requester(a.cookie)

for request_id, details in target_requests:
    response = r.request(api.get_comments_POST, {"request_id": request_id})
    try:
        comments = response['comments']
        head = f'{details} ({api.request_url(request_id)})'
        print(head)
        if (len(comments) == 0):
            continue
        with open('comments.txt', "a", encoding="utf-8") as f:
            f.write(f'\n{head}\n')
            if int(comments[-1]['user_id']) not in org_user_ids:
                f.write(f'***********************************************\n')
            for comment in comments:
                f.write(f'{comment["user_title"]}: {comment["content"]} <{comment["creationtime"]}>\n')
            if int(comments[-1]['user_id']) not in org_user_ids:
                f.write(f'***********************************************\n\n')
    except Exception as e:
        print(e)
        print(response['message'])
