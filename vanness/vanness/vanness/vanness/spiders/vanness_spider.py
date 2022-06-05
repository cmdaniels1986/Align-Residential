import scrapy
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
import time 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from vanness.items import VannessItem
from datetime import datetime

class VannessSpiderSpider(scrapy.Spider):
    name = 'vanness_spider'
    allowed_domains = ['150vanness.com/availability']
    start_urls = ['https://150vanness.com/availability']

    def parse(self, response):
        #Use Selenium to get the lazy loading banner
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(r'C:\Users\cmdan\OneDrive\Desktop\Spiders\chromedriver.exe')
        driver.get(response.request.url)
        time.sleep(5)

        button = driver.find_element_by_xpath("//button[@class='banner-button']")
        button.click()
        time.sleep(5)

        driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
        button = driver.find_element_by_xpath("//button[@class='primary small ng-binding']")
        button.click()

        driver.switch_to.default_content()
        sel = Selector(text=driver.page_source) 

        item = VannessItem()        
        address = sel.xpath('//li[@class="address"]/address/span[@class="street"]/text()').extract_first().strip('\n')
        address = address + ' ' + sel.xpath('//li[@class="address"]/address/span[@class="city"]/text()').extract_first().strip('\n').replace('\n',' ')
        

        driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
        time.sleep(5)        

        #click first button 
        # driver.execute_script("window.scrollTo(0, 500)")
        # python_button = driver.find_element_by_xpath('//button[@class="primary small ng-binding"]')
        # python_button.click()

        # time.sleep(2)
 
        # python_button = driver.find_element_by_xpath('//a[@tab-index-loaded="true"]')
        # python_button.click()

        # time.sleep(2)

        #Start scraping Iframe        

        expand = driver.find_elements_by_xpath('//div[@class="floorplan-tile ng-scope"]/div[@class="tile-buttons"]/button')
        for i in range(0, len(expand)-1): 
            while False:
                try:           
                    # ActionChains(driver).move_to_element(expand[i]).perform()
                    driver.execute_script("return arguments[0].scrollIntoView();", expand[i])
                    driver.execute_script("window.scrollBy(0, -250);")
                    break
                except:
                    driver.execute_script("window.scrollTo(0, 100)")               
           
            time.sleep(2)            
            expand[i].click()
            time.sleep(2)

            sel = Selector(text=driver.page_source)           

            
            #Get values here
            try:
                test = sel.xpath('//tr/td[@class="ng-binding"]/text()').extract()[2]
            except:
                test = 'broken'

            #if sel.xpath('//tr/td[@class="ng-binding"]/text()').extract()[2] == 'Bedrooms':
            if test == 'Bedrooms':
                try:
                    #If this is the case, multi unit
                    bedbath_raw = 'Bedrooms ' + ' ' + sel.xpath('//tr/td[@class="ng-binding"]/text()').extract()[3] + ' Bathrooms ' + sel.xpath('//tr/td[@class="ng-binding"]/text()').extract()[5]
                    # bathrooms = sel.xpath('//tr/td[@class="ng-binding"]/text()').extract()[5]
                    size = sel.xpath('//tr/td[@class="ng-binding"]/text()').extract()[7]
                    occupancy = sel.xpath('//tr/td[@class="ng-binding"]/text()').extract()[9]

                    units = sel.xpath('//div[@class="radio-option"]')
                    for unit in units:
                        item['unit_id'] = unit.xpath('.//span/text()').extract()[0]
                        item['monthly_price'] = unit.xpath('.//span/text()').extract()[1]
                        item['availability'] = unit.xpath('.//span/text()').extract()[4]
                        item['datecrawled'] = datetime.now()
                        item['domain']  = VannessSpiderSpider.allowed_domains
                        item['url'] = response.request.url
                        item['bedbath_raw'] = bedbath_raw
                        item['size'] = size
                        item['occupancy'] = occupancy
                        item['address'] = address
                        item['property'] = '150 Van Ness'
                        
                        yield item
                except:
                    pass
            else:
                try:
                    item['bedbath_raw'] = 'Bedrooms ' + sel.xpath('//tr/td[@class="ng-binding"]/text()').extract()[5] + ' Bathrooms ' + sel.xpath('//tr/td[@class="ng-binding"]/text()').extract()[7]
                    #bathrooms = sel.xpath('//tr/td[@class="ng-binding"]/text()').extract()[7]
                    item['size'] = sel.xpath('//tr/td[@class="ng-binding"]/text()').extract()[9]
                    item['occupancy'] = sel.xpath('//tr/td[@class="ng-binding"]/text()').extract()[11]
                    item['terms'] = sel.xpath('//tr/td[@class="ng-binding"]/text()').extract()[13]
                    item['unit_id']  = sel.xpath('//div[@class="radio-option"]/span/text()').extract()[0]
                    item['availability'] = sel.xpath('//div[@class="radio-option"]/span/text()').extract()[4]
                    item['monthly_price'] = sel.xpath('//div[@class="radio-option"]/span/text()').extract()[1]
                    
                    item['datecrawled'] = datetime.now()
                    item['domain']  = VannessSpiderSpider.allowed_domains
                    item['url'] = response.request.url
                    
                    item['address'] = address
                    item['property'] = '150 Van Ness'

                    yield item
                except:
                    pass

                # yield item

            try:
                time.sleep(3)    
                python_button = driver.find_element_by_xpath('//span[@id="footer-back-button"]')
                python_button.click()
            except:
                pass
            time.sleep(3)    
            expand = driver.find_elements_by_xpath('//div[@class="floorplan-tile ng-scope"]/div[@class="tile-buttons"]/button')
            ActionChains(driver).move_to_element(driver.find_element_by_tag_name('html')).perform() 
            
                   
            
            
