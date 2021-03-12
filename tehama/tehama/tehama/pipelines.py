# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from tehama.items import TehamaItem
import datetime

class TehamaPipeline:
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
        item['beds'] = bedbath_raw[0]
        item['baths'] = bedbath_raw[2]
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
        return item