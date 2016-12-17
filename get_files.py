import os

import sqlite3

from get_data import Authenticator


class Downloader:
    def __init__(self, db_path, img_folder, mp3_folder, art_folder):
        self.__img_folder = img_folder
        self.__mp3_folder = mp3_folder
        self.__art_folder = art_folder
        self.images = None
        self.files = None
        self.art = None
        self.event_id = None

        self.__get_lists(db_path)
        pass

    def __get_lists(self, db_path):
        print('Connecting to ' + db_path + '...')

        db = sqlite3.connect(db_path, isolation_level=None)
        c = db.cursor()

        c.execute('PRAGMA encoding = "UTF-8"')
        c.execute("SELECT value FROM settings WHERE key='id'")
        self.event_id = int(c.fetchone()[0])

        c.execute("""
        SELECT request_id,
               '№ '||number || '. ' || voting_title AS name,
               value
        FROM   [values], requests, list
        WHERE  list.id = topic_id AND
               request_id = requests.id AND
               type = 'image' AND
               [values].title LIKE 'Изображени%' AND
               status = 'approved'
        ORDER BY name
        """)
        self.images = c.fetchall()

        c.execute("""
        SELECT  request_id,
                '№ '||number || '. ' || voting_title AS name,
                value
        FROM 'values', requests, list
        WHERE   list.id = topic_id AND
                request_id = requests.id AND
                type = 'file' AND (
                'values'.title = 'Минус в формате mp3' OR
                'values'.title = 'Аудио-трек в формате mp3' OR
                'values'.title = 'Видеофайл' OR
                'values'.title = 'Аудио-трек в формате mp3 или видео') AND
                status = 'approved'
        ORDER BY name
        """)
        self.files = c.fetchall()

        c.execute("""
        SELECT request_id,
               card_code||' '||voting_number || ' №'||number || '. ' || voting_title AS name,
               value
        FROM 'values', requests, list
        WHERE   list.id = topic_id AND
                request_id = requests.id AND
                type = 'file' AND
                card_code IN ("A", "F") AND
                status = 'approved'
        ORDER BY name
        """)
        self.art = c.fetchall()

        db.close()
        print(db_path + ' was safely closed...')

    def __download_images(self):
        pass


if __name__ == "__main__":
    print()
    a = Authenticator()
    a.sign_in()

    db_path = os.path.join(a.event_name, 'sqlite3_data.db')
    folders = map(lambda x: os.path.join(a.event_name, x), ['img', 'mp3', 'art'])

    print()
    img_d = Downloader(db_path, *folders)
