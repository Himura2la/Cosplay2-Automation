from urllib.request import urlopen
import scrapy
import csv


class LastFmTagSpider(scrapy.Spider):
    name = 'rock_bands'
    start_urls = ['https://www.last.fm/tag/rock/artists']
    add_header = True

    def csv_store(self, bands_list):
        mode = 'w' if self.add_header else 'a'
        with open('rock_bands.csv', mode, newline='', encoding='utf=8') as f:
            writer = csv.writer(f)
            if self.add_header:
                writer.writerow(['artist', 'avatar', 'listeners', 'bio'])
                self.add_header = False
            writer.writerow(bands_list)


    def parse(self, response):
        for card in response.css('div.big-artist-list-item'):
            bio = card.css('.big-artist-list-bio p::text').get()
            self.csv_store([
                card.css('.big-artist-list-title a::text').get().strip(),
                card.css('.big-artist-list-avatar-desktop img::attr(src)').get().strip(),
                card.css('.big-artist-list-listeners::text').get().strip().replace(',', ''),
                bio.strip() if bio else ''
            ])

        next_page = response.css('li.pagination-next a::attr(href)').extract_first()
        yield response.follow(next_page, self.parse)


