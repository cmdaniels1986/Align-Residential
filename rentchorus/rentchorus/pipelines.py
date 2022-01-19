# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from rentchorus.items import RentchorusItem
import datetime
# import time 

class RentchorusPipeline:
    def process_item(self, item, spider):
        availability = item['availability']
        if availability == 'Available Now':
            item['availability'] = datetime.date.today()
        else:
            item['availability'] = datetime.datetime.strptime(item['availability'].replace('Available ','').replace('st','').replace('nd','').replace('rd','').replace('th','') + ' ' + str(datetime.date.today().year), '%b %d %Y')
        # unit_id = scrapy.Field()  
        # datecrawled = scrapy.Field()  
        # domain = scrapy.Field()  
        # url = scrapy.Field()      
        # property = scrapy.Field()  
        # address = scrapy.Field()
        # availability = scrapy.Field()  
        bedbath_raw = item['bedbath_raw'].split(' ')
        item['beds'] = bedbath_raw[0].replace('Studio','1')
        item['baths'] = bedbath_raw[2].replace('Bath','1')
        # beds = scrapy.Field() 
        # baths = scrapy.Field() 
        # features_raw = scrapy.Field()  
        item['size'] = item['size'].replace(' sq. ft.','').replace(',','')
        item['monthly_price'] = item['monthly_price'].replace('$','').replace(',','')
        # price_min = scrapy.Field()  
        # price_max = scrapy.Field()           
        # occupancy = scrapy.Field()  
        # pets = scrapy.Field()  
        # terms = scrapy.Field()  
        # units = scrapy.Field()  
        # offer = scrapy.Field() 
        item['bedsxbaths'] = item['beds'] + 'x' + item['baths']
        item['address'] = '30 Otis St.'
        item['city'] = 'San Francisco'
        item['state'] = 'CA'

        item['uniqueidentifier'] = item['property'] + '_' +item['unit_id']
        item['domain']  = 'rentchorus.com'
        # item['datecrawled'] = datetime.now()
        return item
