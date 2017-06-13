import scrapy
import pymongo
from mtg.items import MtgImage
from scrapy.loader import ItemLoader

class ImageSpider(scrapy.Spider):
    name = "images"



    def start_requests(self):
        client = pymongo.MongoClient()
        cards_collection = client.mtg_database.mtg_cards
        cursor = cards_collection.find({},{"image_url":1})
        urls = [result['image_url'] for result in cursor][:2]

        for url in urls:
            self.log("URL = {}".format(url))
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        self.log("Yielding: " + str(response.url))
        item =  MtgImage(image_url=response.url, image_data=response.body)
        # item['image_url'] = response.url
        yield item
