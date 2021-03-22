# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from equityapartments.items import EquityapartmentsItem

class EquityapartmentsPipeline:

    def process_item(self, item, spider):        
        # unit_id = scrapy.Field()  
        # datecrawled = scrapy.Field()  
        # domain = scrapy.Field()  
        # url = scrapy.Field()      
        # property = scrapy.Field()  
        # address = scrapy.Field()
        item['availability'] = item['availability'].replace('Available ','')
        bedbath_raw = item['bedbath_raw'].split(' ')
        item['beds'] = bedbath_raw[0]
        item['baths'] = bedbath_raw[2]
        # bedbath_raw = scrapy.Field()  
        # features_raw = scrapy.Field()  
        item['size'] = item['size'].replace(' sq. ft.','') 
        item['monthly_price'] = item['monthly_price'].replace('$','').replace(',','')  
        # price_min = scrapy.Field()  
        # price_max = scrapy.Field()           
        # occupancy = scrapy.Field()  
        # pets = scrapy.Field()  
        # terms = scrapy.Field()  
        # units = scrapy.Field()  
        # offer = scrapy.Field()  
        item['bedsxbaths'] = item['beds'] + 'x' + item['baths']

        return item
