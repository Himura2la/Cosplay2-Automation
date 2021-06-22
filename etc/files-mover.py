import os
import shutil
import re

source_dir = r"D:\Events\ATOMCOSCON 2021\Fest\Images"
pattern = re.compile(r"^(\d{3})(\. .+)")

target_dir = source_dir
if not os.path.exists(target_dir): os.makedirs(target_dir)

extra_data = {'150':'Сразу','160':'Сразу','170':'Сразу','200':'Сразу','210':'Сразу','220':'Сразу','230':'Стафф+сразу','240':'Сразу','250':'Сразу','260':'Сразу','270':'С точки','280':'Сразу','290':'С точки','300':'Сразу','310':'С точки','320':'Сразу','330':'Сразу','340':'Сразу','350':'Сразу','360':'Сразу','370':'Сразу','380':'Стафф+сразу','390':'С точки','400':'Сразу','410':'Сразу','420':'С точки','430':'С точки','440':'С точки','450':'Сразу','460':'Сразу','470':'Стафф+сразу','480':'Сразу','490':'Стафф+сразу','500':'Сразу','510':'Сразу','520':'Сразу','530':'Сразу','540':'Сразу','550':'Стафф+сразу','560':'Сразу','570':'Сразу','580':'Сразу','590':'Сразу','600':'Сразу','610':'Сразу','620':'С точки','630':'Сразу','640':'Сразу','650':'Сразу','660':'Сразу','670':'Сразу','680':'Сразу','690':'Стафф+с точки','700':'Сразу','710':'Стафф+сразу','720':'Сразу','730':'С точки','740':'Сразу','750':'Сразу','760':'Стафф+сразу','770':'Сразу','780':'С точки','790':'Сразу','800':'Сразу','810':'Сразу','820':'Стафф+сразу','830':'С точки','840':'Сразу','850':'Сразу','860':'Сразу','870':'Стафф+сразу'}


def replacer(match):
    return match[1] + '. ' +  extra_data[match[1]] +  match[2] 


def convert_path(original_path, original_name):
    base_path, dir_name = os.path.split(dir_path)
    original_name, file_ext = os.path.splitext(original_name)

    new_name = re.sub(pattern, replacer, original_name) + file_ext
    #new_name = dir_name + file_ext

    return os.path.join(target_dir, new_name)


for dir_path, dir_names, file_names in os.walk(source_dir):
    for original_name in file_names:
        original_path = os.path.join(dir_path, original_name)
        print(original_path)
        new_path = convert_path(dir_path, original_name)
        print(new_path + '\n')
        shutil.move(original_path, new_path)
