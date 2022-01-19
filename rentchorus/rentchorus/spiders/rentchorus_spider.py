import scrapy
from rentchorus.items import RentchorusItem

from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
import time 
from datetime import datetime

class RentchorusSpiderSpider(scrapy.Spider):
    name = 'rentchorus_spider'
    allowed_domains = ['rentchorus.com/']
    start_urls = ['https://sightmap.com/embed/0n9w6r13w71']

    def parse(self, response):
        #Use Selenium to get the lazy loading banner
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        # driver = webdriver.Firefox(executable_path=r"C:\Users\cmdan\Desktop\Spiders\geckodriver.exe")
        driver = webdriver.Chrome(r'C:\Users\cmdan\Desktop\Spiders\chromedriver.exe', options=chrome_options)
        
        offer = ""
        driver.get(response.request.url)
        time.sleep(5)

        sel = Selector(text=driver.page_source) 

        expand = driver.find_elements_by_xpath('//div[@class="css-1yypv1x-FloorHorizontalItemWrapper e47b5d90"]/li')
        for i in range(0, len(expand)): 
            expand[i].click()
            sel = Selector(text=driver.page_source) 
            count = sel.xpath('//span[@class="list-results-label-number"]/text()').extract_first().replace(' Units','')
            print(count)
            if count != '0':
                print('Got here')
                units = sel.xpath('//div[@class="list-item css-ehwxqh-UnitList"]')
                for unit in units:
                    item = RentchorusItem()
                    item['unit_id'] = unit.xpath('.//a/span[@class="line"]/span/text()').extract_first().replace('APT ', '')
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
                        item['property'] = 'Chorus'
                        item['address'] = '30 Otis St.'
                        item['address'] = 'San Francisco'
                        item['address'] = 'CA'
                        item['datecrawled'] = datetime.now()
                        item['domain']  = 'rentchorus.com'
                        item['url'] = response.request.url
                    except:
                        text1 = ""
                    
                    yield item 
        driver.quit
