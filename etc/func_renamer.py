
import os
import re

d = "/media/data/Clouds/YandexDisk/Fests/ANI-SHINAI 2021/Fest/партнеры"

i=605
for _, f in enumerate(os.listdir(d)):
    i += 5
    new_name = str(i) + " I. " + f.replace('_', ' - ').replace(' - .','.')
    print(f'{f}->{new_name}')
    old_path = os.path.join(d, f)
    new_path = os.path.join(d, new_name)
    os.rename(old_path, new_path)
