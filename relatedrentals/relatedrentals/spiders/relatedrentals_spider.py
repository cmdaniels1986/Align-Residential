import scrapy
from datetime import datetime
from relatedrentals.items import RelatedrentalsItem

class RelatedrentalsSpiderSpider(scrapy.Spider):
    name = 'relatedrentals_spider'
    allowed_domains = ['www.relatedrentals.com']
    start_urls = ['https://www.relatedrentals.com/search?city=51&property=47200726', 
    'https://www.relatedrentals.com/search?city=51&property=25015386',
    'https://www.relatedrentals.com/search?city=51&property=10057386']

    #start_urls = ['https://www.relatedrentals.com/search?city=51&property=47200726']

    def parse(self, response):
        units = response.xpath("//div[@class='views-row']")

        for unit in units:
            unit_id = unit.xpath('.//article/@data-api-id').extract_first()
            datecrawled = datetime.now()
            domain = RelatedrentalsSpiderSpider.allowed_domains
            url = response.urljoin(unit.xpath('.//article/@about').extract_first())
            try:
                property = unit.xpath('.//article/@data-category').extract_first()     
                property = property + ' ' + unit.xpath('.//article/@data-gtm-name').extract_first() 
            except: property = ''
            # property = unit.xpath('.//article/div/a/div[@class="fg-unit-related__content"]/div/div/span[@class="property-neighborhood"]/text()').extract_first()    
            # property = property.strip()
            # property = property + ' ' + unit.xpath('.//article/div/a/div[@class="fg-unit-related__content"]/div/div[@class="fg-unit-related__content-header"]/text()').extract()[1]
            availability = unit.xpath('.//article/@data-dimension9').extract_first()
            bedbath_raw = unit.xpath('.//article/@data-gtm-name').extract_first()

            # size = unit.xpath('.//article/@data-nid').extract_first()   
            monthly_price = unit.xpath('.//article/@data-price').extract_first() 

            if unit_id is not None:
                 yield scrapy.Request(url,
                                      callback=self.parse_unit,
                                      meta={'unit_id': unit_id,
                                             'datecrawled': datecrawled,
                                             'domain': domain,
                                             'url': url,
                                             'property': property,
                                             'availability': availability,
                                             'bedbath_raw': bedbath_raw,
                                             #'size': size,
                                             'monthly_price': monthly_price})
        next_page_url = response.xpath('//a[@title="Go to next page"]/@href').extract_first()
        if next_page_url is not None:
            absolute_next_page_url = 'https://www.relatedrentals.com/search?' + next_page_url
            yield scrapy.Request(absolute_next_page_url)

    def parse_unit(self, response):
        unit_id = response.xpath('//meta[@name="title"]/@content').extract_first() 
        datecrawled = response.meta['datecrawled']
        domain = response.meta['domain']
        url = response.meta['url']
        property = response.meta['property']
        address = response.xpath('//div[@class="fg-unit-header__content-address"]/text()').extract_first().strip()
        availability = response.meta['availability']
        #bedbath_raw = response.meta['bedbath_raw']
        bedbath_raw = response.xpath('//div[@class="fg-unit-header__content-text"]/p/text()').extract_first()
        # features_raw = ''
        # size = response.meta['size']
        monthly_price = response.meta['monthly_price']
        # price_min = ''
        # price_max = ''
        # occupancy = ''
        # pets = ''
        # terms = ''
        # units = ''
        offer = response.xpath('//h6[@class="special-offer__title arrow-right"]/text()').extract_first().strip().replace('Special Offer: ','')

        item = RelatedrentalsItem()

        item['unit_id'] = unit_id
        item['datecrawled'] = datecrawled
        item['domain'] = domain
        item['url'] = url
        item['property'] = property
        item['address'] = address
        item['availability'] = availability
        item['bedbath_raw'] = bedbath_raw
        #item['size'] = size
        item['monthly_price'] = monthly_price
        item['offer'] = offer

        yield item
