# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# Card DB entry
# {   "number": "1",
    # "name": "Angel of Sanctions",
    # "card_url": "http://magiccards.info/akh/en/1.html",
    # "image_url": "http://magiccards.info/scans/en/akh/1.jpg",
    # "type": "Creature \u2014 Angel 3/4",
    # "mana": "3WW",
    # "rarity": "Mythic Rare",
    # "artist": "Min Yum",
    # "edition": "Amonkhet" },

class MtgCard(scrapy.Item):
    image_data = scrapy.Field()
    image_url = scrapy.Field()
    image_path = scrapy.Field()
    image_urls = scrapy.Field()

class MtgImage(scrapy.Item):
    image_data = scrapy.Field()
    image_url = scrapy.Field()
    image_path = scrapy.Field()
