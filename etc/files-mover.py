import os
import shutil
import unicodedata
import re

source_dir = r"D:\Events\Атом 2021\Files"
pattern = re.compile(r"^(\d{3})(\. .+)")

target_dir =  r"D:\Events\Атом 2021\Images"
if not os.path.exists(target_dir): os.makedirs(target_dir)

def replacer(match):
    return match[1] + '. ' + unicodedata.normalize('NFKD', match[2]).encode('ascii', 'ignore').decode()


def convert_path(original_path, original_file_name):
    base_path, dir_name = os.path.split(dir_path)
    original_file_name, file_ext = os.path.splitext(original_file_name)

    new_name = re.sub(pattern, replacer, dir_name) + file_ext
    new_name = dir_name + file_ext

    return os.path.join(target_dir, new_name)


for dir_path, dir_names, file_names in os.walk(source_dir):
    for original_name in file_names:
        original_path = os.path.join(dir_path, original_name)
        print(original_path)
        new_path = convert_path(dir_path, original_name)
        print(new_path + '\n')
        shutil.move(original_path, new_path)
