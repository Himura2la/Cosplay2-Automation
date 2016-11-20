import os
import pickle
import sqlite3

with open('event_name.txt', 'r') as f:
    event_name = f.read()

data = dict()

for file in os.listdir(event_name):
    if file.split('.')[1] == 'pickle':
        with open(os.path.join(event_name, file), 'rb') as f:
            data[file.split('.')[0]] = pickle.load(f)

db = sqlite3.connect(os.path.join(event_name, "sqlite3_data.db"), isolation_level=None)
c = db.cursor()

c.execute("PRAGMA encoding = \"UTF-8\"")

c.execute("DROP TABLE IF EXISTS settings")
c.execute("CREATE TABLE settings (key TEXT PRIMARY KEY, value TEXT)")
c.executemany("INSERT INTO settings (key, value) VALUES(?,?)", data['settings']['event'].items())

db.commit()
db.close()