from urllib.request import urlopen
from html.parser import HTMLParser
import csv

class CharacterLoader(HTMLParser):
    page_url = "https://myanimelist.net/character.php"

    def __init__(self):
        super().__init__()
        self.in_table = False
        self.in_row = False
        self.in_column = False
        self.in_jp = False
        self.response = [[]]

        

    def load(self, limit):
        with urlopen(self.page_url + f"?limit={limit}") as response:
            page = response.read().decode("utf8")
        self.feed(page)
        return self.response

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            for k, v in attrs:
                if k == 'class' and v == 'characters-favorites-ranking-table':
                    self.in_table = True
        if self.in_table and tag == 'tr':
            for k, v in attrs:
                if k == 'class' and v in ('ranking-list'):
                    self.in_row = True
        if self.in_row and tag == 'td':
            for k, v in attrs:
                if k == 'class' and v.strip() in ('rank', 'character', 'people', 'favorites'):
                    self.in_column = True
        if self.in_row and tag == 'span':
            for k, v in attrs:
                if k == 'class' and v == 'fs12 fn-grey6':
                    self.in_jp = True
        

    def handle_endtag(self, tag):
        if tag == 'table':
            self.in_table = False
        if self.in_table and tag == 'tr':
            self.in_row = False
            self.response.append([])
        if self.in_row and tag == 'td':
            self.in_column = False
        if self.in_row and tag == 'span':
            self.in_jp = False

    def handle_data(self, data):
        data = data.strip()
        if data == "":
            return
        if self.in_column and not self.in_jp:
            self.response[-1].append(data)



full_list = []

for skip in range(0, 1050, 50):  # 
    print("loading", skip)
    loader = CharacterLoader()
    data = loader.load(skip)
    full_list += data
    print("full_list: ", len(full_list))

with open('anime_characters.csv', 'w', newline='', encoding='utf=8') as f:
    writer = csv.writer(f)
    writer.writerows(full_list)
