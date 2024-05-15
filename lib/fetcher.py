import os
import json
import binascii
from urllib.error import HTTPError
from urllib.request import urlopen

from .api import Cosplay2API, Requester


class Fetcher(object):
    def __init__(self, event_name, cookie):
        self.__api = Cosplay2API(event_name)
        self.__cookie = cookie
        self.wid = binascii.b2a_hex(os.urandom(8))
        self.data = dict()

    def fetch_data(self):
        for url in self.__api.data_GET_URLs:
            name = url.split('_')[-1]
            req = Requester.raw_request(url, headers={'Cookie': self.__cookie})
            try:
                with urlopen(req) as r:
                    response = json.loads(r.read().decode('utf-8-sig'))
                    if name == 'requests':
                        for req in response:
                            req['announcement_title'] = None
                    self.data[name] = response
                print("Dataset '%s' acquired successfully." % name)
            except HTTPError as e:
                print("Request failed:", e)
                print("Maybe login required...")
                print(url, 'FAILED to acquire!!!')
                return False
        return True

    def fetch_details(self):
        self.data['details'] = []
        for request_id in [d['id'] for d in self.data['requests']]:
            req = Requester.raw_request(self.__api.request_details_POST, json.dumps({'request_id': request_id}).encode('ascii'), {'Cookie': self.__cookie})
            try:
                with urlopen(req) as r:
                    response = json.loads(r.read().decode('utf-8-sig'))
                    request = filter(lambda a: a['id'] == request_id, self.data['requests']).__next__()
                    request['announcement_title'] = response['request']['announcement_title']
                    request['win'] = response['request']['win']
                    request['win_title'] = response['request']['win_title']
                    self.data['details'].append({'request_id': request_id,
                                                 'json': json.dumps(response, ensure_ascii=False)})
                print("Details for request %s acquired successfully." % request_id)
            except HTTPError as e:
                print("Request failed:", e)
                print('Details are FAILED to acquire!!!')
                return False
        return True

    def fetch_etickets(self):
        req = Requester.raw_request(self.__api.etickets_GET, headers={'Cookie': self.__cookie})
        try:
            with urlopen(req) as r:
                response = json.loads(r.read().decode('utf-8-sig'))
                self.data['etickets'] = response['etickets']
            print("E-tickets acquired successfully.")
            return True
        except HTTPError as e:
            print("Request failed:", e)
            print('E-tickets are FAILED to acquire!!!')
            return False
