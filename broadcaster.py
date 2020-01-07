#!/usr/bin/python3
# -*- coding: utf-8 -*-

comment = "Привет ^_^ Это автоматическая рассылка."
email = False
sms = False
target = "status in ('approved')"

# ---

from lib.authenticator import Authenticator
from lib.api import Cosplay2API, Requester

import os
import csv
import sqlite3
from yaml import load, FullLoader

print(f"Comment ({len(comment)}):\n{comment}")

config = load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.yml'), 'r', encoding='utf-8').read(), Loader=FullLoader)
db_path = config['db_path']
event_name = config["event_name"]
api = Cosplay2API(event_name)
c2_login = config['admin_cs2_name']
c2_password = config['admin_cs2_password'] if 'admin_cs2_password' in config else None

with sqlite3.connect(db_path, isolation_level=None) as db:
    c = db.cursor()
    c.execute('PRAGMA encoding = "UTF-8"')
    c.execute(f"""
        SELECT DISTINCT
            requests.id,
            '[' || status || '] ' || list.card_code || ' ' || number || '. ' || voting_title AS details
        FROM requests, list, [values]
        WHERE topic_id = list.id
          AND request_id = requests.id
          AND {target}""")
    target_requests = {r_id: details for r_id, details in c.fetchall()}

print(f'\nBroadcast target ({len(target_requests)}):')
[print(f'- {details} ({api.request_url(r_id)})') for r_id, details in target_requests.items()]
if not input('\nDo it (yes/no)?: ').lower() in ('y', 'ye', 'yes', 'yep', 'д', 'да'):
    print('Please, double check everything and type "yes" to continue. Aborting for now.')
    exit()
print("OK, let's go!\n")

a = Authenticator(event_name, c2_login, c2_password)
if not a.sign_in():
    exit()
r = Requester(a.cookie)

for request_id, details in target_requests.items():
    r.request(api.add_comment_POST, {"request_id": request_id, "comment": comment, "email": email, "sms": sms})
    print(f'DONE {details} ({api.request_url(request_id)})')
