#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sqlite3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("sql", help='Path to an SQL request to run')
parser.add_argument("-o", help='File to save the result into')
parser.add_argument("--format", help='Output format. Possible values: "long", "short" (default)', default='short')
args = parser.parse_args()

long_col = 'text'

# For header formatting in long_col 
field_format = {'number': "№%s. "}
default_field_format = "%s: "
last_field_format = "%s"

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

long_i = headers.index(long_col) if long_col in headers else None
for record in result:

    if long_i:
        result_txt += f"\n\n## "
        for i, field in enumerate(headers):
            if i != long_i:
                fmt = field_format[field] if field in field_format \
                                            else last_field_format if i >= len(headers) - 2 \
                                            else default_field_format
                result_txt += fmt % record[i]
        result_txt += f"\n{record[long_i]}"
    else:
        for i, field in enumerate(headers):
            if record[i]:
                result_txt += f"{(field + ': ') if args.format == 'long' else ''}{record[i]} \n"
    result_txt += os.linesep

print(result_txt)

css = """
<style>
    body {
        font-family:  Inter, sans-serif;
    }
    h2 {
        margin: 9pt 0 0 0;
        font-size: 15pt;
    }
    h3 {
        margin: 0 0 0 14pt;
        font-size: 12pt;
        font-style: italic;
    }
    p {
        margin: 0 0 0 0;
        font-size: 12pt;
    }
</style>
"""

if args.o:
    if args.o.endswith('.html'):
        try:
            import markdown
        except ImportError:
            pass
        else:
            result_txt = '<!DOCTYPE html><html>' \
                '<head><meta charset="utf-8">%s</head>' \
                '<body>%s</body></html>' % (css, markdown.markdown(result_txt))
    open(args.o, 'w', encoding='utf-8').write(result_txt)
    print("Saved to %s" % os.path.abspath(args.o))
