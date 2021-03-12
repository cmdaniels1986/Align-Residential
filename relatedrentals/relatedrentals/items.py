# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RelatedrentalsItem(scrapy.Item):
    unit_id = scrapy.Field()  
    datecrawled = scrapy.Field()  
    domain = scrapy.Field()  
    url = scrapy.Field()      
    property = scrapy.Field()  
    address = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    availability = scrapy.Field()  
    bedbath_raw = scrapy.Field()  
    beds = scrapy.Field() 
    baths = scrapy.Field() 
    features_raw = scrapy.Field()  
    size = scrapy.Field()  
    monthly_price = scrapy.Field()  
    price_min = scrapy.Field()  
    price_max = scrapy.Field()           
    occupancy = scrapy.Field()  
    pets = scrapy.Field()  
    terms = scrapy.Field()  
    units = scrapy.Field()  
    offer = scrapy.Field()  
    bedsxbaths = scrapy.Field()
