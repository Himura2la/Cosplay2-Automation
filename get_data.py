import json
import os
import sqlite3
from getpass import getpass
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen, Request


class Cosplay2API(object):
    def __init__(self, event_name):
        self.api = 'http://' + event_name + '.cosplay2.ru/api/'

        self.login_POST = self.api + 'users/login'

        self.settings_GET = self.api + 'events/get_settings'
        self.list_GET = self.api + 'topics/get_list'
        self.requests_GET = self.api + 'topics/get_all_requests'
        self.values_GET = self.api + 'requests/get_all_values'

        self.GET_URLs = [self.settings_GET, self.list_GET, self.requests_GET, self.values_GET]


class Authenticator(object):
    __cookie_name = 'private_session.cookie'

    def __init__(self, event_name='tulafest', login='himura@tulafest.ru'):
        self.event_name = event_name
        self.login = login
        self.cookie = None
        self.__attempts = None
        self.__api = None

    def sign_in(self, attempts=3):
        self.__attempts = attempts
        self.__api = Cosplay2API(self.event_name)

        while self.__attempts > 0:
            if self.__sign_in():
                print("Login successful!")
                return True
            else:
                print("Login failed!")
            self.__attempts -= 1
        return False

    def __sign_in(self):
        try:
            with open(self.__cookie_name, 'r') as f:
                self.cookie = f.read()
                print('Checking the cookie from ' + self.__cookie_name + ' file.')

                req = Request(self.__api.settings_GET, None, {'Cookie': self.cookie})
                try:
                    with urlopen(req) as r:
                        response = r.read().decode('utf-8-sig')
                        print('The cookie works great! Proof: ' + response[:70] + '...')
                    return True
                except HTTPError as e:
                    print("Request failed:", e)
                    print("Deleting the cookie and restarting...")
                    os.remove(self.__cookie_name)
                    self.__attempts += 1
                    return False

        except FileNotFoundError:  # No cookie saved
            login_info = urlencode({'name':     self.login,
                                    'password': getpass('Password for ' + self.login + ': ')}).encode('ascii')
            try:
                with urlopen(self.__api.login_POST, login_info) as r:
                    cookie = r.getheader('Set-Cookie')
                    with open(self.__cookie_name, 'w') as f:
                        f.write(cookie)
                        print('Logged in and saved cookie to the ' + self.__cookie_name +
                              ' file. Remember that this file is strictly private!')
                        return True
            except HTTPError as e:
                print("Login failed:", e)
                return False


class Fetcher(object):
    def __init__(self, event_name, cookie):
        self.__api = Cosplay2API(event_name)
        self.__cookie = cookie
        self.data = dict()

    def fetch(self):
        for url in self.__api.GET_URLs:
            name = url.split('_')[-1]
            if self.__request(name, url):
                print("Dataset '%s' acquired successfully." % name)
            else:
                print(url, 'FAILED to acquire!!!')
                return False
        return True

    def __request(self, name, url, params=None):
        req = Request(url, params, {'Cookie': self.__cookie})
        try:
            with urlopen(req) as r:
                response = json.loads(r.read().decode('utf-8-sig'))
                self.data[name] = response
            return True
        except HTTPError as e:
            print("Request failed:", e)
            print("Maybe login required...")
            return False


class MakeDB(object):

    def __init__(self, db_path, data):
        self.__db_path = db_path
        self.data = data

        if os.path.isfile(self.__db_path):
            print('Deleting old database...')
            os.remove(self.__db_path)

        print('Connecting to ' + self.__db_path + '...')
        db = sqlite3.connect(self.__db_path, isolation_level=None)
        cursor = db.cursor()
        cursor.execute('PRAGMA encoding = "UTF-8"')
        cursor.execute("PRAGMA synchronous = OFF")

        self.__make_schemas(cursor)

        for key in data.keys():
            self.__populate(key, cursor)

        db.commit()
        db.close()

        print("All done! Happy SQL\'ing!")

    @staticmethod
    def __make_schemas(c):
        print("Making schemas...")

        c.execute("DROP TABLE IF EXISTS settings")
        c.execute("CREATE TABLE settings (key TEXT PRIMARY KEY, value TEXT)")

        c.execute("DROP TABLE IF EXISTS list")
        c.execute("""CREATE TABLE list (
        id INTEGER PRIMARY KEY, card_code INTEGER, title TEXT, category TEXT, card_enabled INTEGER, card_name_rule TEXT,
        card_announcement_rule TEXT, card_diplom_rule TEXT, default_duration REAL, description TEXT, event_id INTEGER,
        intro TEXT, [order] INTEGER, print_badges INTEGER, public_requests TEXT, time_addons_close TEXT,
        time_cards_open TEXT, time_requests_close TEXT, time_requests_open TEXT, time_voting_close TEXT,
        time_voting_open TEXT, url_code TEXT, voting_group INTEGER, voting_jury INTEGER, voting_public INTEGER)""")

        c.execute("DROP TABLE IF EXISTS requests")
        c.execute("""CREATE TABLE requests (
        id INTEGER PRIMARY KEY, voting_title TEXT, status TEXT, topic_id INTEGER, number INTEGER, comment_time TEXT,
        image_update_time TEXT, new_comments INTEGER, new_updates INTEGER, update_time TEXT, user_id INTEGER,
        user_title TEXT, voting_number INTEGER)""")

        c.execute("DROP TABLE IF EXISTS [values]")
        c.execute("""CREATE TABLE 'values' (
        id INTEGER PRIMARY KEY AUTOINCREMENT, request_id INT, request_section_id INT, section_title TEXT, title TEXT,
        value TEXT, type TEXT, public INTEGER, max_repeat INTEGER)""")

    def __populate(self, key, c):
        print("Populating %s..." % key)

        if type(self.data[key]) is dict:
            c.executemany("INSERT INTO %s (key, value) VALUES(?,?)" % key, self.data['settings']['event'].items())
        elif type(self.data[key]) is list:
            keys = sorted(self.data[key][0].keys())

            rows = '[' + '], ['.join(keys) + ']'
            values = ':' + ', :'.join(keys)

            c.execute("BEGIN TRANSACTION")
            c.executemany("INSERT INTO [%s] (%s) VALUES(%s)" % (key, rows, values), self.data[key])
            c.execute("COMMIT")
        else:
            print("WTF is this ???")

if __name__ == "__main__":
    print()
    a = Authenticator()
    a.sign_in()

    print()
    f = Fetcher(a.event_name, a.cookie)
    f.fetch()

    print()
    MakeDB(os.path.join(a.event_name, 'sqlite3_data.db'), f.data)
