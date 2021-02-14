import os
import sqlite3
import json
from glob import glob
from datetime import datetime
from yaml import load, FullLoader
from collections import Counter
import matplotlib.pyplot as plt
import math

root_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
config = load(
    open(os.path.join(root_dir, 'config.yml'), 'r', encoding='utf-8').read(),
    Loader=FullLoader)
db_path = config['db_path']

def get_request_created(json_string):
    data = json.loads(json_string)
    request_created_string = data['request']['creation_time']
    return datetime.fromisoformat(request_created_string)

def get_days_to_fest(moment, fest_start_time):
    return (moment - fest_start_time).days


with sqlite3.connect(db_path, isolation_level=None) as db:
    c = db.cursor()
    c.execute('PRAGMA encoding = "UTF-8"')
    c.execute('SELECT * FROM settings WHERE key IN ("short_title", "start_time")')
    fest_info = c.fetchall()
    c.execute("""
        SELECT json FROM list, requests, details
        WHERE list.id = topic_id
        AND requests.id = request_id
        AND default_duration > 0
    """)
    requests_details = c.fetchall()

fest_info = {k: v for k, v in fest_info}
fest_info['start_time'] = datetime.strptime(fest_info['start_time'], r'%d.%m.%y %H:%M')
requests = [get_days_to_fest(get_request_created(row[0]), fest_info['start_time']) for row in requests_details]

print(Counter(requests))

time_range = abs(min(requests) - max(requests))
n, bins, patches = plt.hist(x=requests, bins=time_range, color='#0504aa', alpha=0.7, rwidth=0.85)
plt.grid(axis='y', alpha=0.75)
plt.xlabel('Дней до феста')
plt.ylabel('Заявок подано')
plt.title(f'Гистограмма безответственности участникв {fest_info["short_title"]}')
plt.show()
