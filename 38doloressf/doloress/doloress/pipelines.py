# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from doloress.items import DoloressItem
from datetime import date

class DoloressPipeline:
    def process_item(self, item, spider):
        item['unit_id'] = item['unit_id'].replace('#','')  
        # datecrawled = scrapy.Field()  
        # domain = scrapy.Field()  
        # url = scrapy.Field()      
        # property = scrapy.Field()  
        # address = scrapy.Field()
        bedbath_raw = item['bedbath_raw'].split(' ')
        item['beds'] = bedbath_raw[0]
        item['baths'] = bedbath_raw[2]
        item['monthly_price'] = item['monthly_price'].replace('Starting at $','').replace(',','')
        # features_raw = scrapy.Field()  
        item['size'] = item['size'].replace(' Sq.Ft.', '').replace(',','') 

        availability = item['availability']
        if availability == 'Available Now':
            item['availability'] = date.today()

        item['bedsxbaths'] = item['beds'] + 'x' + item['baths']

        item['address'] = '38 Dolores St'
        item['city'] = 'San Francisco'
        item['state'] = 'CA'
        
        return item
