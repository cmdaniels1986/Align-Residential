import scrapy
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
import time 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


from greystar.items import GreystarItem
from datetime import datetime

class GreystarSpiderSpider(scrapy.Spider):
    name = 'greystar_spider'
    allowed_domains = ['www.greystar.com']
    start_urls = ['https://www.greystar.com/properties/san-francisco-ca/duboce-apartments/floorplans']

    def parse(self, response):
        
        #Use Selenium to get the lazy loading banner
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(r'C:\Users\cmdan\OneDrive\Desktop\Spiders\chromedriver.exe')
        driver.get(response.request.url)
        time.sleep(10)
        while True:
            try:
                ActionChains(driver).move_to_element(driver.find_element_by_xpath('//a[@ng-click="loadMore()"]')).perform()
                ActionChains(driver).send_keys(Keys.DOWN).perform()
                ActionChains(driver).send_keys(Keys.DOWN).perform()
                ActionChains(driver).send_keys(Keys.DOWN).perform()
                ActionChains(driver).send_keys(Keys.DOWN).perform()
                ActionChains(driver).send_keys(Keys.DOWN).perform()         
                # Clicked Button                              
                python_button = driver.find_element_by_xpath('//a[@ng-click="loadMore()"]')
                python_button.click()
                time.sleep(5)
            except:
                break
        sel = Selector(text=driver.page_source) 

        property = sel.xpath('//h1[@itemprop="name"]/text()').extract_first()
        address = sel.xpath('//span[@itemprop="streetAddress"]/text()').extract_first()
        city = sel.xpath('//span[@itemprop="addressLocality"]/text()').extract_first()
        state = sel.xpath('//span[@itemprop="addressRegion"]/text()').extract_first()
        #address = address + ', ' + sel.xpath('//span[@itemprop="postalCode"]/text()').extract_first()
        floorplans = sel.xpath('//a[@aria-label="View Available"]')

        for floorplan in floorplans:            
            url = response.urljoin(floorplan.xpath('.//@href').extract_first())
            driver.get(url)
            time.sleep(5)
            sel = Selector(text=driver.page_source)

            while True:
                try:
                    ActionChains(driver).move_to_element(driver.find_element_by_xpath('//a[@title="Load more link"]')).perform()
                    ActionChains(driver).send_keys(Keys.DOWN).perform()
                    ActionChains(driver).send_keys(Keys.DOWN).perform()
                    ActionChains(driver).send_keys(Keys.DOWN).perform()
                    ActionChains(driver).send_keys(Keys.DOWN).perform()
                    time.sleep(5)
                    python_button = python_button = driver.find_element_by_xpath('//a[@title="Load more link"]')
                    python_button.click()
                    time.sleep(3)

                    sel = Selector(text=driver.page_source)
                except:
                    break
            bedbath_raw = sel.xpath('.//span[@class="rooms"]/span/text()').extract_first().strip()
            units = sel.xpath('//li[@class="cols ng-scope"]')
            for unit in units:
                item = GreystarItem()

                item['unit_id'] = unit.xpath('.//div[@class="apt-number"]/span/text()').extract_first()
                item['url'] = url
                item['datecrawled'] = datetime.now()
                item['domain']  = GreystarSpiderSpider.allowed_domains
                item['property'] = property
                item['address'] = address
                item['availability'] = unit.xpath('.//div[@class="date"]/span/text()').extract_first()
                item['size'] = unit.xpath('.//div[@class="sq-ft"]/span/text()').extract_first()
                item['monthly_price'] = unit.xpath('.//div[@class="rent"]/span/text()').extract_first()
                item['terms'] = unit.xpath('.//div[@class="deposit"]/span/text()').extract_first()
                item['bedbath_raw'] = bedbath_raw
                
                yield item              
                                   
                 
                # features_raw = scrapy.Field()  
                # price_min = scrapy.Field()  
                # price_max = scrapy.Field()           
                # occupancy = scrapy.Field()  
                # pets = scrapy.Field()   
                # units = scrapy.Field()  
                # offer = scrapy.Field() 

        driver.quit()