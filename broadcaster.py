#!/usr/bin/python3
# -*- coding: utf-8 -*-

comment = """
Поздравляем с прохождением отбора в сценическую программу YnO14! ╰(*°▽°*)╯
Ждём Вас в ВОСКРЕСЕНЬЕ 19.01 с 8 утра на входе участников Тульского Городского Концертного Зала (справа от главного, возле парковки). Репетиция с 8:30 до 11:30. Просьба знать свой номер: {} (он ещё должен в смс прийти, и на бейдже будет)!
До фестиваля осталось совсем немного, так что, пожалуйста, не пишите больше ничего сюда в комментарии к заявке, организаторы уже их не читают,
они просто потеряются (。﹏。*)
Все срочные дела просьба решать с координатором в ЛС.
Следите за новостями в группе ВК (там, кстати, уже есть полная программа),
и до встречи на фесте! ヽ(✿ﾟ▽ﾟ)ノ
""".strip()  # -------------------------------------------- 1 SMS ->|      --------- 2 SMS with "YnO14, заявка 000: " ->|

target = "status = 'approved' and default_duration > 0 and card_code not like 'V%' and card_code not like 'A%'"  # AND requests.id NOT IN ()"
email = True
sms = False


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
	        '[' || status || '] ' || IFNULL(list.card_code || ' ' || voting_number, '№ ' || requests.number) || IFNULL('. ' || voting_title, user_title) AS details
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
        voting_number = details.split('] ', 1)[1].split('. ', 1)[0]
        ready_comment = comment.format(voting_number, voting_number.split(' ', 1)[1][0])
        data = {"request_id": request_id, "comment": ready_comment, "email": email, "sms": sms}

        sent = r.request(api.add_comment_POST, data, False)
        if not sent:
            print(f'X {details} ({api.request_url(request_id)})')
            pass
        else:
            print(f'✔️ {details} ({api.request_url(request_id)})')
        print(ready_comment)
        done_requests.add(str(request_id))
except Exception as e:
    print(type(e).__name__, e)
finally:
    print(f'\nDone! Requests processed ({len(done_requests)}):\nSELECT * FROM [requests] WHERE [id] IN ({",".join(done_requests)})')
