import os
import re
import shutil
from random import randrange


for dirpath, dirnames, filenames in os.walk(r"H:\Intermedia"):
    for filename in filenames:
        old_filename = filename
        print(filename)
        #filename = re.sub(r"^(\d{1}\.)", r"00\1", filename)
        #filename = re.sub(r"^(\d{2}\.)", r"0\1", filename)
        filename = re.sub(r"^0(\d{2})", r"\1", filename)
        print(filename + '\n')
        shutil.move(os.path.join(dirpath, old_filename), os.path.join(dirpath, filename))