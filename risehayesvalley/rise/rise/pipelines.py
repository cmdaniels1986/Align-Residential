# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from rise.items import RiseItem
import datetime

class RisePipeline:
    def process_item(self, item, spider):

        availability = item['availability']
        if availability == 'Available Now':
            item['availability'] = datetime.date.today()
        else:
            item['availability'] = datetime.datetime.strptime(item['availability'].strip(), '%m/%d/%Y')

        item['unit_id'] = item['unit_id'].replace('# ','')
        # datecrawled = scrapy.Field()  
        # domain = scrapy.Field()  
        # url = scrapy.Field()      
        # property = scrapy.Field()  
        # address = scrapy.Field()
        # availability = scrapy.Field()  
        bedbath_raw = item['bedbath_raw'].replace('Studio', '0 Bedroom').strip().split(' ')
        item['beds'] = bedbath_raw[0]
        item['baths'] = bedbath_raw[2]
        # beds = scrapy.Field() 
        # baths = scrapy.Field() 
        # features_raw = scrapy.Field()  
        item['size']  = item['size'].replace('Upto ','').replace(' sqft', '')
        item['monthly_price'] = item['monthly_price'].replace('Starting at : ','').replace('$','').replace(',','')
        # price_min = scrapy.Field()  
        # price_max = scrapy.Field()           
        # occupancy = scrapy.Field()  
        # pets = scrapy.Field()  
        # terms = scrapy.Field()  
        # units = scrapy.Field()  
        # offer = scrapy.Field() 
        return item
