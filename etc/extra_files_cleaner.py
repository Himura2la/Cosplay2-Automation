import os
from send2trash import send2trash  # pip install Send2Trash


for dirpath, dirnames, filenames in os.walk(r"D:\Fests Local\Yuki no Odori 7\Files\tulafest"):
    for filename in filenames:
        if 'Фото' in filename:
            path = os.path.join(dirpath, filename)
            print(path)
            send2trash(path)
            print('Bye')