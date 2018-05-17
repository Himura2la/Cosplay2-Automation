import os
import re
from random import randrange


for dirpath, dirnames, filenames in os.walk(r"D:\Clouds\YandexDisk\Fests\АтомКосКон2018\src"):
    for filename in filenames:
        old_filename = filename
        print(filename)
        filename = re.sub(r"^(\d{1}\.)", r"00\1", filename)
        filename = re.sub(r"^(\d{2}\.)", r"0\1", filename)

        # filename = re.sub(r"^0(\d{2})", r"\1", filename)
        # filename = '%03d. %s' % (randrange(100), filename)
        print(filename + '\n')

        os.rename(os.path.join(dirpath, old_filename), os.path.join(dirpath, filename))
