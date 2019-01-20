#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Himura Kazuto <himura@tulafest.ru>

from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen

import os
from yaml import load
from getpass import getpass

configfile = open(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'config.yml'), 'r', encoding='utf-8')
config = load(configfile.read())
configfile.close()
event_name = config['event_name']
login = config['admin_cs2_name']
password = config['admin_cs2_password']

if not password:
    password = getpass('Password for ' + login + ': ')

login_info = urlencode({'name': login, 'password': password}).encode('ascii')
try:
    with urlopen('http://' + event_name + '.cosplay2.ru/api/' + 'users/login', login_info) as r:
        print("Your cookie: '%s'\nStill hot!" % r.getheader('Set-Cookie'))
except HTTPError as e:
    print('Failed T_T Check your password...\n' + str(e))
