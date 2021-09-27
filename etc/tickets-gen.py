import secrets
from datetime import datetime
from tempfile import mkdtemp
import csv
import os
import qrcode

types = {
    '01': {
        'descr': 'Билет «Тануки»',
        'start': 300,
        'total': 60
    },
    '02': {
        'descr': 'Билет «Кицунэ»',
        'start': 300,
        'total': 25
    },
    '03': {
        'descr': 'VIP Билет «Ооками»',
        'start': 300,
        'total': 20
    }
}

target_csv_path = r'D:\Clouds\YandexDisk\Fests\Yuki no Odori 11\Tickets\%s.csv'
pool = ['A', 'B', 'D', 'E', 'F', 'H', 'K', 'L', 'M', 'P', 'R', 'S', 'T', 'U', 'V', 'X', 'Y', 'Z'] + \
       [chr(ord('1') + i) for i in range(9)]

if not os.path.exists(os.path.split(target_csv_path)[0]):
    os.makedirs(os.path.split(target_csv_path)[0])

qr_dir = mkdtemp()

def make_codes(how_many):
    return [''.join([secrets.choice(pool) for _ in range(9)]) for _ in range(how_many)]


target_csv_path = target_csv_path % datetime.now().strftime('%y%m%d%H%M%S')
report = {}

with open(target_csv_path, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter=',', quotechar='"')
    w.writerow([
        'code'
        , 'ser'
        , 'num'
        , 'descr'
        , 'qr'
    ])
    for ser, data in types.items():
        report[ser] = {'from': data['start']}
        for i, code in enumerate(make_codes(data['total'])):
            num = data['start'] + i
            qr_img_path = os.path.join(qr_dir, code + '.png')
            qrcode.make(code).save(qr_img_path)
            row = [
                code
                , ser
                , num
                , data['descr']
                , qr_img_path
            ]
            w.writerow(row)
            report[ser]['to'] = num
            print(row)

report = ";".join([f"{t}-{d['from']}..{d['to']}" for t, d in report.items() if 'to' in d])
path, ext = target_csv_path.rsplit('.', 1)
new_path = f"{path} {report}.{ext}"
os.rename(target_csv_path, new_path)
