import scrapy


class LandingsSpiderSpider(scrapy.Spider):
    name = 'landings_spider'
    allowed_domains = ['thelandingsf.com']
    start_urls = ['https://sightmap.com/embed/ryzvg8k1pln']

    def parse(self, response):
        pass
