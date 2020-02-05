import os
import sqlite3
from glob import glob
from datetime import datetime
from yaml import load, FullLoader
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.dates import (DAILY, DateFormatter, rrulewrapper, RRuleLocator, drange)

db_dirs = {
    'yno8': r"C:\Users\himura\Desktop\yno8-backups",
    'yno9': r"C:\Users\himura\Desktop\yno9-backups"
}
queries = {
    'scene': 'select count(*) from list, requests where list.id = topic_id and default_duration > 0 and card_code not like "V%"'
#    'etickets': 'select count(*) from etickets where money_transfered not null'
}
line_colors = ['-b', '-r']

# TODO: count days to fest

data = {}
for fest, d in db_dirs.items():
    for f in glob(os.path.join(d, '*.db')):
        dir_path = os.path.join(d, f)
        results = {}
        date = datetime.strptime(f.rsplit('\\', 1)[1], '%y-%m-%d_%H-%M-%S.db')
        with sqlite3.connect(f, isolation_level=None) as db:
            c = db.cursor()
            c.execute('PRAGMA encoding = "UTF-8"')
            for name, query in queries.items():
                c.execute(query)
                result, = c.fetchone()
                results[f'{fest}-{name}'] = result
            data[date] = (date, results)

fig, ax = plt.subplots()
x = list(data.keys())
for i, name in enumerate(data[x[0]][1].keys()):
    ax.plot_date(x, [v[name] for k, v in data.values()], line_colors[i])
ax.xaxis.set_major_formatter(DateFormatter(f'%d.%m'))
ax.xaxis.set_major_locator(RRuleLocator(rrulewrapper(DAILY, interval=7)))
ax.xaxis.set_tick_params(rotation=30)
ax.grid()
ax.legend(queries.keys())
plt.show()
