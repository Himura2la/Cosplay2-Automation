import os
import pickle
import sqlite3

db_name = 'sqlite3_data.db'

with open('event_name.txt', 'r') as f:
    event_name = f.read()

data = dict()

for file in os.listdir(event_name):
    if file.split('.')[1] == 'pickle':
        with open(os.path.join(event_name, file), 'rb') as f:
            data[file.split('.')[0]] = pickle.load(f)

print('Connecting to ' + db_name + '...')

db = sqlite3.connect(os.path.join(event_name, db_name), isolation_level=None)
c = db.cursor()

c.execute('PRAGMA encoding = "UTF-8"')
c.execute("PRAGMA synchronous = OFF")

print("Populating settings...")

c.execute("DROP TABLE IF EXISTS settings")
c.execute("CREATE TABLE settings (key TEXT PRIMARY KEY, value TEXT)")
c.executemany("INSERT INTO settings (key, value) VALUES(?,?)", data['settings']['event'].items())

print("Populating list...")

c.execute("DROP TABLE IF EXISTS list")
c.execute("""CREATE TABLE list (
id INTEGER PRIMARY KEY, card_code INTEGER, title TEXT, category TEXT, card_enabled INTEGER, card_name_rule TEXT,
card_announcement_rule TEXT, card_diplom_rule TEXT, default_duration REAL, description TEXT, event_id INTEGER,
intro TEXT, "order" INTEGER, print_badges INTEGER, public_requests TEXT, time_addons_close TEXT, time_cards_open TEXT,
time_requests_close TEXT, time_requests_open TEXT, time_voting_close TEXT, time_voting_open TEXT, url_code TEXT,
voting_group INTEGER, voting_jury INTEGER, voting_public INTEGER)
""")
c.executemany("INSERT INTO list (id, card_code, title, category, card_enabled, card_name_rule, card_announcement_rule, "
              "card_diplom_rule, default_duration, description, event_id, intro, 'order', print_badges, "
              "public_requests, time_addons_close, time_cards_open, time_requests_close, time_requests_open, "
              "time_voting_close, time_voting_open, url_code, voting_group, voting_jury, voting_public) "
              "VALUES(:id, :card_code, :title, :category, :card_enabled, :card_name_rule, "
              ":card_announcement_rule, :card_diplom_rule, :default_duration, :description, :event_id, :intro, :order, "
              ":print_badges, :public_requests, :time_addons_close, :time_cards_open, :time_requests_close, "
              ":time_requests_open, :time_voting_close, :time_voting_open, :url_code, :voting_group, :voting_jury, "
              ":voting_public)", data['list'])

print("Populating requests...")

c.execute("DROP TABLE IF EXISTS requests")
c.execute("""CREATE TABLE requests (
id INTEGER PRIMARY KEY, voting_title TEXT, status TEXT, topic_id INTEGER, number INTEGER, comment_time TEXT,
image_update_time TEXT, new_comments INTEGER, new_updates INTEGER, update_time TEXT, user_id INTEGER, user_title TEXT,
voting_number INTEGER)
""")
c.execute("BEGIN TRANSACTION")
c.executemany("INSERT INTO requests (id, voting_title, status, topic_id, number, comment_time, image_update_time, "
              "new_comments, new_updates, update_time, user_id, user_title, voting_number) "
              "VALUES(:id, :voting_title, :status, :topic_id, :number, :comment_time, :image_update_time, "
              ":new_comments, :new_updates, :update_time, :user_id, :user_title, :voting_number)", data['requests'])
c.execute("COMMIT")

print("Populating values...")

c.execute("DROP TABLE IF EXISTS 'values'")
c.execute("""CREATE TABLE 'values' (
id INTEGER PRIMARY KEY AUTOINCREMENT, request_id INT, request_section_id INT, section_title TEXT, title TEXT,
value TEXT, type TEXT, public INTEGER, max_repeat INTEGER)
""")
c.execute("BEGIN TRANSACTION")
c.executemany("INSERT INTO 'values' (request_id, request_section_id, section_title, title, value, "
              "type, public, max_repeat) "
              "VALUES(:request_id, :request_section_id, :section_title, :title, :value, "
              ":type, :public, :max_repeat)", data['values'])
c.execute("COMMIT")

db.commit()
db.close()

print("All done! Happy SQL\'ing!")
