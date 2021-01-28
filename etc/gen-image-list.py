import os
import csv
import re
import shutil

csv_path = r"C:\Users\himura\Desktop\zad_alpha.csv"
num_row = '№'
target_csv_path = r"C:\Users\himura\Desktop\zad_alpha_img.csv"

img_dir = r'D:\Events\Yuki no Odori 10\zad_img'
id_regex = re.compile(r'№(\d{1,3})\.jpg')

empty_img_path = r'D:\Events\Yuki no Odori 10\Yuno_2021.png'
empty_img_path = os.path.abspath(empty_img_path) if empty_img_path else ''

move_used_to = 'used'
no_img_warning = 'Юно не является изображением персонажа'

if move_used_to:
    used_dir = os.path.join(img_dir, move_used_to)
    if not os.path.isdir(used_dir):
        os.mkdir(used_dir)

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
    num = int(res.group(1))
    if num not in data:
        print("[WARNING] No row for: '%s'" % file_name)
        continue

    if move_used_to:
        new_file_name = os.path.join(used_dir, file_name)
        shutil.move(os.path.join(img_dir, file_name), new_file_name)
        file_name = new_file_name
    else:
        file_name = os.path.join(img_dir, file_name)

    data[num].append(file_name)
    if len(data[num]) > rows_target:
        rows_target = len(data[num])

rows_added = rows_target - rows_source
data = data.values()

for row in data:
    no_img = len(row) == rows_source
    if len(row) < rows_target:
        row += [empty_img_path] * (rows_target - len(row))
    if no_img:
        print("[WARNING] No images for: '%s'" % str(row))
        row += [no_img_warning]
    else:
        row += [""]

# from tabulate import tabulate
# print(tabulate(data))

with open(target_csv_path, 'w', encoding='utf-16', newline='') as f:
    w = csv.writer(f, delimiter=',', quotechar='"')
    w.writerow(head + ["@img%d-path" % (i+1) for i in range(rows_added)] + ["no-img-warning"])
    w.writerows(data)
