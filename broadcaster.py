#!/usr/bin/python3
# -*- coding: utf-8 -*-

comment = """
Кончается время досыла на Yuki no Odori! tulafest.ru очень ждёт Т__Т
""".strip()  # --------------------------------------------- 1 SMS ->|      --------- 2 SMS with "YnO9, заявка 000: " ->|
target = "status in ('materials')"
email = True
sms = True


from lib.authenticator import Authenticator
from lib.api import Cosplay2API, Requester
import os
import csv
import sqlite3
from time import sleep
from yaml import load, FullLoader

config = load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.yml'), 'r', encoding='utf-8').read(), Loader=FullLoader)
db_path, event_name = config['db_path'], config['event_name']
c2_login, c2_password = config['admin_cs2_name'], config['admin_cs2_password'] if 'admin_cs2_password' in config else None
api = Cosplay2API(event_name)

with sqlite3.connect(db_path, isolation_level=None) as db:
    c = db.cursor()
    c.execute('PRAGMA encoding = "UTF-8"')
    c.execute(f"""
        SELECT DISTINCT
            requests.id,
            '[' || status || '] ' || list.card_code || ' ' || number || IFNULL('. ' || voting_title, '') AS details
        FROM requests, list, [values]
        WHERE topic_id = list.id
          AND request_id = requests.id
          AND {target}""")
    target_requests = [(r_id, details) for r_id, details in c.fetchall()]

print(f'Requests to add the comment to:')
[print(f'{i+1}. {details} ({api.request_url(r_id)})') for i, (r_id, details) in enumerate(target_requests)]
print(f"\nThe comment's text ({len(comment)} characters, {1+len(comment)//70} SMS):\n{comment}")
if not input('\nDo it (yes/no)?: ').lower() in ('y', 'ye', 'yes', 'yep', 'д', 'да'):
    print('You are not ready yet! Please, double check everything and type "yes" to continue.')
    exit()
print("OK, let's go!")

a = Authenticator(event_name, c2_login, c2_password)
if not a.sign_in():
    exit()
r = Requester(a.cookie)

done_requests = set()
try:
    for request_id, details in target_requests:
        r.request(api.add_comment_POST, {"request_id": request_id, "comment": comment, "email": email, "sms": sms})
        print(f'✔️ {details} ({api.request_url(request_id)})')
        done_requests.add(str(request_id))
        sleep(1)
except Exception as e:
    print(type(e).__name__, e)
finally:
    print(f'\nDone! Requests processed ({len(done_requests)}):\nSELECT * FROM [requests] WHERE [id] IN ({",".join(done_requests)})')
