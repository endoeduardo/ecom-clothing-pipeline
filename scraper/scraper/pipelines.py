"""SCRAPING PIPELINE TO INSERT INTO MONGO DB"""
# pylint: skip-file: W0201
import re

import pymongo
from itemadapter import ItemAdapter


class MongoPipeline:
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "items"),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.collection_name = spider.collection_name

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        adapter["product_name"] = self.trim_whitespace(adapter["product_name"])
        adapter["internal_id"] = self.trim_whitespace(adapter["internal_id"])
        adapter["price"] = self.transform_price_into_float(adapter["price"])
        adapter["color"] = self.trim_whitespace(adapter["color"])
        adapter["gender"] = self.trim_whitespace(adapter["gender"])

        self.db[self.collection_name].insert_one(adapter.asdict())
        return item

    def trim_whitespace(self, string):
        if isinstance(string, str):
            return string.strip()
        return None
    
    def transform_price_into_float(self, price_string):
        number_str = re.search(r"\d+,\d+", price_string).group()
        cleaned = number_str.replace(".", "")
        cleaned = cleaned.replace(",", ".")

        return float(cleaned)