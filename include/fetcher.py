import os
import json
import binascii
from urllib.error import HTTPError
from urllib.request import urlopen, Request

from .api import Cosplay2API


class Fetcher(object):
    def __init__(self, event_name, cookie):
        self.__api = Cosplay2API(event_name)
        self.__cookie = cookie
        self.wid = binascii.b2a_hex(os.urandom(8))
        self.data = dict()

    def fetch(self):
        for url in self.__api.GET_URLs:
            name = url.split('_')[-1]
            if self.__request(name, url):
                print("Dataset '%s' acquired successfully." % name)
            else:
                print(url, 'FAILED to acquire!!!')
                return False

        # for request_id in [d['id'] for d in self.data['requests']]:
        #     self.__request('req_details',
        #                    self.__api.request_details_POST,
        #                    json.dumps({'request_id': request_id}).encode('ascii'))
        #     break
        # fields_for_history = [d for d in self.data['values'] if d['type'] in ('file', 'image')]

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
