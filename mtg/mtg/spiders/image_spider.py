import scrapy
import pymongo
from mtg.items import MtgImage

class ImageSpider(scrapy.Spider):
    name = "images"



    def start_requests(self):
        client = pymongo.MongoClient()
        cards_collection = client.mtg_database.mtg_cards
        cursor = cards_collection.find({},{"image_url":1})
        urls = [result['image_url'] for result in cursor][:5]

        for url in urls:
            self.log("URL = {}".format(url))
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        pass
