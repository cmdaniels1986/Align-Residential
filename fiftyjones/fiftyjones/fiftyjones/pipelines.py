# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from fiftyjones.items import FiftyjonesItem
import datetime

class FiftyjonesPipeline:
    def process_item(self, item, spider):

        availability = item['availability']
        if availability == 'Now Available':
            item['availability'] = datetime.date.today()
        else:
            item['availability'] = datetime.datetime.strptime(item['availability'], '%m/%d/%Y')

        bedbath_raw = item['bedbath_raw'].replace('Studio', '0 bed').replace(' / ',' ').split(' ')
        item['beds'] = bedbath_raw[0]
        item['baths'] = bedbath_raw[2]
        # unit_id = scrapy.Field()  
        # datecrawled = scrapy.Field()  
        # domain = scrapy.Field()  
        # url = scrapy.Field()      
        # property = scrapy.Field()  
        # address = scrapy.Field()
        # features_raw = scrapy.Field()  
        # size = scrapy.Field()  
        item['monthly_price'] = item['monthly_price'].strip('$').strip(',')
        item['size'] = item['size'].strip(' sf').strip(',')
        # price_min = scrapy.Field()  
        # price_max = scrapy.Field()           
        # occupancy = scrapy.Field()  
        # pets = scrapy.Field()  
        # terms = scrapy.Field()  
        # units = scrapy.Field()  
        # offer = scrapy.Field()  

        return item
