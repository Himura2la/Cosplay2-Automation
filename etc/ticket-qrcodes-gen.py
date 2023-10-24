# -*- coding: utf-8 -*-
import qrcode
import csv
import os

csv_input = r"C:\Users\glago\Desktop\print1_29_09.csv"
code_row = "code"
qr_dir = "qr"

with open(csv_input, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    head = reader.__next__()
    rows = [{head[i]: row[i].strip() for i in range(len(head))} for row in reader]

csv_output = os.path.splitext(csv_input)[0] + '_qr.csv'
base_dir = os.path.split(csv_input)[0]
qrcodes_path = os.path.join(base_dir, qr_dir)
if not os.path.exists(qrcodes_path): os.makedirs(qrcodes_path)

for ticket in rows:
    code = ticket[code_row]
    qr_img_path = os.path.join(qrcodes_path, code + '.png')
    qrcode.make(code).save(qr_img_path)
    ticket['qr_path'] = os.path.relpath(qr_img_path, base_dir)


with open(csv_output, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter=',', quotechar='"')
    w.writerow(head + [qr_dir])
    w.writerows([row.values() for row in rows])
