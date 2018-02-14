#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re

output = r"C:\Users\glago\Desktop\2.csv"
regex_for_human = re.compile(r',("\w{1,3} \d{1,3}|Перерыв|\d блок|Внеконкурс)')
regex_nums_only = re.compile(r',"\w{1,3} \d{1,3}')

regex = regex_for_human

def proc(text):
    ret = ''
    for string in text.split('\n'):
        if re.search(regex, string):
            ret += string + '\n'
    #open(output, 'w', encoding='utf-8').write(ret)
    #os.startfile(output, 'open')
    print(ret)
    

proc(open(r"C:\Users\glago\Desktop\festival_plan.csv", encoding='utf-8').read())


# r"(^\d{2}:\d{2}\t.*?), интермедия.*?$" -> r"\n\1"
# ( \d{3}), -> \1.