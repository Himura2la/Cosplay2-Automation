#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import re

output = r"C:\Users\glago\Desktop\2.csv"
regex_all = re.compile(r",(\w{1,3} \d{1,3}|Перерыв|\d блок|Внеконкурс)")
regex_nums_only = re.compile(r',"\w{1,3} \d{1,3}')

regex = regex_nums_only

def proc(text):
    ret = ''
    for string in text.split('\n'):
        if re.search(regex, string):
            ret += string + '\n'
    open(output, 'w', encoding='utf-8').write(ret)
    os.startfile(output, 'open')
    

proc(open(r"C:\Users\glago\Desktop\festival_plan.csv", encoding='utf-8').read())
