# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from vara.items import VaraItem
import datetime

class VaraPipeline:
    def process_item(self, item, spider):
        
        availability = item['availability']
        if availability == 'Now':
            item['availability'] = datetime.date.today()
        else:
            item['availability'] = datetime.datetime.strptime(item['availability'], "%b %d, %Y")

        # unit_id = scrapy.Field()  
        # datecrawled = scrapy.Field()  
        # domain = scrapy.Field()  
        # url = scrapy.Field()      
        # property = scrapy.Field()  
        # address = scrapy.Field()
        # availability = scrapy.Field()  
        bedbath_raw = item['bedbath_raw'].replace('Studio', 'Bed 0 Baths 1').split(' ')
        item['beds'] = bedbath_raw[1]
        item['baths'] = bedbath_raw[3]
        # beds = scrapy.Field() 
        # baths = scrapy.Field() 
        # features_raw = scrapy.Field()  
        item['size'] = item['size'].replace(',','') 
        # monthly_price = scrapy.Field()  
        prices = item['price_min'].replace('$','').replace(',','').replace('/month','').replace('-','').split(' ')
        item['price_min'] = prices[0]
        item['price_max'] = prices[1]        
        # occupancy = scrapy.Field()  
        # pets = scrapy.Field()  
        # terms = scrapy.Field()  
        # units = scrapy.Field()  
        # offer = scrapy.Field() 

        return item
