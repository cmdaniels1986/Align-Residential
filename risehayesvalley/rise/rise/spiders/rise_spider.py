import scrapy
from rise.items import RiseItem
from datetime import datetime

from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
import time 

class RiseSpiderSpider(scrapy.Spider):
    name = 'rise_spider'
    allowed_domains = ['www.therisehayesvalley.com']
    start_urls = ['https://www.therisehayesvalley.com/floorplans']

    def parse(self, response):
        units = response.xpath('//*[@name="applynow"]')
        datecrawled = datetime.now()
        domain = RiseSpiderSpider.allowed_domains

        for unit in units:
            url = response.urljoin(unit.xpath('.//@href').extract_first())
            property = unit.xpath('.//@data-floorplan-name').extract_first()
            address = response.xpath('//div[@data-selenium-id="address_street"]/text()').extract_first().strip()
            address = address + ' ' + response.xpath('//*[@data-selenium-id="address_city"]/text()').extract_first() 
            address = address + ', ' + response.xpath('//*[@data-selenium-id="address_state"]/text()').extract_first()
            address = address + ', ' + response.xpath('//*[@data-selenium-id="address_zip"]/text()').extract_first()
            if url is not None:
                 yield scrapy.Request(url,
                                      callback=self.parse_building,
                                      meta={'url': url,
                                            'property': property,
                                            'datecrawled': datecrawled,
                                            'domain': domain,
                                            'address': address})

    def parse_building(self, response):
        url = response.meta['url']
        property = response.meta['property']
        datecrawled = response.meta['datecrawled']
        domain = response.meta['domain']
        address = response.meta['address']

        item = RiseItem()

        #Use Selenium to get the lazy loading banner
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(r'C:\Users\cmdan\Desktop\Spiders\chromedriver.exe', options=chrome_options)
        driver.get(url)
        time.sleep(5)
        sel = Selector(text=driver.page_source)
        item['offer'] = sel.xpath('//div[@class="holder-notification-message"]/span/text()').extract_first()
        driver.quit()
        # end Selenium        

        item['datecrawled'] = datecrawled
        item['address'] = address
        item['domain'] = domain
        item['url'] = url
        item['property'] = property
        item['bedbath_raw'] = response.xpath('//ul[@class="list-inline"]/li/text()').extract()[0] + response.xpath('//ul[@class="list-inline"]/li/text()').extract()[1] 
        item['size'] = response.xpath('//ul[@class="list-inline"]/li/text()').extract()[2]
        item['pets'] = response.xpath('//ul[@class="list-inline"]/li/text()').extract()[3]

        units = response.xpath('//div[@id="availApts"]/div')
        for unit in units:
            item['unit_id'] = unit.xpath('.//div/div/div/p/span/text()').extract_first()
            item['availability'] = unit.xpath('.//div/div/p[@class="card-subtitle mb-2 text-muted"]/text()').extract_first()
            item['monthly_price'] = unit.xpath('.//div/div/p[@class="card-subtitle mb-2 text-muted"]/span/text()').extract_first() 
            item['terms'] = 'Deposit: ' + response.xpath('//div/div/p/span/text()').extract()[1]
            
            # Overrides
            if item['availability'] != 'Available Now':
                item['availability'] = unit.xpath('.//div/div/p[@class="card-subtitle mb-2 text-muted"]/span/text()').extract_first()
                item['monthly_price'] = unit.xpath('.//div/div/p[@class="card-subtitle mb-2 text-muted"]/span/text()').extract()[1]

            yield item
            # features_raw = ''
            # occupancy = ''
            # units = ''
