#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Himura Kazuto <himura@tulafest.ru>

from urllib import request
import requests
import youtube_dl
import json


class CloudDownloader(object):
    @staticmethod
    def get(url, target):
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'{target}.%(ext)s'
        }
        print(f'Downloading {url} to {target}...')
        ext = None
        try:
            if '://yadi.sk/' in url:
                print('Trying to download from Yandex Disk...')
                url, ext = CloudDownloader.get_link_yadisk(url)
            elif '://cloud.mail.ru/public/' in url:
                print('Trying to download from Mail.Ru Cloud...')
                url, ext = CloudDownloader.get_link_mailru(url)
                return True
            if ext is not None:
                print(f'Downloading the direct link: {url}')
                request.urlretrieve(url, f'{target}.{ext}')
                return True
            else:
                print('Using YoutubeDL...')
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                    return True
        except Exception as e:
            print('Cloud download FAILED !!!')
            print(e)
            return False

    @staticmethod
    def get_link_yadisk(url):
        YADISK_ENDPOINT = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={}'
        href = requests.get(YADISK_ENDPOINT.format(url)).json()['href']
        ext = href.split('filename=', 1)[-1].split('&', 1)[0].split('.', 1)[-1]
        return href, ext

    @staticmethod
    def get_link_mailru(url):
        CLOUD_MAILRU_TOKEN_URL = 'https://cloud.mail.ru/api/v2/tokens/download'
        page = requests.get(url).text
        weblink = url.split('/public/', 1)[-1]
        folders_section = page.rsplit('"folders": {', 1)[-1].rsplit('};</script>', 1)[0]
        folder = json.loads(f'{{{folders_section}')['folder']
        items_count = int(folder['count']['folders']) + int(folder['count']['files'])
        if items_count > 1:
            print(f'Link shares {items_count} items, no idea which one to download...')
            return False
        file_name = folder['list'][0]['name']
        if weblink != folder['list'][0]['weblink'] or weblink != folder['list'][0]['id']:
            print(f'Strange things with mail.ru weblink. URL: {url}, folder: {json.dumps(folder)}')
        weblink_get_section = page.rsplit('"weblink_get": [', 1)[-1].split(']', 1)[0]
        weblink_get = json.loads(weblink_get_section)['url']
        token = requests.get(CLOUD_MAILRU_TOKEN_URL).json()['body']['token']
        file_url = f'{weblink_get}/{weblink}?key={token}'
        ext = file_name.rsplit('.', 1)[-1]
        return file_url, ext


if __name__ == '__main__':
    pass
