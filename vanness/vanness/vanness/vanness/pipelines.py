# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from vanness.items import VannessItem
import datetime

class VannessPipeline:
    def process_item(self, item, spider):

        availability = item['availability']
        if availability == 'Available Now' or availability == 'Available Now ':
            item['availability'] = datetime.date.today()
        else:
            try:
                item['availability'] = datetime.datetime.strptime(item['availability'], '%B %d, %Y')
            except:
                item['availability'] = datetime.datetime.strptime(item['availability'], '%B %d, %Y ')
        item['unit_id'] = item['unit_id'].replace('#','').replace(' - ','-')
        # datecrawled = scrapy.Field()  
        # domain = scrapy.Field()  
        # url = scrapy.Field()      
        # property = scrapy.Field()  
        # address = scrapy.Field()
        # availability = scrapy.Field()  
        bedbath_raw = item['bedbath_raw'].replace('Studio', '0').replace('  ', ' ').replace('  ', ' ').replace('  ', ' ').strip().split(' ')
        item['beds'] = bedbath_raw[1]
        item['baths'] = bedbath_raw[3]
        # beds = scrapy.Field()
        # baths = scrapy.Field() 
        # features_raw = scrapy.Field()  
        item['size'] = item['size'].replace(',','') 
        item['monthly_price'] = item['monthly_price'].replace('$','').replace('*','').replace(',','') 
        # price_min = scrapy.Field()  
        # price_max = scrapy.Field()           
        # occupancy = scrapy.Field()  
        # pets = scrapy.Field()  
        # terms = scrapy.Field()  
        # units = scrapy.Field()  
        # offer = scrapy.Field()  
        item['bedsxbaths'] = item['beds'] + 'x' + item['baths']
        item['address'] = '150 Van Ness Avenue'
        item['city'] = 'San Francisco'
        item['state'] = 'CA'
        
        return item
