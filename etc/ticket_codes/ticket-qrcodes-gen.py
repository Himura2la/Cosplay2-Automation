# -*- coding: utf-8 -*-
import qrcode
import urllib
import csv
import os

csv_input = r"C:\Users\glago\YandexDisk\Fests\DiliRock 2024\DiliRockFest 2024 Tickets - rock bands.csv"
qr_dir = "qr"
code_data_rows = ["type", "number", "code"]

def make_code(data_values: list[str]):
    viewform_url = "https://docs.google.com/forms/d/e/1FAIpQLScZ2Na3rU7tdMV7GYcz9wU1Cc54ANDP3zU1NoYLnGvC5IKTmg/viewform"
#    data_values = ["Adult", "Linkin Park", "123"]
    query = urllib.parse.urlencode({
        "usp": "pp_url",
        "entry.150154323": data_values[0],  # Adult/Child
        "entry.1210501521": data_values[1],  # ticket number
        "entry.61963044": data_values[2]     # code (band name)
    })
    return f'{viewform_url}?{query}'

with open(csv_input, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    head = reader.__next__()
    rows = [{head[i]: row[i].strip() for i in range(len(head))} for row in reader]

csv_output = os.path.splitext(csv_input)[0] + '_qr.csv'
base_dir = os.path.split(csv_input)[0]
qrcodes_path = os.path.join(base_dir, qr_dir)
if not os.path.exists(qrcodes_path): os.makedirs(qrcodes_path)

for ticket in rows:
    code = make_code([ticket[code_row] for code_row in code_data_rows])
    file_name = ticket[code_data_rows[1]]
    qr_img_path = os.path.join(qrcodes_path, file_name + '.png')
    qrcode.make(code).save(qr_img_path)
    ticket['qr_path'] = os.path.relpath(qr_img_path, base_dir)


with open(csv_output, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter=',', quotechar='"')
    w.writerow(head + [qr_dir])
    w.writerows([row.values() for row in rows])
