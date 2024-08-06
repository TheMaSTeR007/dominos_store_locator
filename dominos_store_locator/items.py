# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DominosStoreLocatorItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    area = scrapy.Field()
    address = scrapy.Field()
    landmark = scrapy.Field()
    phone = scrapy.Field()
    open_until = scrapy.Field()
    map_url = scrapy.Field()
    site_url = scrapy.Field()
