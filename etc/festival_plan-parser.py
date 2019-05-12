#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Author: Himura Kazuto <himura@tulafest.ru>

import os
import sys
import csv
from xml.etree import ElementTree

festival_plan_xls = r"%USERPROFILE%\Desktop\festival_plan.xls" if len(sys.argv) < 2 else sys.argv[1]
out_dir = os.path.split(festival_plan_xls)[0]

xls_contents = open(festival_plan_xls, encoding='utf-8-sig').read()
xls_contents = xls_contents.split('<body>', 1)[1].replace(' style="""', '').replace('&', '&amp;')  # баги в вёрстке :(
# open(os.path.join(out_dir, 'xls_contents.html'), 'w', encoding='utf-8').write(xls_contents)  # на случай новых багов
table = ElementTree.XML(xls_contents)

plan = []
for row in iter(table):
    time_cell, data_cell = row
    if not time_cell.text:
        tag = data_cell[0].tag
        time = time_cell[0].text
        val = data_cell[0].text
    else:
        tag = None
        time = time_cell.text
        val = data_cell.text
    plan.append((tag, time, val))

human_plan = ''
technical_plan = []
for row in plan[2:]:  # Отрезаем День и Место
    tag, time, val = row
    if tag == 'b':  # Доп. инфа
        human_plan += f'\n{time} {val}:\n'
        technical_plan.append((val, '', '', '', ''))
    elif tag is None:  # Номер
        human_plan += f"{time} {val.replace(',', '.', 1)}\n"
        code, title = val.split(', ', 1)
        code, num = code.split(' ', 1)
        technical_plan.append(('', time, code, num, title))
    else:
        raise Exception("Unexpected tag in cell: <%s>" % tag)

open(os.path.join(out_dir, 'human_plan.txt'), 'w', encoding='utf-8').write(human_plan)
with open(os.path.join(out_dir, 'technical_plan.csv'), 'w', newline='', encoding='utf=8') as f:
    writer = csv.writer(f)
    writer.writerow(['info', 'time', 'code', 'num', 'voting_title'])
    writer.writerows(technical_plan)
