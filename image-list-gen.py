import os
import csv
import re

csv_path = r'D:\Clouds\YandexDisk\Fests\AtomCosCon2018\zad.csv'
num_row = 'num'
target_csv_path = r'D:\Clouds\YandexDisk\Fests\AtomCosCon2018\zad_img.csv'

img_dir = r'D:\Clouds\YandexDisk\Fests\AtomCosCon2018\img'
id_regex = re.compile(r'^(\d{3})\.')

empty_img_path = 'null.png'  # http://www.1x1px.me/


with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    head = reader.__next__()
    data = {int(row[head.index(num_row)]): row for row in reader}

rows_source = len(head)
rows_target = 0

for file_name in os.listdir(img_dir):
    if os.path.isdir(file_name):
        continue

    res = re.search(id_regex, file_name)

    if res is None:
        print("[WARNING] Unknown file: '%s'" % file_name)
        continue

    num, name = int(res.group(1)), file_name

    if num not in data:
        print("[WARNING] No row for: '%s'" % file_name)
        continue

    data[num].append(os.path.join(img_dir, file_name))
    if len(data[num]) > rows_target:
        rows_target = len(data[num])

rows_added = rows_target - rows_source
data = data.values()

for row in data:
    no_img = len(row) == rows_source
    if len(row) < rows_target:
        row += [os.path.abspath(empty_img_path)] * (rows_target - len(row))
    if no_img:
        print("[WARNING] No images for: '%s'" % str(row))
        row += ["false"]
    else:
        row += ["true"]

# from tabulate import tabulate
# print(tabulate(data))

with open(target_csv_path, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter=',', quotechar='"')
    w.writerow(head + ["img%d_path" % (i+1) for i in range(rows_added)] + ["fade_on"])
    w.writerows(data)
