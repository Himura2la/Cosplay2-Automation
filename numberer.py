#!/usr/bin/python3
# -*- coding: utf-8 -*-

import csv
import sqlite3

from lib.api import Cosplay2API, Requester
from lib.config import read_config

num_row = 'num'
voting_number_row = 'voting_number'

config = read_config()
db_path = config['db_path']
event_name = config["event_name"]
api = Cosplay2API(event_name)
r = Requester(config=config)
numberer_table_path = config['numberer_table_path'] if 'numberer_table_path' in config else None
reset_numbers_mode = not numberer_table_path

with sqlite3.connect(db_path, isolation_level=None) as db:
    c = db.cursor()
    c.execute('PRAGMA encoding = "UTF-8"')
    c.execute("SELECT number, requests.id, voting_number, default_duration FROM list, requests WHERE list.id = topic_id")
    requests = {num: {"id": r_id, "voting_number": '' if voting_number is None else str(voting_number), "scene": default_duration > 0} for num, r_id, voting_number, default_duration in c.fetchall()}


if numberer_table_path:
    with open(numberer_table_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        head = reader.__next__()
        voting_numbers = {int(row[head.index(num_row)]): int(row[head.index(voting_number_row)]) for row in reader if row[head.index(num_row)] and row[head.index(voting_number_row)]}


def set_number(request, target_voting_number, force=False):
    already_ok = not force and request['voting_number'] == target_voting_number
    action_symbol = '==' if already_ok else '->'
    print('https://%s.cosplay2.ru/orgs/requests/request/%s | %s %s %s' % (event_name, request['id'], request['voting_number'], action_symbol, target_voting_number))
    if not already_ok:
        r.request(api.save_data_POST, {"field": "voting_number", "request_id": request['id'], "data": target_voting_number})
        pass

known_requests = [num for (num, req) in requests.items() if reset_numbers_mode or req["scene"]]

if reset_numbers_mode:
    print("resetting voting_number in all requesrs (scene + offline)")
    for i, num in enumerate(known_requests):
        print('[', i+1, '/', len(known_requests), ']', end=" ")
        set_number(requests[num], '', True)
    for i, num in enumerate(known_requests):
        req = requests[num]
        print('[', i+1, '/', len(requests), ']', end=" ")
        set_number(req, str(num), True)
else:
    print("setting voting_number only in scene requesrs")
    # for i, num in enumerate(known_requests):
    #     print('[', i+1, '/', len(known_requests), ']', end=" ")
    #     set_number(requests[num], '', True)
    for i, (num, v_num) in enumerate(voting_numbers.items()):
        req = requests[num]
        print('[', i+1, '/', len(voting_numbers), ']', end=" ")
        set_number(req, v_num)
