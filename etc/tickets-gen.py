import secrets
from datetime import datetime
import csv
import os

types = {
    '01': {
        'descr': 'Билет «Тануки»',
        'image': '1. Тануки.jpg',
        'start': 300,
        'total': 60
    },
    '02': {
        'descr': 'Билет «Кицунэ»',
        'image': '2. Кицунэ.jpg',
        'start': 300,
        'total': 30
    },
    '03': {
        'descr': 'VIP Билет «Ооками»',
        'image': '3. Оками.jpg',
        'start': 300,
        'total': 50
    }
}

image_base_path = r'D:\Clouds\YandexDisk\Fests\Yuki no Odori\Кроли\Билетные кроли'
target_csv_path = r'D:\Clouds\YandexDisk\Fests\Yuki no Odori 9\Tickets\%s.csv'
pool = ['A', 'B', 'D', 'E', 'F', 'H', 'K', 'L', 'M', 'P', 'R', 'S', 'T', 'U', 'V', 'X', 'Y', 'Z'] + \
       [chr(ord('1') + i) for i in range(9)]

if not os.path.exists(os.path.split(target_csv_path)[0]):
    os.makedirs(os.path.split(target_csv_path)[0])


def make_codes(how_many):
    return [''.join([secrets.choice(pool) for _ in range(9)]) for _ in range(how_many)]


target_csv_path = target_csv_path % datetime.now().strftime('%y%m%d%H%M%S')
report = {}

with open(target_csv_path, 'w', encoding='utf-16', newline='') as f:
    w = csv.writer(f, delimiter=',', quotechar='"')
    w.writerow([
    #    'ds',
        'code'
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
            #    f"{ser}-{num}",
                code
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
