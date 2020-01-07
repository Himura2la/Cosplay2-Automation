
import os
import re

d = "C:\\Users\\himura\\Desktop\\чб конкурс"
pattern = '385%s. конкурс чб - %s'
r = re.compile('(.+)(\.\w+)')

data = """
амнезия орион
затана дс комиксф
веном человек паук
кот сильвестр загадочные истории
микки маус
безликий унесенные призраками
шелдон купер теория большого взрыва эффект доллера
круэлла де виль
крик очень страшное кино
по кунг фу панда
мисаки президент студсовета горничная
кид соул итер
денни призрак денни
мартин мадагаскар
бетти буп
битлджюс 
слендермен
джек кошмар перед рождеством
монокума Данганронпа - Школа надежды и безнадёжные школьники
""".split('\n')

for _, f in enumerate(os.listdir(d)):
    name, ext = r.match(f).groups()
    i = int(name)
    ch = chr(ord('a') + i - 1)
    title = f'{name}. {data[i]}'
    new_name = pattern % (ch, title) + ext
    print(f'{f}->{new_name}')
    old_path = os.path.join(d, f)
    new_path = os.path.join(d, new_name)
    os.rename(old_path, new_path)
