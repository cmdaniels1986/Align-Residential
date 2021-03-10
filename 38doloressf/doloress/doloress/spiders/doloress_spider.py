import scrapy
from doloress.items import DoloressItem

from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
import time 

from datetime import datetime

class DoloressSpiderSpider(scrapy.Spider):
    name = 'doloress_spider'
    allowed_domains = ['38doloressf.securecafe.com']
    start_urls = ['https://38doloressf.securecafe.com/onlineleasing/38-dolores/floorplans']    

    def parse(self, response):

        #Use Selenium to get the lazy loading banner
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(r'C:\Users\cmdan\Desktop\Spiders\chromedriver.exe', options=chrome_options)
        driver.get(response.request.url)
        time.sleep(5)
        sel = Selector(text=driver.page_source)
        driver.quit()

        floorplans = sel.xpath('//div[@class="fp-card"]/div/a')
        address = sel.xpath('//span[@itemprop="address"]/span/text()').extract()[0] + ' ' + sel.xpath('//span[@itemprop="address"]/span/text()').extract()[1] + ' ' + sel.xpath('//span[@itemprop="address"]/span/text()').extract()[2] + ' ' + sel.xpath('//span[@itemprop="address"]/span/text()').extract()[3]
        domain = DoloressSpiderSpider.allowed_domains

        for floorplan in floorplans:
            url = floorplan.xpath('.//@href').extract_first()

            if url is not None:
                #  yield scrapy.Request(url,
                #                       callback=self.parse_building,
                #                       meta={'url': url,
                #                             'address': address})            
                driver_building = webdriver.Chrome(r'C:\Users\cmdan\Desktop\Spiders\chromedriver.exe', options=chrome_options)
                driver_building.get(url)
                time.sleep(5)
                sel_building = Selector(text=driver_building.page_source)
                driver_building.quit()
                apartments = sel_building.xpath('//div[@class="fp-availApt-Container"]')
                
                item = DoloressItem()

                if apartments is None:
                    item['unit_id'] = -1
                    item['datecrawled'] = datetime.now()
                    item['monthly_price'] = sel_building.xpath('//span[@class="promoPrice"]/text()').extract_first()
                    bedbath_raw = sel_building.xpath('//div[@class="single-fp-flexitem single-fp-type"]/text()').extract()[1].strip()
                    bedbath_raw = bedbath_raw + ' ' + sel_building.xpath('//div[@class="single-fp-flexitem single-fp-baths"]/text()').extract()[1].strip()    
                    item['bedbath_raw'] = bedbath_raw
                    item['size'] = sel_building.xpath('//div[@class="single-fp-flexitem single-fp-sqft"]/text()').extract()[1].strip()
                    item['occupancy'] = 0
                    item['property'] = '38 Dolores'
                    item['availability'] = 'Not Available'
                    
                    yield item


                
                for apartment in apartments:
                    item['url'] = url
                    item['address'] = address
                    item['domain'] = domain
                    item['availability'] = 'Available Now'
                    item['datecrawled'] = datetime.now()
                    item['property'] = '38 Dolores'
                    item['size'] = sel_building.xpath('//div[@class="single-fp-flexitem single-fp-sqft"]/text()').extract()[1].strip()
                    item['monthly_price']= apartment.xpath('.//span/text()').extract()[1]
                    item['unit_id'] = apartment.xpath('.//span/text()').extract()[0]
                    
                    bedbath_raw = sel_building.xpath('//div[@class="single-fp-flexitem single-fp-type"]/text()').extract()[1].strip()
                    bedbath_raw = bedbath_raw + ' ' + sel_building.xpath('//div[@class="single-fp-flexitem single-fp-baths"]/text()').extract()[1].strip()
                    item['bedbath_raw'] = bedbath_raw
                    yield item


                    
 


