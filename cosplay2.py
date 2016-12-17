import os
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


class Login(object):
    def __init__(self, attempts):
        self.attempts = attempts
        self.cookie_name = 'private_session.cookie'
        self.cookie = None
        self.event_name = None
        self.login = None

        if self.read_info():
            self.api = Cosplay2API(self.event_name)
            while self.attempts > 0:
                if self.sign_in():
                    print("Login successful!")
                    break
                else:
                    print("Login failed!")
                self.attempts -= 1

    def read_info(self):
        with open('config.txt', 'r') as f:
            try:
                self.event_name = f.readline().split('Event name:')[1].strip()
                self.login = f.readline().split('User email:')[1].strip()
                return True
            except IndexError:
                print('Invalid format of config.txt')
                return False

    def sign_in(self):
        try:
            with open(self.cookie_name, 'r') as f:
                self.cookie = f.read()
                print('Checking the cookie from ' + self.cookie_name + ' file. Remember that it is strictly private!')

                req = Request(self.api.settings_GET, None, {'Cookie': self.cookie})
                try:
                    with urlopen(req) as r:
                        response = r.read().decode('utf-8-sig')
                        print('The cookie file works great! Proof: ' + response[:70] + '...')
                    return True
                except HTTPError as e:
                    print("Request failed:", e)
                    print("Deleting the cookie and restarting...")
                    os.remove(self.cookie_name)
                    self.attempts += 1
                    return False

        except FileNotFoundError:
            login_info = urlencode({'name':     self.login,
                                    'password': getpass('Password for ' + self.login + ': ')}).encode('ascii')
            try:
                with urlopen(self.api.login_POST, login_info) as r:
                    cookie = r.getheader('Set-Cookie')
                    with open(self.cookie_name, 'w') as f:
                        f.write(cookie)
                        print('Logged in and saved cookie to the ' + self.cookie_name +
                              ' file. Remember that it is strictly private!')
                        return True
            except HTTPError as e:
                print("Login failed:", e)
                return False

#class Acquire:

if __name__ == "__main__":
    Login(3)

