import os
import csv
import re

img_dir = r'D:\Fests Local\Yuki no Odori 7\Images'
csv_path = r'D:\Clouds\YandexDisk\Fests\Yuki no Odori 7\zad\zad_data.csv'
id_regex = re.compile(r'^(\d{3}) (\w{1,3})\.')

empty_img_path = r'C:\Users\glago\Desktop\null.png'  # http://www.1x1px.me/

target_csv_path = r'D:\Clouds\YandexDisk\Fests\Yuki no Odori 7\zad\zad_data_img.csv'


with open(csv_path, 'r', encoding='utf-8') as f:
    data = csv.reader(f)
    rows = [[cell for cell in row] for row in data]
head, rows = rows[0], rows[1:]

data = {r[0].split(' ', 1)[1]: r for r in rows}

rows_source = len(head)
rows_target = 0

for file_name in os.listdir(img_dir):
    res = re.search(id_regex, file_name)

    if res is None:
        print("[WARNING] Unknown file: '%s'" % file_name)
        continue

    num, name = res.group(1), file_name

    if num not in data:
        print("[WARNING] No row for: '%s'" % file_name)
        continue

    data[num].append(os.path.join(img_dir, file_name))
    if len(data[num]) > rows_target:
        rows_target = len(data[num])

rows_added = rows_target - rows_source
data = data.values()

for row in data:
    if len(row) < rows_target:
        row += [empty_img_path] * (rows_target - len(row))

from tabulate import tabulate
print(tabulate(data))

with open(target_csv_path, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter=',', quotechar='"',)
    w.writerow(head + ["img%d_path" % (i+1) for i in range(rows_added)])
    w.writerows(data)
