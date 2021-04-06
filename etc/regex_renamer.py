import os
import re

path = r"/media/data/Temp/AnyWayFest/Tracks"
data = {'301':'сразу','304':'сразу','307':'сразу','310':'сразу','313':'сразу','316':'сразу','319':'сразу','322':'сразу','325':'сразу','328':'сразу','331':'сразу','334':'сразу','337':'сразу','340':'сразу','343':'сразу','346':'сразу','349':'сразу','352':'сразу','355':'сразу','358':'сразу','361':'сразу','364':'сразу','367':'сразу','370':'сразу','373':'сразу','376':'сразу','379':'сразу','382':'сразу','385':'сразу','388':'сразу','391':'сразу','394':'сразу','397':'сразу','400':'сразу','403':'сразу','406':'сразу','409':'сразу','412':'сразу','415':'сразу','418':'сразу','421':'сразу','424':'сразу','427':'сразу','430':'сразу','433':'сразу','436':'сразу','439':'сразу','442':'сразу','445':'сразу','448':'сразу','451':'сразу','454':'с точки','457':'сразу','460':'сразу','463':'сразу','466':'с точки','469':'сразу','472':'сразу','475':'сразу','478':'сразу','481':'сразу','484':'сразу','487':'сразу','490':'сразу','493':'сразу','496':'сразу','499':'сразу','502':'сразу','505':'сразу','508':'сразу','511':'сразу','514':'сразу','517':'сразу','520':'сразу','523':'сразу','526':'сразу','529':'сразу','532':'сразу'}
pattern = re.compile(r"^(\d{3})(\. .+)")

def replacer(match):
    return match[1] + '. ' + data[match[1]] + match[2]


for dirpath, dirnames, filenames in os.walk(path):
    for old_filename in filenames:
        print(old_filename)
        new_filename = re.sub(pattern, replacer, old_filename)
        print(new_filename + '\n')
        os.rename(os.path.join(dirpath, old_filename), os.path.join(dirpath, new_filename))
