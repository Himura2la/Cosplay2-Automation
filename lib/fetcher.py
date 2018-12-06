import json
from urllib.error import HTTPError
from urllib.request import urlopen, Request

from .api import Cosplay2API


class Fetcher(object):
    def __init__(self, event_name, cookie):
        self.__api = Cosplay2API(event_name)
        self.__cookie = cookie
        self.data = dict()

    def fetch_data(self):
        for url in self.__api.data_GET_URLs:
            name = url.split('_')[-1]
            if self.__request(name, url):
                print("Dataset '%s' acquired successfully." % name)
            else:
                print(url, 'FAILED to acquire!!!')
                return False
        return True

    def fetch_etickets(self):
        if self.__request('etickets', self.__api.etickets_GET, key='etickets'):
            print("E-tickets acquired successfully.")
            return True
        else:
            print('E-tickets are FAILED to acquire!!!')
        return False

    def __request(self, name, url, params=None, key=None):
        req = Request(url, params, {'Cookie': self.__cookie})
        try:
            with urlopen(req) as r:
                response = json.loads(r.read().decode('utf-8-sig'))
                self.data[name] = response[key] if key else response
            return True
        except HTTPError as e:
            print("Request failed:", e)
            print("Maybe login required...")
            return False
