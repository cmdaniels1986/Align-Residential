import scrapy
from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
import time 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from tehama.items import TehamaItem
from datetime import datetime


class TehamaSpiderSpider(scrapy.Spider):
    name = 'tehama_spider'
    allowed_domains = ['33tehama.com']
    start_urls = ['https://sightmap.com/embed/4yjp2k1xpxl']
    # start_urls = ['https://sightmap.com/embed/ryzvg8k1pln']
    def parse(self, response):
        #Use Selenium to get the lazy loading banner
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        # driver = webdriver.Firefox(executable_path=r"C:\Users\cmdan\Desktop\Spiders\geckodriver.exe")
        driver = webdriver.Chrome(r'C:\Users\cmdan\Desktop\Spiders\chromedriver.exe', options=chrome_options)

        #First Find Special on Apartments.com
        driver.get('https://www.apartments.com/33-tehama-san-francisco-ca/eqzek7p/')
        time.sleep(5)
        sel = Selector(text=driver.page_source) 
        # offer = sel.xpath('//div[@class="moveInSpecialsContainer"]/p/text()').extract_first()
        offer = ""
        driver.get(response.request.url)
        time.sleep(5)



        sel = Selector(text=driver.page_source) 

        # property = sel.xpath('//img[@class="nav-logo-img"]/@alt').extract_first()
        # address = sel.xpath('//div[@class="address-wrapper"]/div/span/a/text()').extract_first()
        # address = address + ' ' + sel.xpath('//div[@class="address-wrapper"]/div/span[@style="margin-bottom: 8px"]/a/text()').extract_first()
                
        # driver.switch_to.frame('_hjRemoteVarsFrame')
        # driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
        # time.sleep(5) 

        # sel.xpath('//div[@class="css-1yypv1x-FloorHorizontalItemWrapper e47b5d90"]')
        
        expand = driver.find_elements_by_xpath('//div[@class="css-1yypv1x-FloorHorizontalItemWrapper e47b5d90"]/li')
        for i in range(0, len(expand)): 
            expand[i].click()
            sel = Selector(text=driver.page_source) 
            count = sel.xpath('//span[@class="list-results-label-number"]/text()').extract_first()
            if count != '0':
                units = sel.xpath('//div[@class="list-item css-tq0h9w-UnitList"]')
                for unit in units:
                    
                    item = TehamaItem()
                    item['unit_id'] = unit.xpath('.//a/span[@class="line"]/span/text()').extract_first()
                    text = unit.xpath('.//a/span[@class="line secondary-font css-12qnlfx-UnitList"]/text()').extract_first() 
                    textlist = text.split(' / ')
                    item['bedbath_raw'] = textlist[0] + ' ' + textlist[1]
                    item['size'] = textlist[2]
                    try:
                        text1 = unit.xpath('.//a/span[@class="line secondary-font css-12qnlfx-UnitList"]/text()').extract()[1]
                        textlist1 = text1.split(' / ')
                        item['monthly_price'] = textlist1[0]
                        # item['terms'] = textlist1[1]
                        try:
                            item['availability'] = unit.xpath('.//a/span[@class="line secondary-font css-12qnlfx-UnitList"]/text()').extract()[2]
                        except:
                            item['availability'] = ""
                        item['property'] = '33 Tehama'
                        item['address'] = '33 Tehama St'
                        item['address'] = 'San Francisco'
                        item['address'] = 'CA'
                        item['datecrawled'] = datetime.now()
                        item['domain']  = TehamaSpiderSpider.allowed_domains
                        item['url'] = response.request.url
                    except:
                        text1 = ""
                    
                    yield item 
        driver.quit
           
