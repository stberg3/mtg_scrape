# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import hashlib
from mtg.items import MtgImage


class MtgPipeline(object):

    collection_name = "mtg_images"
    image_path = "images/"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        with open("pipeline.log", "a") as f:
            f.write("pipeline initialized...\n")

    @classmethod
    def from_crawler(cls, crawler):
        with open("pipeline.log", "w") as f:
            f.write("from_crawler called...\n")
            f.write("DB Info:\n\tURI:\t{0}\n\tDB:\t{1}\n".format(
                crawler.settings.get('MONGO_URI'),
                crawler.settings.get('MONGO_DATABASE', 'items')
            ))

        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        with open("pipeline.log", "a") as f:
            f.write("spider opened...\n")

        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]


    def close_spider(self, spider):
        with open("pipeline.log", "a") as f:
            f.write("spider closed...\n")

        self.client.close()

    def process_item(self, item, spider):
        with open("pipeline.log", "a") as f:
            f.write("pipeline processing...\n")

        url = item["image_url"]
        url_hash =  hashlib.md5(url.encode("utf8")).hexdigest()
        file_name = "{}.jpg".format(url_hash)

        with open((self.image_path+file_name), "wb") as file:
            file.write(response.body)

        item.image_path = file_name

        self.client[db_name][collection_name].update_one(
            {"image_url" : item.image_url},
            {"image_path": item.image_path}
        )

        return item
