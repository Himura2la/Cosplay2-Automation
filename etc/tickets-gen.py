import secrets
from datetime import datetime
import csv
import os

types = {
    '01': {
        'descr': 'Билет\n"Тануки"',
        'image': 'tanuki.jpg',
        'start': 321,
        'total': 4
    },
    '02': {
        'descr': 'Билет\n"Кицунэ"',
        'image': 'kitsune.jpg',
        'start': 310,
        'total': 0
    },
    '03': {
        'descr': 'VIP Билет\n"Ооками"',
        'image': 'ookami.jpg',
        'start': 305,
        'total': 20
    }
}

image_base_path = r'D:\Clouds\YandexDisk\Fests\Yuki no Odori 8\design\Ticket\krol'
target_csv_path = f'D:\Clouds\YandexDisk\Fests\Yuki no Odori 8\design\Ticket\\tickets-%s.csv'
pool = ['A', 'B', 'D', 'E', 'F', 'H', 'K', 'L', 'M', 'P', 'R', 'S', 'T', 'U', 'V', 'X', 'Y', 'Z'] + \
       [chr(ord('1') + i) for i in range(9)]


def make_codes(how_many):
    return [''.join([secrets.choice(pool) for _ in range(9)]) for _ in range(how_many)]


target_csv_path = target_csv_path % datetime.now().strftime('%y%m%d%H%M%S')
report = {}

with open(target_csv_path, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter=',', quotechar='"')
    w.writerow([
        'ds'
        , 'code'
        , 'ser'
        , 'num'
        , 'descr'
    #    , 'img'
    ])
    for ser, data in types.items():
        report[ser] = {'from': data['start']}
        for i, code in enumerate(make_codes(data['total'])):
            num = data['start'] + i
            row = [
                f"{ser}-{num}"
                , code
                , ser
                , num
                , data['descr']
            #    , os.path.join(image_base_path, data['image'])
            ]
            w.writerow(row)
            report[ser]['to'] = num
            print(row)

report = ";".join([f"{t}-{d['from']}..{d['to']}" for t, d in report.items() if 'to' in d])
path, ext = target_csv_path.rsplit('.', 1)
new_path = f"{path} {report}.{ext}"
os.rename(target_csv_path, new_path)
