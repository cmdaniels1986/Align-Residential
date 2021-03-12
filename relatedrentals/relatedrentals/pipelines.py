# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from relatedrentals.items import RelatedrentalsItem
import datetime

class RelatedrentalsPipeline:
    def process_item(self, item, spider):

        availability = item['availability']
        if availability == 'Now':
            item['availability'] = datetime.date.today()
        else:
            item['availability'] = datetime.datetime.strptime(item['availability'] + '/' + str(datetime.date.today().year), '%m/%d/%Y')

        unit_id = item['unit_id']
        start =unit_id.find('#')
        finish = unit_id.find(' at ')
        
        item['unit_id'] = unit_id[start:finish].replace('#','').strip() 
        # datecrawled = scrapy.Field()  
        # domain = scrapy.Field()  
        # url = scrapy.Field()      
        # property = scrapy.Field()  
        # address = scrapy.Field()
        # availability = scrapy.Field()  
        bedbath_raw1 = item['bedbath_raw'].replace('Alcove Studio', '0 bed').replace('Studio', '0 bed').replace('Jr. ', '').replace('Corner ', '').replace(',','')
        bedbath_raw2 = bedbath_raw1.split(' ')
        item['beds'] = bedbath_raw2[0]
        item['baths'] = bedbath_raw2[2]
        # beds = scrapy.Field() 
        # baths = scrapy.Field() 
        # features_raw = scrapy.Field()  
        
        # size = scrapy.Field()  
        # monthly_price = scrapy.Field()  
        # price_min = scrapy.Field()  
        # price_max = scrapy.Field()           
        # occupancy = scrapy.Field()  
        # pets = scrapy.Field()  
        # terms = scrapy.Field()  
        # units = scrapy.Field()  
        # offer = scrapy.Field() 
        item['bedsxbaths'] = item['beds'] + 'x' + item['baths'] 
        address = item['address']
        item['address'] = address[0:address.find('  ')].strip()
        city = address.replace(item['address'],'').strip()
        item['city'] = city[0:city.find(',')].strip()
        item['state'] = address[address.find(',')+1:address.rfind(' ')].strip()
        property = item['property'].split(':')
        item['property'] = property[0].strip()

        return item
