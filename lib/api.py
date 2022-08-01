#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import json
import binascii
from urllib.error import HTTPError
from urllib.request import urlopen, Request


class Cosplay2API(object):
    def __init__(self, event_name):
        self.event_name = event_name
        self.api = 'https://' + event_name + '.cosplay2.ru/api/'

        self.login_POST = self.api + 'users/login'
        self.request_details_POST = self.api + 'requests/get'
        self.save_data_POST = self.api + 'requests/save_data'
        self.get_comments_POST = self.api + 'requests/get_comments'
        self.add_comment_POST = self.api + 'requests/add_comment'

        self.settings_GET = self.api + 'events/get_settings'
        self.list_GET = self.api + 'topics/get_list'
        self.requests_GET = self.api + 'topics/get_all_requests'
        self.values_GET = self.api + 'requests/get_all_values'
        self.data_GET_URLs = [self.settings_GET, self.list_GET, self.requests_GET, self.values_GET]

        self.etickets_GET = self.api + 'etickets/get_list'

    def request_url(self, request_id):
        return 'https://%s.cosplay2.ru/orgs/requests/request/%s' % (self.event_name, request_id)


class Requester(object):
    def __init__(self, cookie, wid=None):
        self.__cookie = cookie
        self.__wid = wid if wid else binascii.b2a_hex(os.urandom(8)).decode()

    @staticmethod
    def raw_request(url, data=None, headers={}):
        headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:104.0) Gecko/20100101 Firefox/104.0'
        return Request(url, data, headers)

    def request(self, url, params=None, json_response=True):
        if params:
            params['wid'] = self.__wid
            params = json.dumps(params).encode('ascii')
        req = Requester.raw_request(url, params, {'Cookie': self.__cookie})
        try:
            with urlopen(req) as r:
                response = r.read().decode('utf-8-sig')
                if json_response:
                    response = json.loads(response)
            return response
        except HTTPError as e:
            print("Request failed:", e)
            print("Maybe login required...")
            return False
