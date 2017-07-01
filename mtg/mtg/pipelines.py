# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import hashlib
# from settings import MONGO_URI, MONGO_DB
from mtg.items import MtgImage
from time import asctime, localtime

class MetadataPipeline(object):
    collection_name = "mtg_cards"

    # self.mongo_uri = MONGO_URI
    # self.mongo_db = MONGO_DB

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        with open("pipeline.log", "a") as f:
            f.write("MetadataPipeline initialized...\n")

    @classmethod
    def from_crawler(cls, crawler):
        with open("pipeline.log", "a") as f:
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
            f.write("spider opened...:\n\t{0}\n\t{1}\n".format(
            self.mongo_uri, self.mongo_db))

        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]


    def close_spider(self, spider):
        # with open("pipeline.log", "a") as f:
        #     f.write("spider closed...\n")

        self.client.close()

    def process_item(self, item, spider):
        # with open("pipeline.log", "a") as f:
        #     f.write("pipeline processing...\n")

        url = item["image_url"]
        url_hash =  hashlib.md5(url.encode("utf8")).hexdigest()
        file_name = "{}.jpg".format(url_hash)

        with open((self.image_path+file_name), "wb") as file:
            file.write(item["image_data"])

        item["image_path"] = file_name

        with open("pipeline.log", "a") as f:
            f.write("DB access:\n"+item["image_url"]+"\n")

            f.write("access?:\n\t{}\n".format(
                str(self.db[self.collection_name].find_one({"name":"Mountain"}))))

            f.write("modifying:\n\t{}\n".format(
                self.db[self.collection_name].find_one(
                    {"image_url":item["image_url"]})))

        self.db[self.collection_name].find_and_modify(
            query={"image_url" : item["image_url"]},
            update={"$set":{"image_path": item["image_path"]}}
        )

        return item


class MtgPipeline(object):

    collection_name = "mtg_cards"
    image_path = "images/"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        with open("pipeline.log", "a") as f:
            f.write("MtgPipeline initialized...\n")

    @classmethod
    def from_crawler(cls, crawler):
        with open("pipeline.log", "a") as f:
            f.write("\nPIPELINE STARTED: {}\n".format(asctime(localtime())))
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
            f.write("spider opened...:\n\t{0}\n\t{1}\n".format(
            self.mongo_uri, self.mongo_db
            ))

        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]


    def close_spider(self, spider):
        # with open("pipeline.log", "a") as f:
        #     f.write("spider closed...\n")

        self.client.close()

    def process_item(self, item, spider):
        # with open("pipeline.log", "a") as f:
        #     f.write("pipeline processing...\n")

        url = item["image_urls"][0]
        url_hash =  hashlib.sha1(url.encode("utf8")).hexdigest()
        file_name = "{}.jpg".format(url_hash)

        # with open((self.image_path+file_name), "wb") as file:
        #     file.write(item["image_data"])

        item["image_path"] = file_name

        self.db[self.collection_name].insert_one(dict(item))

        self.db[self.collection_name].find_and_modify(
            query={"image_url" : item["image_urls"][0]},
            update={"$set":{"image_path": item["image_path"]}}
        )

        return item
