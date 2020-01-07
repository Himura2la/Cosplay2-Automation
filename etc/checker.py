import os
import sqlite3
import re
from yaml import load, FullLoader

configfile = open("config.yml", "r")
config = load(configfile.read(), Loader=FullLoader)
configfile.close()
db_name = config['db_path']
event_name = config['event_name']
id_regex = re.compile(re.escape(config['id_regex']))
code_regex = re.compile(re.escape(config['code_regex']))
files_folder = os.path.join(config['festengine_path'],'mp3')

data = dict()

print('Connecting to ' + db_name + '...')

db = sqlite3.connect(db_name, isolation_level=None)
c = db.cursor()

c.execute('PRAGMA encoding = "UTF-8"')

c.execute("SELECT value FROM settings WHERE key='id'")
event_id = int(c.fetchone()[0])

c.execute(config['checker_sql'])

def split_name(name):
    res = re.search(code_regex, name)
    if res is not None:
        return res.groups()
    else:
        print("[WARNING] Unknown file '%s'" % name)
        return None, None, None, None

items = c.fetchall()
files = list(map(split_name, os.listdir(files_folder)))

nums_all = {int(number) for _, _, number, _, _, _ in items}
nums_exist = {int(number) for _, _, _, number in files if number is not None}

nums_absent = nums_all - nums_exist  # The whole program in a single line

for card_code, voting_number, number, nom, voting_title, req_id in items:
    if number in nums_absent:
        print ('[ABSENT] {0} {1} №{2}. ({3}) {4} [http://{5}.cosplay2.ru/orgs/requests/request/{6}]'.format(card_code, voting_number, number, nom, voting_title, event_name, req_id))

