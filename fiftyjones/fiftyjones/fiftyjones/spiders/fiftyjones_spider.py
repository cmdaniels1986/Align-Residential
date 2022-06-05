import scrapy
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
import time 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from fiftyjones.items import FiftyjonesItem
from datetime import datetime


class FiftyjonesSpiderSpider(scrapy.Spider):
    name = 'fiftyjones_spider'
    allowed_domains = ['www.50jones.com']
    start_urls = ['https://50jones.com/availability/']

    def parse(self, response):
        #Use Selenium to get the lazy loading banner
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(r'C:\Users\cmdan\OneDrive\Desktop\Spiders\chromedriver.exe')
        driver.get(response.request.url)
        time.sleep(5)

        sel = Selector(text=driver.page_source) 

        # offer = sel.xpath('//div[@class="usnb-message"]/div/text()').extract_first().strip()
        property = sel.xpath('//div[@class="footer-contact-body"]/strong/text()').extract_first()
        address = sel.xpath('//span[@itemprop="streetAddress"]/text()').extract_first().strip()
        address = address + ' ' + sel.xpath('//span[@itemprop="addressLocality"]/text()').extract_first().strip()
        address = address + ', ' + sel.xpath('//span[@itemprop="addressRegion"]/text()').extract_first().strip()
        address = address + ' ' + sel.xpath('//span[@itemprop="postalCode"]/text()').extract_first().strip()

        #Begin the scrolling
        expand = driver.find_elements_by_xpath('//button[@class="details-control"]')
        for i in expand:
            ActionChains(driver).move_to_element(i).perform()
            driver.execute_script("return arguments[0].scrollIntoView();", i)
            driver.execute_script("window.scrollBy(0, -250);")
            # time.sleep(1)
            i.click()
            #scroll to top of page to reset
            ActionChains(driver).move_to_element(driver.find_element_by_tag_name('html')).perform()

        sel = Selector(text=driver.page_source) 

        units = sel.xpath('//table[@class="dataTable no-footer"]/tbody/tr[@role="row"]')

        item = FiftyjonesItem()
        for unit in units:
            item['bedbath_raw'] = unit.xpath('.//td/text()').extract_first()
            item['size'] = unit.xpath('.//td/text()').extract()[1]
            item['monthly_price'] = unit.xpath('.//td/text()').extract()[2]
            # item['offer'] = offer
            item['property'] = property
            item['address'] = address
            try: 
                item['availability'] = unit.xpath('.//td/div[@class="availability-table-data"]/div/text()').extract_first()
            except:
                item['availability'] = 'Call'    
            item['unit_id'] = unit.xpath('.//td/span/text()').extract_first()
            item['datecrawled'] = datetime.now()
            item['domain']  = FiftyjonesSpiderSpider.allowed_domains
            item['url'] = response.request.url
            
            yield item


    # features_raw = scrapy.Field()  
    # price_min = scrapy.Field()  
    # price_max = scrapy.Field()           
    # occupancy = scrapy.Field()  
    # pets = scrapy.Field()  
    # terms = scrapy.Field()  
    # units = scrapy.Field()  
