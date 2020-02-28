import os
import sqlite3
from glob import glob
from datetime import datetime
from yaml import load, FullLoader
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import (DAILY, DateFormatter, rrulewrapper, RRuleLocator, drange)

db_dirs = [
    r"C:\Users\himura\Desktop\yno8-backups",
    r"C:\Users\himura\Desktop\yno9-backups"
]
queries = {
    'scene': 'select count(*) from list, requests where list.id = topic_id and default_duration > 0 and card_code not like "V%"',
    'etickets': 'select count(*) from etickets where money_transfered not null'
}
line_colors = ['b.', 'r.', 'k.', 'g.']

data = {}
for d in db_dirs:
    fest_info = None
    for f in glob(os.path.join(d, '*.db')):
        results = {}
        date = datetime.strptime(os.path.split(f)[1], '%y-%m-%d_%H-%M-%S.db')
        with sqlite3.connect(f, isolation_level=None) as db:
            c = db.cursor()
            c.execute('PRAGMA encoding = "UTF-8"')
            if not fest_info:
                c.execute('select * from settings where key in ("short_title", "start_time")')
                fest_info = { k: v for k, v in c.fetchall() }
                fest_info['start_time'] = datetime.strptime(fest_info['start_time'], '%d.%m.%y %H:%M')
            for query_name, query in queries.items():
                c.execute(query)
                result, = c.fetchone()
                results[f'{fest_info["short_title"]}-{query_name}'] = result
        days_to_fest = int((date - fest_info['start_time']).days)
        if days_to_fest > 0:
            break
        if not days_to_fest in data:
            data[days_to_fest] = results
        else:
            for dataset in results:
                data[days_to_fest][dataset] = results[dataset]

fig, ax = plt.subplots()
x = list(data.keys())
datasets = data[x[0]].keys()
for i, name in enumerate(datasets):
    ax.plot(x, [v[name] if name in v else None for k, v in data.items()], line_colors[i])
ax.grid()
ax.set_xlabel('Дней до феста')
ax.legend(datasets)
plt.show()
