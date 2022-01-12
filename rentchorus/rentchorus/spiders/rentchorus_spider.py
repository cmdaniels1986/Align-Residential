import scrapy
from rentchorus.items import RentchorusItem

from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
import time 

class RentchorusSpiderSpider(scrapy.Spider):
    name = 'rentchorus_spider'
    allowed_domains = ['rentchorus.com/']
    start_urls = ['https://sightmap.com/embed/0n9w6r13w71']

    def parse(self, response):
        pass
