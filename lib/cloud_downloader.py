#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Himura Kazuto <himura@tulafest.ru>

import youtube_dl
import requests
import json


class CloudDownloader(object):
    @staticmethod
    def get(url, target):
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'{target}.%(ext)s'
        }
        print(f'Downloading {url} to {target}...')
        if '://yadi.sk/i' in url:
            print('Getting direct link from YaDisk API...')
            return CloudDownloader.get_link_yadisk(url)
        elif '://cloud.mail.ru/public/' in url:
            print('Getting direct link from Mail.Ru Cloud download page...')
            return CloudDownloader.get_link_mailru(url)
        else:
            print('Using YoutubeDL...')
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                try:
                    ydl.download([url])
                    return True
                except Exception as e:
                    print(e)
                    return False

    @staticmethod
    def get_link_yadisk(url):
        YADISK_ENDPOINT = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={}'
        return requests.get(YADISK_ENDPOINT.format(url)).json()['href']

    @staticmethod
    def get_link_mailru(url):
        CLOUD_MAILRU_TOKEN_URL = 'https://cloud.mail.ru/api/v2/tokens/download'
        page = requests.get(url).text
        part1 = url.split('/public/', 1)[-1]
        weblink_section = page.rsplit('"weblink_get": [', 1)[-1].split(']', 1)[0]
        part0 = json.loads(weblink_section)['url']
        token = requests.get(CLOUD_MAILRU_TOKEN_URL).json()['body']['token']
        filename = ''
        return f'{part0}/{part1}/{filename}?key={token}'
