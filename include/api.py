#!/usr/bin/python3
# -*- coding: utf-8 -*-


class Cosplay2API(object):
    def __init__(self, event_name):
        self.api = 'http://' + event_name + '.cosplay2.ru/api/'

        self.login_POST = self.api + 'users/login'

        self.settings_GET = self.api + 'events/get_settings'
        self.list_GET = self.api + 'topics/get_list'
        self.requests_GET = self.api + 'topics/get_all_requests'
        self.values_GET = self.api + 'requests/get_all_values'

        self.GET_URLs = [self.settings_GET, self.list_GET, self.requests_GET, self.values_GET]

