from urllib.request import *
from urllib.parse import *
from getpass import *
import json
import pickle
import os

with open('event_name.txt', 'r') as f:
    event_name = f.read()
    pass

api = 'http://' + event_name + '.cosplay2.ru/api/'
login_POST = api + 'users/login'
settings_GET = api + 'events/get_settings'
list_GET = api + 'topics/get_list'
requests_GET = api + 'topics/get_all_requests'
values_GET = api + 'requests/get_all_values'

cookie_name = 'private_session.cookie'


def dump_request(url, filename, params=None):
    req = Request(url, params, {'Cookie': cookie})
    with urlopen(req) as r:
        response = json.loads(r.read().decode('utf-8-sig'))
        with open(os.path.join(event_name, filename + '.pickle'), 'wb') as f:
            pickle.dump(response, f)
        print(filename + " done!", )
        # print(str(response) + "\n\n")

try:
    with open(cookie_name, 'r') as f:
        cookie = f.read()
        print('Using cookie from ' + cookie_name + ' file. Remember that it is strictly private!')
except FileNotFoundError as e:
    login = input("Your Cosplay2 e-mail: ")
    login_info = urlencode({'name': login, 'password': getpass('Password for ' + login + ': ')}).encode('ascii')
    with urlopen(login_POST, login_info) as r:
        if r.getcode() == 200:
            cookie = r.getheader('Set-Cookie')
            with open(cookie_name, 'w') as f:
                f.write(cookie)
        else:
            print("Login failed:", r.info())
            exit()

print('Started acquiring data...')

if not os.path.exists(event_name):
    os.makedirs(event_name)

dump_request(settings_GET, 'settings')
dump_request(list_GET, 'list')
dump_request(requests_GET, 'requests')
dump_request(values_GET, 'values')

