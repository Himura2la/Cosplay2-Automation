import os
import re
import shutil


for dirpath, dirnames, filenames in os.walk(r"D:\Clouds\YandexDisk\Fests\Yuki no Odori 7\art_foto\Фотокосплей по номинациям"):
    for filename in filenames:
        old_filename = filename
        print(filename)
        filename = re.sub(r"^(\d{1}\.)", r"00\1", filename)
        filename = re.sub(r"^(\d{2}\.)", r"0\1", filename)
        print(filename + '\n')
        shutil.move(os.path.join(dirpath, old_filename),
                    os.path.join(dirpath, filename))