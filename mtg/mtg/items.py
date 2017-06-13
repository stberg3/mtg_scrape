# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class MtgImage(scrapy.Item):
    image_data = scrapy.Field()
    image_url = scrapy.Field()
    image_path = scrapy.Field()
