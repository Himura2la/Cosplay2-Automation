#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Himura Kazuto <himura@tulafest.ru>

import youtube_dl


class CloudDownloader(object):
    @staticmethod
    def get(url, target):
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'{target}.%(ext)s'
        }
        print(f'Downloading {url} to {target}...')
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([url])
                return True
            except Exception as e:
                print(e)
                return False


if __name__ == "__main__":
    import json

    links = []

    for i, link in enumerate(links):
        url = json.loads(link)['link']
        CloudDownloader.get(url, f'.\\{i}')
