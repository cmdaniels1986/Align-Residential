# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from greystar.items import GreystarItem
import datetime


class GreystarPipeline:
    def process_item(self, item, spider):

        availability = item['availability']
        if availability == 'Today':
            item['availability'] = datetime.date.today()
        else:
            item['availability'] = datetime.datetime.strptime(item['availability'], '%m/%d/%y')

        # unit_id = scrapy.Field()  
        # datecrawled = scrapy.Field()  
        # domain = scrapy.Field()  
        # url = scrapy.Field()      
        # property = scrapy.Field()  
        # address = scrapy.Field()
        # availability = scrapy.Field()  
        bedbath_raw = item['bedbath_raw'].replace(' | ',' ').split(' ')
        item['beds'] = bedbath_raw[0]
        item['baths'] = bedbath_raw[2]
        # beds = scrapy.Field()  
        # baths = scrapy.Field()  
        # features_raw = scrapy.Field()  
        # size = scrapy.Field()  
        # monthly_price = scrapy.Field()  
        monthly_price = item['monthly_price']
        monthly_price = monthly_price.replace('$','').replace(',','').replace('.00','')
        monthly_price = monthly_price.split(' - ')
        item['monthly_price'] = monthly_price[0]
        item['price_min'] = monthly_price[0]
        try:
            item['price_max'] = monthly_price[1] 
        except:
            item['price_max'] = monthly_price[0]        
        # occupancy = scrapy.Field()  
        # pets = scrapy.Field()  
        # terms = scrapy.Field()  
        # units = scrapy.Field()  
        # offer = scrapy.Field()  
        item['bedsxbaths'] = item['beds'] + 'x' + item['baths']
        return item
