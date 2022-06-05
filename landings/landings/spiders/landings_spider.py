import scrapy

from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
import time 
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from landings.items import LandingsItem
from datetime import datetime

class LandingsSpiderSpider(scrapy.Spider):
    name = 'landings_spider'
    allowed_domains = ['thelandingsf.com']
    start_urls = ['https://sightmap.com/embed/ryzvg8k1pln']

    def parse(self, response):
        #Use Selenium to get the lazy loading banner
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        # driver = webdriver.Firefox(executable_path=r"C:\Users\cmdan\Desktop\Spiders\geckodriver.exe")
        driver = webdriver.Chrome(r'C:\Users\cmdan\OneDrive\Desktop\Spiders\chromedriver.exe')

        #First Find Special on Apartments.com
        # driver.get('https://www.apartments.com/33-tehama-san-francisco-ca/eqzek7p/')
        # time.sleep(5)
        # sel = Selector(text=driver.page_source) 
        # offer = sel.xpath('//div[@class="moveInSpecialsContainer"]/p/text()').extract_first()
        offer = ""
        driver.get(response.request.url)
        time.sleep(5)

        sel = Selector(text=driver.page_source) 

        expand = driver.find_elements_by_xpath('//table[@class="css-vpcorb-FloorSelectTable e1bwchys6"]/tbody/tr')
        for i in range(0, len(expand)): 
            expand[i].click()
            sel = Selector(text=driver.page_source) 
            count = sel.xpath('//span[@class="list-results-label-number"]/text()').extract_first().strip()
            
            if count != '0':
                units = sel.xpath('//div[@class="list-item css-tq0h9w-UnitList"]')
                for unit in units:

                    item = LandingsItem()
                    item['unit_id'] = unit.xpath('.//a/span[@class="line"]/span/text()').extract_first().replace('APT ','')

                    text = unit.xpath('.//a/span[@class="line secondary-font css-1u8xyim-UnitList"]/text()').extract_first() 
                    textlist = text.split(' / ')
                    item['bedbath_raw'] = textlist[0] + ' ' + textlist[1]
                    item['size'] = textlist[2]
                    try:
                        text1 = unit.xpath('.//a/span[@class="line secondary-font css-1u8xyim-UnitList"]/text()').extract()[1]
                        textlist1 = text1.split(' / ')
                        item['monthly_price'] = textlist1[0]
                        # item['terms'] = textlist1[1]
                        try:
                            item['availability'] = unit.xpath('.//a/span[@class="line secondary-font css-1u8xyim-UnitList"]/text()').extract()[2]
                        except:
                            item['availability'] = ""
                        item['property'] = 'The Landing'
                        item['address'] = '33 Tehama St'
                        item['address'] = 'San Francisco'
                        item['address'] = 'CA'
                        item['datecrawled'] = datetime.now()
                        item['domain']  = LandingsSpiderSpider.allowed_domains
                        item['url'] = response.request.url
                    except:
                        text1 = ""
                    yield item 