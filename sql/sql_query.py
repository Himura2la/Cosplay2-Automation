#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sqlite3
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("--sql", help='Path to an SQL request to run', required=True)
parser.add_argument("--db_path", help='Path to the database (overrides config)')
parser.add_argument("-o", help='File to save the result into')
parser.add_argument("--format", help='Output format. Possible values: "long" (default), "csv"', default='long')
parser.add_argument("--long_col", help='In "long" format specifies the column with long data. Default: "text"', default='text')
args = parser.parse_args()

# For header formatting in long_col 
field_format = {'number': "№%s. "}
default_field_format = "%s: "
last_field_format = "%s"

db_path = args.db_path
if not db_path:
    from yaml import load, FullLoader
    root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    config = load(open(os.path.join(root, 'config.yml'), 'r', encoding='utf-8').read(), Loader=FullLoader)
    db_path = config['db_path']

print('Connecting to %s...' % os.path.abspath(db_path))

with sqlite3.connect(db_path, isolation_level=None) as db:
    c = db.cursor()
    c.execute('PRAGMA encoding = "UTF-8"')
    c.execute(open(args.sql, encoding='utf-8').read())
    print('Fetching data...')
    result = c.fetchall()
    headers = [description[0] for description in c.description]
    print('Closing the database...')

result_txt = ""

if args.format == 'long':
    long_i = headers.index(args.long_col) if args.long_col in headers else None
    for record in result:
        if not record[1]:
            continue
        if long_i:
            result_txt += f"{os.linesep}{os.linesep}## "
            for i, field in enumerate(headers):
                if i != long_i:
                    fmt = field_format[field] if field in field_format \
                                                else last_field_format if i >= len(headers) - 2 \
                                                else default_field_format
                    result_txt += fmt % record[i]
            result_txt += f"{os.linesep}{record[long_i]}"
        else:
            for i, field in enumerate(headers):
                result_txt += f"{field}: {record[i]}{os.linesep}"
        result_txt = result_txt.replace('\\n', os.linesep)
        result_txt += os.linesep

    print(result_txt)

    if args.o:
        open(args.o, 'w', encoding='utf-8').write(result_txt)
        print("Saved to %s" % os.path.abspath(args.o))



if args.format == 'csv':
    import csv
    json_i = headers.index("json")
    headers.pop(json_i)
    headers.append('notes')
    
    with open(args.o, 'w', newline='', encoding='utf=8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for record in result:
            if not record[1]:
                continue
            row = list(record)
            description =  json.loads(row.pop(json_i))
            notes = description['request']['notes']
            row.append(notes)
            writer.writerow(row)

