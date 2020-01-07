#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lib.authenticator import Authenticator
from lib.api import Cosplay2API
from urllib.error import HTTPError
from urllib.request import urlopen, Request

import os
import binascii
import csv
import json
import sqlite3
from yaml import load, FullLoader


RESET_NUMBERS_MODE = False
num_row = 'num'
voting_number_row = 'voting_number'

config = load(open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.yml'), 'r', encoding='utf-8').read(), Loader=FullLoader)
db_path = config['db_path']
event_name = config["event_name"]
api = Cosplay2API(event_name)
c2_login = config['admin_cs2_name']
c2_password = config['admin_cs2_password'] if 'admin_cs2_password' in config else None


with sqlite3.connect(db_path, isolation_level=None) as db:
    c = db.cursor()
    c.execute('PRAGMA encoding = "UTF-8"')
    c.execute("SELECT number, id FROM requests WHERE status in ('approved')")
    request_ids = {num: r_id for num, r_id in c.fetchall()}


if not RESET_NUMBERS_MODE:
    with open(config['numberer_table_path'], 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        head = reader.__next__()
        voting_numbers = {int(row[head.index(num_row)]): int(row[head.index(voting_number_row)]) for row in reader}


class Requester:
    def __init__(self, cookie, wid):
        self.__cookie = cookie
        self.__wid = wid

    def request(self, url, params=None):
        if params:
            params['wid'] = self.__wid
            params = json.dumps(params).encode('ascii')
        req = Request(url, params, {'Cookie': self.__cookie})
        try:
            with urlopen(req) as r:
                response = json.loads(r.read().decode('utf-8-sig'))
            return response
        except HTTPError as e:
            print("Request failed:", e)
            print("Maybe login required...")
            return False


# --------


def set_number(r, request_id, voting_number):
    print(f'https://{event_name}.cosplay2.ru/orgs/requests/request/{request_id}', '->', voting_number)
    r.request(api.save_data_POST, {"field": "voting_number", "request_id": request_id, "data": voting_number})


a = Authenticator(event_name, c2_login, c2_password)
if not a.sign_in():
    exit()
r = Requester(a.cookie, binascii.b2a_hex(os.urandom(8)).decode())


if RESET_NUMBERS_MODE:
    for num in request_ids.keys():
        r_id = request_ids[num]
        set_number(r, r_id, num)
else:
    for num, v_num in voting_numbers.items():
        r_id = request_ids[num]
        set_number(r, r_id, v_num)
