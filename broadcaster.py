#!/usr/bin/python3
# -*- coding: utf-8 -*-

comment = """
Косплеер, лови свой промокод на билеты со скидкой! {}
""".strip()  # --------------------------------------------- 1 SMS ->|
target = "[values].title == 'Количество участников' AND status = 'disapproved' AND card_code = 'D'"
email = True
sms = True

def prepare_comment(details, field_value):
    n_persons = int(field_value)
    promocodes = variable_values.pop()
    var_comment = "Косплееры, ловите свои промокоды на билеты со скидкой! {}" if n_persons > 1 else comment
    for i in range(n_persons - 1):
        promocodes += ', ' + variable_values.pop()
    return var_comment.format(promocodes)

    # voting_number = details.split('] ', 1)[1].split('. ', 1)[0]
    # comment.format(voting_number, voting_number.split(' ', 1)[1][0])

variable_values = """
test1
test2
""".strip().split('\n')

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
	        '[' || status || '] ' || IFNULL(list.card_code || ' ' || voting_number, '№ ' || requests.number) || IFNULL('. ' || voting_title, user_title) AS details,
            [values].value
        FROM requests, list, [values]
        WHERE topic_id = list.id
          AND request_id = requests.id
          AND {target}""")
    target_requests = [(r_id, details, field_value) for r_id, details, field_value in c.fetchall()]

print(f'Requests to add the comment to:')
[print(f'{i+1}. {details} [{field_value}] ({api.request_url(r_id)})') for i, (r_id, details, field_value) in enumerate(target_requests)]
print(f"\nVariable values: {len(variable_values)}")
test_comment = prepare_comment(target_requests[0][1], target_requests[0][2])
print(f"The comment's text ({len(test_comment)} characters, {1+len(test_comment)//70} SMS):\n{test_comment}")
if len(target_requests) > len(variable_values):
    print(f'WARNING!!! Variable values are not enough for all requests!!!')
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
    for request_id, details, field_value in target_requests:
        voting_number = details.split('] ', 1)[1].split('. ', 1)[0]
        ready_comment = prepare_comment(details, field_value)
        if not r.request(api.add_comment_POST, {"request_id": request_id, "comment": ready_comment, "email": email, "sms": sms}):
            raise Exception("Maybe you ran out of SMS money...")
        print(f'✔️ {details} [{field_value}] ({api.request_url(request_id)})')
        print(ready_comment)
        done_requests.add(str(request_id))
        sleep(1)
except Exception as e:
    print(type(e).__name__, e)
finally:
    print(f'\nDone! Requests processed ({len(done_requests)}):\nSELECT * FROM [requests] WHERE [id] IN ({",".join(done_requests)})')
