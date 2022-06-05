import scrapy
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
import time 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

import selenium.webdriver.support.ui as ui

from vara.items import VaraItem
from datetime import datetime


class VaraSpiderSpider(scrapy.Spider):
    name = 'vara_spider'
    allowed_domains = ['www.vara-sf.com']
    start_urls = ['https://www.vara-sf.com/san-francisco/vara/conventional/']

    def parse(self, response):
        #Use Selenium to get the lazy loading banner
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        # driver = webdriver.Firefox(executable_path=r"C:\Users\cmdan\Desktop\Spiders\geckodriver.exe")
        driver = webdriver.Chrome(r'C:\Users\cmdan\OneDrive\Desktop\Spiders\chromedriver.exe')     
        driver.get(response.request.url)
        time.sleep(5)

        sel = Selector(text=driver.page_source) 

        #Get Special
        offer = sel.xpath('//h6[@class="special-title"]/text()').extract_first()

        tab0 = driver.find_element_by_xpath('//a[@id="fp-tab-0"]')
        tab0.click()

        # #TAB 1 Reserve Now
        exps_res1 = driver.find_elements_by_xpath('//ul[@id="floorplans-0"]/li[@class="fp-grid-item"]/ul[@class="fp-grid-links col-3  has-specials"]/li[@class="grid-link action"]/a[@data-title="Check Floor Plan Availability"]')
        if len(exps_res1) == 0:
            exps_res1 = driver.find_elements_by_xpath('//ul[@id="floorplans-0"]/li[@class="fp-grid-item"]/ul[@class="fp-grid-links col-3 "]/li[@class="grid-link action"]/a[@data-title="Check Floor Plan Availability"]')
        for i in range(0, len(exps_res1)): 
            item = VaraItem()
            time.sleep(5)
            ActionChains(driver).move_to_element(exps_res1[i]).perform()
            driver.execute_script("window.scrollBy(0, 250);")

            exps_res1[i].click()
            time.sleep(5)
            sel = Selector(text=driver.page_source)
            
            units = sel.xpath('//div[@class="unit-row-wrapper"]')
            bedbath_raw = 'Bed ' + sel.xpath('//li[@class="fp-stats-item modal-beds"]/span[@class="stat-value"]/text()').extract_first() + ' baths ' + sel.xpath('//li[@class="fp-stats-item modal-baths"]/span[@class="stat-value"]/text()').extract_first()
            price_min = sel.xpath('//li[@class="fp-stats-item rent"]/span[@class="stat-value"]/text()').extract_first()
            price_max = sel.xpath('//li[@class="fp-stats-item rent"]/span[@class="stat-value"]/text()').extract_first()
            
            for unit in units:
                item['unit_id'] = unit.xpath('.//div/span/text()').extract()[1]
                item['monthly_price'] = unit.xpath('.//div[@class="unit-col select"]/a/@data-rent').extract_first() 
                item['size'] = unit.xpath('.//div/span/text()').extract()[5]
                item['terms'] = unit.xpath('.//div/span/text()').extract()[7]
                item['availability'] = unit.xpath('.//div/span/text()').extract()[10]
                item['datecrawled'] = datetime.now()
                item['domain']  = VaraSpiderSpider.allowed_domains
                item['url'] = response.request.url
                item['bedbath_raw'] = bedbath_raw
                item ['address'] = '1600 15th St San Francisco, CA 94103'
                item['property'] = 'VARA'
                item['price_min'] = price_min
                item['price_max'] = price_max
                item['offer'] = offer

                yield item
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()

        # #TAB 1 Available Future
        exps_res1 = driver.find_elements_by_xpath('//ul[@id="floorplans-0"]/li[@class="fp-grid-item"]/ul[@class="fp-grid-links col-2  has-specials"]/li[@class="grid-link action"]/a[@data-title="Check Floor Plan Availability"]')
        if len(exps_res1) == 0:
            exps_res1 = driver.find_elements_by_xpath('//ul[@id="floorplans-0"]/li[@class="fp-grid-item"]/ul[@class="fp-grid-links col-2 "]/li[@class="grid-link action"]/a[@data-title="Check Floor Plan Availability"]')
        for i in range(0, len(exps_res1)): 
            item = VaraItem()
            time.sleep(5)
            ActionChains(driver).move_to_element(exps_res1[i]).perform()
            driver.execute_script("window.scrollBy(0, 250);")

            exps_res1[i].click()
            time.sleep(5)
            sel = Selector(text=driver.page_source)
            
            units = sel.xpath('//div[@class="unit-row-wrapper"]')
            bedbath_raw = 'Bed ' + sel.xpath('//li[@class="fp-stats-item modal-beds"]/span[@class="stat-value"]/text()').extract_first() + ' baths ' + sel.xpath('//li[@class="fp-stats-item modal-baths"]/span[@class="stat-value"]/text()').extract_first()
            price_min = sel.xpath('//li[@class="fp-stats-item rent"]/span[@class="stat-value"]/text()').extract_first()
            price_max = sel.xpath('//li[@class="fp-stats-item rent"]/span[@class="stat-value"]/text()').extract_first()
            
            for unit in units:
                item['unit_id'] = unit.xpath('.//div/span/text()').extract()[1]
                item['monthly_price'] = unit.xpath('.//div[@class="unit-col select"]/a/@data-rent').extract_first() 
                item['size'] = unit.xpath('.//div/span/text()').extract()[5]
                item['terms'] = unit.xpath('.//div/span/text()').extract()[7]
                item['availability'] = unit.xpath('.//div/span/text()').extract()[10]
                item['datecrawled'] = datetime.now()
                item['domain']  = VaraSpiderSpider.allowed_domains
                item['url'] = response.request.url
                item['bedbath_raw'] = bedbath_raw
                item ['address'] = '1600 15th St San Francisco, CA 94103'
                item['property'] = 'VARA'
                item['price_min'] = price_min
                item['price_max'] = price_max
                item['offer'] = offer

                yield item
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(5)
        driver.execute_script("window.scrollBy(0, -10000);")

        tab1 = driver.find_element_by_xpath('//a[@id="fp-tab-1"]')
        tab1.click()

        # #TAB 2 Reserve Now
        exps_res1 = driver.find_elements_by_xpath('//ul[@id="floorplans-1"]/li[@class="fp-grid-item"]/ul[@class="fp-grid-links col-3  has-specials"]/li[@class="grid-link action"]/a[@data-title="Check Floor Plan Availability"]')
        if len(exps_res1)==0:
            exps_res1 = driver.find_elements_by_xpath('//ul[@id="floorplans-1"]/li[@class="fp-grid-item"]/ul[@class="fp-grid-links col-3 "]/li[@class="grid-link action"]/a[@data-title="Check Floor Plan Availability"]')
        for i in range(0, len(exps_res1)): 
            item = VaraItem()
            time.sleep(5)
            ActionChains(driver).move_to_element(exps_res1[i]).perform()
            driver.execute_script("window.scrollBy(0, 250);")

            exps_res1[i].click()
            time.sleep(5)
            sel = Selector(text=driver.page_source)
            
            units = sel.xpath('//div[@class="unit-row-wrapper"]')
            bedbath_raw = 'Bed ' + sel.xpath('//li[@class="fp-stats-item modal-beds"]/span[@class="stat-value"]/text()').extract_first() + ' baths ' + sel.xpath('//li[@class="fp-stats-item modal-baths"]/span[@class="stat-value"]/text()').extract_first()
            price_min = sel.xpath('//li[@class="fp-stats-item rent"]/span[@class="stat-value"]/text()').extract_first()
            price_max = sel.xpath('//li[@class="fp-stats-item rent"]/span[@class="stat-value"]/text()').extract_first()
            
            for unit in units:
                item['unit_id'] = unit.xpath('.//div/span/text()').extract()[1]
                item['monthly_price'] = unit.xpath('.//div[@class="unit-col select"]/a/@data-rent').extract_first() 
                item['size'] = unit.xpath('.//div/span/text()').extract()[5]
                item['terms'] = unit.xpath('.//div/span/text()').extract()[7]
                item['availability'] = unit.xpath('.//div/span/text()').extract()[10]
                item['datecrawled'] = datetime.now()
                item['domain']  = VaraSpiderSpider.allowed_domains
                item['url'] = response.request.url
                item['bedbath_raw'] = bedbath_raw
                item ['address'] = '1600 15th St San Francisco, CA 94103'
                item['property'] = 'VARA'
                item['price_min'] = price_min
                item['price_max'] = price_max
                item['offer'] = offer

                yield item
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()

        # #TAB 2 Available Future
        exps_res1 = driver.find_elements_by_xpath('//ul[@id="floorplans-1"]/li[@class="fp-grid-item"]/ul[@class="fp-grid-links col-2  has-specials"]/li[@class="grid-link action"]/a[@data-title="Check Floor Plan Availability"]')
        if len(exps_res1)==0:
             exps_res1 = driver.find_elements_by_xpath('//ul[@id="floorplans-1"]/li[@class="fp-grid-item"]/ul[@class="fp-grid-links col-2 "]/li[@class="grid-link action"]/a[@data-title="Check Floor Plan Availability"]')
        for i in range(0, len(exps_res1)): 
            item = VaraItem()
            time.sleep(5)
            ActionChains(driver).move_to_element(exps_res1[i]).perform()
            driver.execute_script("window.scrollBy(0, 250);")

            exps_res1[i].click()
            time.sleep(5)
            sel = Selector(text=driver.page_source)
            
            units = sel.xpath('//div[@class="unit-row-wrapper"]')
            bedbath_raw = 'Bed ' + sel.xpath('//li[@class="fp-stats-item modal-beds"]/span[@class="stat-value"]/text()').extract_first() + ' baths ' + sel.xpath('//li[@class="fp-stats-item modal-baths"]/span[@class="stat-value"]/text()').extract_first()
            price_min = sel.xpath('//li[@class="fp-stats-item rent"]/span[@class="stat-value"]/text()').extract_first()
            price_max = sel.xpath('//li[@class="fp-stats-item rent"]/span[@class="stat-value"]/text()').extract_first()
            
            for unit in units:
                item['unit_id'] = unit.xpath('.//div/span/text()').extract()[1]
                item['monthly_price'] = unit.xpath('.//div[@class="unit-col select"]/a/@data-rent').extract_first() 
                item['size'] = unit.xpath('.//div/span/text()').extract()[5]
                item['terms'] = unit.xpath('.//div/span/text()').extract()[7]
                item['availability'] = unit.xpath('.//div/span/text()').extract()[10]
                item['datecrawled'] = datetime.now()
                item['domain']  = VaraSpiderSpider.allowed_domains
                item['url'] = response.request.url
                item['bedbath_raw'] = bedbath_raw
                item ['address'] = '1600 15th St San Francisco, CA 94103'
                item['property'] = 'VARA'
                item['price_min'] = price_min
                item['price_max'] = price_max
                item['offer'] = offer

                yield item
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(5)
        driver.execute_script("window.scrollBy(0, -10000);")
        tab2 = driver.find_element_by_xpath('//a[@id="fp-tab-2"]')
        tab2.click()

        #TAB 3 Reserve Now
        exps_res1 = driver.find_elements_by_xpath('//ul[@id="floorplans-2"]/li[@class="fp-grid-item"]/ul[@class="fp-grid-links col-3  has-specials"]/li[@class="grid-link action"]/a[@data-title="Check Floor Plan Availability"]')
        if len(exps_res1)==0:
            exps_res1 = driver.find_elements_by_xpath('//ul[@id="floorplans-2"]/li[@class="fp-grid-item"]/ul[@class="fp-grid-links col-3 "]/li[@class="grid-link action"]/a[@data-title="Check Floor Plan Availability"]')
        for i in range(0, len(exps_res1)): 
            item = VaraItem()
            time.sleep(5)
            ActionChains(driver).move_to_element(exps_res1[i]).perform()
            driver.execute_script("window.scrollBy(0, 250);")

            exps_res1[i].click()
            time.sleep(5)
            sel = Selector(text=driver.page_source)
            
            units = sel.xpath('//div[@class="unit-row-wrapper"]')
            bedbath_raw = 'Bed ' + sel.xpath('//li[@class="fp-stats-item modal-beds"]/span[@class="stat-value"]/text()').extract_first() + ' baths ' + sel.xpath('//li[@class="fp-stats-item modal-baths"]/span[@class="stat-value"]/text()').extract_first()
            price_min = sel.xpath('//li[@class="fp-stats-item rent"]/span[@class="stat-value"]/text()').extract_first()
            price_max = sel.xpath('//li[@class="fp-stats-item rent"]/span[@class="stat-value"]/text()').extract_first()
            
            for unit in units:
                item['unit_id'] = unit.xpath('.//div/span/text()').extract()[1]
                item['monthly_price'] = unit.xpath('.//div[@class="unit-col select"]/a/@data-rent').extract_first() 
                item['size'] = unit.xpath('.//div/span/text()').extract()[5]
                item['terms'] = unit.xpath('.//div/span/text()').extract()[7]
                item['availability'] = unit.xpath('.//div/span/text()').extract()[10]
                item['datecrawled'] = datetime.now()
                item['domain']  = VaraSpiderSpider.allowed_domains
                item['url'] = response.request.url
                item['bedbath_raw'] = bedbath_raw
                item ['address'] = '1600 15th St San Francisco, CA 94103'
                item['property'] = 'VARA'
                item['price_min'] = price_min
                item['price_max'] = price_max
                item['offer'] = offer

                yield item
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()

        # #TAB 3 Available Future
        exps_res1 = driver.find_elements_by_xpath('//ul[@id="floorplans-2"]/li[@class="fp-grid-item"]/ul[@class="fp-grid-links col-2  has-specials"]/li[@class="grid-link action"]/a[@data-title="Check Floor Plan Availability"]')
        if len(exps_res1)==0:
            exps_res1 = driver.find_elements_by_xpath('//ul[@id="floorplans-2"]/li[@class="fp-grid-item"]/ul[@class="fp-grid-links col-2 "]/li[@class="grid-link action"]/a[@data-title="Check Floor Plan Availability"]')
        for i in range(0, len(exps_res1)): 
            item = VaraItem()
            time.sleep(5)
            ActionChains(driver).move_to_element(exps_res1[i]).perform()
            driver.execute_script("window.scrollBy(0, 250);")

            exps_res1[i].click()
            time.sleep(5)
            sel = Selector(text=driver.page_source)
            
            units = sel.xpath('//div[@class="unit-row-wrapper"]')
            bedbath_raw = 'Bed ' + sel.xpath('//li[@class="fp-stats-item modal-beds"]/span[@class="stat-value"]/text()').extract_first() + ' baths ' + sel.xpath('//li[@class="fp-stats-item modal-baths"]/span[@class="stat-value"]/text()').extract_first()
            price_min = sel.xpath('//li[@class="fp-stats-item rent"]/span[@class="stat-value"]/text()').extract_first()
            price_max = sel.xpath('//li[@class="fp-stats-item rent"]/span[@class="stat-value"]/text()').extract_first()
            
            for unit in units:
                item['unit_id'] = unit.xpath('.//div/span/text()').extract()[1]
                item['monthly_price'] = unit.xpath('.//div[@class="unit-col select"]/a/@data-rent').extract_first() 
                item['size'] = unit.xpath('.//div/span/text()').extract()[5]
                item['terms'] = unit.xpath('.//div/span/text()').extract()[7]
                item['availability'] = unit.xpath('.//div/span/text()').extract()[10]
                item['datecrawled'] = datetime.now()
                item['domain']  = VaraSpiderSpider.allowed_domains
                item['url'] = response.request.url
                item['bedbath_raw'] = bedbath_raw
                item ['address'] = '1600 15th St San Francisco, CA 94103'
                item['property'] = 'VARA'
                item['price_min'] = price_min
                item['price_max'] = price_max
                item['offer'] = offer

                yield item
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(5)
        driver.execute_script("window.scrollBy(0, -10000);")
        tab2 = driver.find_element_by_xpath('//a[@id="fp-tab-3"]')
        tab2.click()

        #TAB 4 Reserve Now
        exps_res1 = driver.find_elements_by_xpath('//ul[@id="floorplans-3"]/li[@class="fp-grid-item"]/ul[@class="fp-grid-links col-3  has-specials"]/li[@class="grid-link action"]/a[@data-title="Check Floor Plan Availability"]')
        if len(exps_res1) == 0:
            exps_res1 = driver.find_elements_by_xpath('//ul[@id="floorplans-3"]/li[@class="fp-grid-item"]/ul[@class="fp-grid-links col-3 "]/li[@class="grid-link action"]/a[@data-title="Check Floor Plan Availability"]')  
        for i in range(0, len(exps_res1)): 
            item = VaraItem()
            time.sleep(5)
            ActionChains(driver).move_to_element(exps_res1[i]).perform()
            driver.execute_script("window.scrollBy(0, 250);")

            exps_res1[i].click()
            time.sleep(5)
            sel = Selector(text=driver.page_source)
            
            units = sel.xpath('//div[@class="unit-row-wrapper"]')
            bedbath_raw = 'Bed ' + sel.xpath('//li[@class="fp-stats-item modal-beds"]/span[@class="stat-value"]/text()').extract_first() + ' baths ' + sel.xpath('//li[@class="fp-stats-item modal-baths"]/span[@class="stat-value"]/text()').extract_first()
            price_min = sel.xpath('//li[@class="fp-stats-item rent"]/span[@class="stat-value"]/text()').extract_first()
            price_max = sel.xpath('//li[@class="fp-stats-item rent"]/span[@class="stat-value"]/text()').extract_first()
            
            for unit in units:
                item['unit_id'] = unit.xpath('.//div/span/text()').extract()[1]
                item['monthly_price'] = unit.xpath('.//div[@class="unit-col select"]/a/@data-rent').extract_first() 
                item['size'] = unit.xpath('.//div/span/text()').extract()[5]
                item['terms'] = unit.xpath('.//div/span/text()').extract()[7]
                item['availability'] = unit.xpath('.//div/span/text()').extract()[10]
                item['datecrawled'] = datetime.now()
                item['domain']  = VaraSpiderSpider.allowed_domains
                item['url'] = response.request.url
                item['bedbath_raw'] = bedbath_raw
                item ['address'] = '1600 15th St San Francisco, CA 94103'
                item['property'] = 'VARA'
                item['price_min'] = price_min
                item['price_max'] = price_max
                item['offer'] = offer

                yield item
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()

        # #TAB 4 Available Future
        exps_res1 = driver.find_elements_by_xpath('//ul[@id="floorplans-3"]/li[@class="fp-grid-item"]/ul[@class="fp-grid-links col-2  has-specials"]/li[@class="grid-link action"]/a[@data-title="Check Floor Plan Availability"]')
        if len(exps_res1) == 0:
            exps_res1 = driver.find_elements_by_xpath('//ul[@id="floorplans-3"]/li[@class="fp-grid-item"]/ul[@class="fp-grid-links col-2 "]/li[@class="grid-link action"]/a[@data-title="Check Floor Plan Availability"]')
        for i in range(0, len(exps_res1)): 
            item = VaraItem()
            time.sleep(5)
            ActionChains(driver).move_to_element(exps_res1[i]).perform()
            driver.execute_script("window.scrollBy(0, 250);")

            exps_res1[i].click()
            time.sleep(5)
            sel = Selector(text=driver.page_source)
            
            units = sel.xpath('//div[@class="unit-row-wrapper"]')
            bedbath_raw = 'Bed ' + sel.xpath('//li[@class="fp-stats-item modal-beds"]/span[@class="stat-value"]/text()').extract_first() + ' baths ' + sel.xpath('//li[@class="fp-stats-item modal-baths"]/span[@class="stat-value"]/text()').extract_first()
            price_min = sel.xpath('//li[@class="fp-stats-item rent"]/span[@class="stat-value"]/text()').extract_first()
            price_max = sel.xpath('//li[@class="fp-stats-item rent"]/span[@class="stat-value"]/text()').extract_first()
            
            for unit in units:
                item['unit_id'] = unit.xpath('.//div/span/text()').extract()[1]
                item['monthly_price'] = unit.xpath('.//div[@class="unit-col select"]/a/@data-rent').extract_first() 
                item['size'] = unit.xpath('.//div/span/text()').extract()[5]
                item['terms'] = unit.xpath('.//div/span/text()').extract()[7]
                item['availability'] = unit.xpath('.//div/span/text()').extract()[10]
                item['datecrawled'] = datetime.now()
                item['domain']  = VaraSpiderSpider.allowed_domains
                item['url'] = response.request.url
                item['bedbath_raw'] = bedbath_raw
                item ['address'] = '1600 15th St San Francisco, CA 94103'
                item['property'] = 'VARA'
                item['price_min'] = price_min
                item['price_max'] = price_max
                item['offer'] = offer

                yield item
            ActionChains(driver).send_keys(Keys.ESCAPE).perform()


            
