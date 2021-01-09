import os
import re
from random import randrange

def replacer(match):
    return match.string.replace(f"{match[1]}.", f"{139 + int(match[2])}.")


for dirpath, dirnames, filenames in os.walk(r"/media/data/Events/Gakko 12/Gakko_Выступающие/135. №0-10 (Сценка (с микрофонами) КВН)"):
    for filename in filenames:
        old_filename = filename
        print(filename)
        # filename = re.sub(r"^(\d{1}\.)", r"00\1", filename)
        # filename = re.sub(r"^(\d{2}\.)", r"0\1", filename)

        # filename = re.sub(r"^0(\d{2})", r"\1", filename)
        # filename = '%03d. %s' % (randrange(100), filename)

        filename = re.sub(r"^(\d{3}).*Трек (\d{3}).*", replacer, filename)

        print(filename + '\n')

        os.rename(os.path.join(dirpath, old_filename), os.path.join(dirpath, filename))
