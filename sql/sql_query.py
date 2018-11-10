#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sqlite3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--db_path", help='Path to the database', required=True)
parser.add_argument("--sql", help='Path to an SQL request to run', required=True)
parser.add_argument("-o", help='File to save the result into')
parser.add_argument("--format", help='Output format. Possible values: "raw" (default), "long"', default='raw')
parser.add_argument("--long_col", help='In "long" format specifies the column with long data. Default: "value"', default='value')
args = parser.parse_args()

# For header formatting in long_col 
field_format = {'number': "№%s. "}
default_field_format = "%s: "
last_field_format = "%s"

print('Connecting to %s...' % os.path.abspath(args.db_path))
result, headers = [], []
with sqlite3.connect(args.db_path, isolation_level=None) as db:
    c = db.cursor()
    c.execute('PRAGMA encoding = "UTF-8"')
    c.execute(open(args.sql, encoding='utf-8').read())
    print('Fetching data...')
    result = c.fetchall()
    headers = [description[0] for description in c.description]
    print('Closing the database...')

result_txt = ""

if args.format == 'raw':
    result_txt = str([headers] + result)

elif args.format == 'long':
    long_i = headers.index(args.long_col) if args.long_col in headers else None
    for record in result:
        if long_i:
            result_txt += "%s%s## " % (os.linesep, os.linesep)
            for i, field in enumerate(headers):
                if i != long_i:
                    fmt = field_format[field] if field in field_format \
                                                else last_field_format if i >= len(headers) - 2 \
                                                else default_field_format
                    result_txt += fmt % record[i]
            result_txt += "%s%s" % (os.linesep, record[long_i])
        else:
            for i, field in enumerate(headers):
                result_txt += "%s: %s%s" % (field, record[i], os.linesep)
        result_txt += os.linesep

print(result_txt)

if args.o:
    open(args.o, 'w', encoding='utf-8').write(result_txt.replace('\\n', os.linesep))
    print("Saved to %s" % os.path.abspath(args.o))
