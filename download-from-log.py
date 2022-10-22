from genericpath import isfile
import os
from urllib.request import urlopen
from lib.api import Requester
from shutil import copyfileobj

log_path = r"C:\Events\imagiro\Files\log-160822205104.txt"
update = False

with open(log_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    
for line in lines:
    if not line.startswith("download_me "):
        continue
    line = line.lstrip("download_me ")
    parts = line.split("->")
    if len(parts) == 2:
        url, target = (part.strip() for part in parts)
        print(f"{url} -> {target}", end='')
        if os.path.isfile(target):
            if update:
                os.remove(target)
                print(' [DELETED]', end='')
            else:
                print(' [EXISTS]')
                continue
        req = Requester.raw_request(url)
        with urlopen(req) as in_stream, open(target, 'wb') as out_file:
            copyfileobj(in_stream, out_file)
            print(' [OK]')
    else:
        print(f"trash: '{line}'")
