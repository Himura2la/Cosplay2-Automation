# -*- coding: utf-8 -*-

import csv
import os
import markdown

csv_input = r"C:\Users\glago\Desktop\ToFu Fest Участники - Информация о номерах.csv"
long_cols_start_at = 3

with open(csv_input, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    head = reader.__next__()
    rows = [{head[i]: row[i].strip() for i in range(len(head))} for row in reader]

md = ""
html_output = os.path.splitext(csv_input)[0] + '.html'

for row in rows:
    for i, (col, val) in enumerate(row.items()):
        if val:
            if i == 0:
                md += f"\n\n## {val}\n\n"
            elif i > long_cols_start_at:
                md += f"\n### {col}\n{val}\n"
            else:
                md += f"* **{col}**: {val}\n"

html = markdown.markdown(md)
with open(html_output, 'w', encoding='utf-8') as f:
    f.write(html)
