import os
import sqlite3


class MakeDB(object):
    def __init__(self, db_path, data):
        self.__db_path = db_path
        self.data = data

        fest_dir = os.path.split(self.__db_path)[0]
        if not os.path.isdir(fest_dir):
            print('Making fest dir...')
            os.makedirs(fest_dir)
        
        if os.path.isfile(self.__db_path):
            print('Deleting old database...')
            os.remove(self.__db_path)

        print('Connecting to ' + self.__db_path + '...')
        db = sqlite3.connect(self.__db_path, isolation_level=None)
        cursor = db.cursor()
        cursor.execute('PRAGMA encoding = "UTF-8"')
        cursor.execute("PRAGMA synchronous = OFF")

        for key in data.keys():
            if self.__make_schema(key, cursor):
                if not self.__populate(key, cursor):
                    print("ERROR in '%s'" % key)
            else:
                print("No schema for '%s'. Add the schema to `%s:__make_schema()` function." % (key, __file__))

        db.commit()
        db.close()

        print("All done! Happy SQL'ing!")

    @staticmethod
    def __make_schema(key, c):
        print("Making '%s' table schema..." % key)
        if key == 'settings':
            c.execute("DROP TABLE IF EXISTS settings")
            c.execute("CREATE TABLE settings (key TEXT PRIMARY KEY, value TEXT)")
        elif key == 'list':
            c.execute("DROP TABLE IF EXISTS list")
            c.execute("""CREATE TABLE list (
            id INTEGER PRIMARY KEY, card_code INTEGER, title TEXT, category TEXT, card_enabled INTEGER, card_name_rule TEXT,
            card_announcement_rule TEXT, card_diplom_rule TEXT, default_duration REAL, description TEXT, event_id INTEGER,
            intro TEXT, `order` INTEGER, print_badges INTEGER, public_requests TEXT, time_addons_close TEXT,
            time_cards_open TEXT, time_requests_close TEXT, time_requests_open TEXT, time_voting_close TEXT,
            time_voting_open TEXT, url_code TEXT, voting_group INTEGER, voting_jury INTEGER, voting_public INTEGER)""")
        elif key == 'requests':
            c.execute("DROP TABLE IF EXISTS requests")
            c.execute("""CREATE TABLE requests (
            id INTEGER PRIMARY KEY, voting_title TEXT, announcement_title TEXT, status TEXT, topic_id INTEGER,
            number INTEGER, comment_time TEXT, image_update_time TEXT, new_comments INTEGER, new_updates INTEGER,
            update_time TEXT, user_id INTEGER, user_title TEXT, voting_number INTEGER)""")
        elif key == 'values':
            c.execute("DROP TABLE IF EXISTS `values`")
            c.execute("""CREATE TABLE `values` (
            id INTEGER PRIMARY KEY AUTOINCREMENT, request_id INTEGER, request_section_id INTEGER,
            section_title TEXT, title TEXT, value TEXT, type TEXT, public INTEGER, max_repeat INTEGER)""")
        elif key == 'etickets':
            c.execute("DROP TABLE IF EXISTS etickets")
            c.execute("""CREATE TABLE etickets (
            id TEXT PRIMARY KEY, user_id INTEGER, fio TEXT, city TEXT, email TEXT, mobile TEXT,
            etickets_type_id INTEGER, etickets_paymethod TEXT, money_transfered INTEGER, pay_time TEXT,
            pay_details TEXT, time_create TEXT, user_title TEXT, user_city TEXT, image_update_time TEXT, ett_title TEXT
            )""")
        elif key == 'details':
            c.execute("DROP TABLE IF EXISTS details")
            c.execute("CREATE TABLE details (id INTEGER PRIMARY KEY AUTOINCREMENT, request_id INTEGER, json TEXT)")
        else:
            return False
        return True

    def __populate(self, key, c):
        print("Populating '%s' table..." % key)
        if not self.data[key]:
            print("'%s' is empty!" % key)
            return False
        elif type(self.data[key]) is dict:
            c.executemany("INSERT INTO %s (key, value) VALUES(?,?)" % key, self.data['settings']['event'].items())
            return True
        elif type(self.data[key]) is list:
            keys = sorted(self.data[key][0].keys())

            rows = '[' + '], ['.join(keys) + ']'
            values = ':' + ', :'.join(keys)

            c.execute("BEGIN TRANSACTION")
            c.executemany("INSERT INTO `%s` (%s) VALUES(%s)" % (key, rows, values), self.data[key])
            c.execute("COMMIT")
            return True
        else:
            print("WTF just happened ???")
            return False

