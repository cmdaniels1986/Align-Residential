import scrapy
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
import time 

from equityapartments.items import EquityapartmentsItem
from datetime import datetime

class EquityapartmentsSpiderSpider(scrapy.Spider):
    name = 'equityapartments_spider'
    allowed_domains = ['www.equityapartments.com']
    start_urls = ['https://www.equityapartments.com/san-francisco/design-district/one-henry-adams-apartments##unit-availability-tile']

    def parse(self, response):
        #Use Selenium to get the lazy loading banner
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(r'C:\Users\cmdan\Desktop\Spiders\chromedriver.exe', options=chrome_options)
        driver.get(response.request.url)
        time.sleep(5)
        # Clicked Button
        try:
            python_button = driver.find_elements_by_xpath('//p[starts-with(@ng-show,"!vm.BedroomTypes")]')[0]
            python_button.click()
            time.sleep(3)
        except:
            pass

        sel = Selector(text=driver.page_source)        

        units = sel.xpath('//div[@class="col-xs-12 unit-expanded-card"]/div[@class="row"]')
        property = sel.xpath('//h1[@itemprop="name"]/text()').extract_first()
        address = sel.xpath('//span[@itemprop="streetAddress"]/text()').extract_first()
        city = sel.xpath('//span[@itemprop="addressLocality"]/text()').extract_first()
        state = sel.xpath('//span[@itemprop="addressRegion"]/text()').extract_first()
        # address = address + ', ' + sel.xpath('//span[@itemprop="postalCode"]/text()').extract_first()
        for unit in units:

            item = EquityapartmentsItem()
            monthly_price = unit.xpath('.//div[@class="col-xs-4 specs"]/p/span[@class="pricing ng-binding"]/text()').extract_first()
            terms = unit.xpath('.//div[@class="col-xs-4 specs"]/p/span[@class="time-period ng-binding"]/text()').extract_first()
            bedbath_raw = unit.xpath('.//div[@class="col-xs-4 specs"]/p[@class="ng-binding"]/text()').extract_first().strip() + ' ' + unit.xpath('.//div[@class="col-xs-4 specs"]/p[@class="ng-binding"]/text()').extract()[1].strip()
            size = unit.xpath('.//div[@class="col-xs-4 specs"]/p[@class="ng-binding"]/span/text()').extract_first()
            availability = unit.xpath('.//div[@class="col-xs-4 specs"]/p[@ng-show="true"]/text()').extract_first().strip()
                  
            ini_str = unit.xpath('.//div[@class="col-xs-3 ctas"]/div/div/a/@href').extract_first()
            
            try:
                offer = offer = unit.xpath('.//div[@class="col-xs-4 specs"]/div[@class="special-offer"]/p/text()').extract_first().strip()        
            except:
                offer = ''
            # # Finding nth occurrence of substring 
            val = -1
            # for i in range(0, 9): 
            #     val = ini_str.find('/', val + 1) 
            # unit_id = ini_str[val + 1:val+4]
            # unit_id = unit_id.replace('/guestcard/b4213/tour#/booktourunit/newtour/0/1/N/','')
            # unit_id = unit_id[0:unit_id.find('/')]
            # Start Getting Unit ID
            start = ini_str.find('ApartmentID=')
            end = ini_str.find('Term=')
            unit_id = ini_str[start+12:end-1]

            item['unit_id'] = unit_id
            item['datecrawled'] = datetime.now()
            item['domain'] = EquityapartmentsSpiderSpider.allowed_domains
            item['url'] = response.request.url
            item['availability'] = availability
            item['bedbath_raw'] = bedbath_raw
            item['size'] = size
            item['monthly_price'] = monthly_price
            item['property'] = property
            item['address'] = address
            item['city'] = city
            item['state'] = state
            item['pets'] = 'Pet Friendly'
            item['offer'] = offer
            
            yield item

        driver.quit()
