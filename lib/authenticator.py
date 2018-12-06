import os
from getpass import getpass
from .api import Cosplay2API
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import urlopen, Request


class Authenticator(object):
    __cookie_name = 'private-session.cookie'

    def __init__(self, event_name, login, password=None, interactive=True):
        self.event_name = event_name
        self.login = login
        self.password = password
        self.interactive = interactive
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
                print("Trying again...")
                self.__attempts -= 1
        print("Login failed!")
        return False

    def __sign_in(self):
        if os.path.isfile(self.__cookie_name):
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
                print(e)
                print("Seems like the cookie is out of date, deleting it...")
                os.remove(self.__cookie_name)
                self.__attempts += 1
                return False

        else:  # No cookie saved
            if not self.password:
                if self.interactive:
                    self.password = getpass('Password for ' + self.login + ': ')
                else:
                    print("Unable to ask for password in non-interactive mode.")
                    exit()
            login_info = urlencode({'name':     self.login,
                                    'password': self.password}).encode('ascii')
            try:
                with urlopen(self.__api.login_POST, login_info) as r:
                    cookie = r.getheader('Set-Cookie')
                    with open(self.__cookie_name, 'w') as f:
                        f.write(cookie)
                        self.cookie = cookie
                    print("Saved cookie to the '%s' file. Keep this file as your password !!!" % self.__cookie_name)
                    return True
            except HTTPError as e:
                print(e)
                return False
