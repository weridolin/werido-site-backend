# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.http import headers
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scrapys.items.api_collector_items import ApiInfoItem
import dataclasses
import os,sys
from scrapys.models.ac_models import ApiInfosModel


class ApiInfoBasePipeline():
    def __init__(self):
        self.unique_flag = None
        self.cache = []

    def open_spider(self, spider):
        self.unique_flag = spider.unique_flag
        self.session = spider.session

    def close_spider(self, spider):
        self.cache.clear()

    def process_item(self,item:ApiInfoItem,spider):
        """
            更新item回数据库
        """
        spider.logger.info(f">>> process item ->{dataclasses.asdict(item)}")
        record = self.session.query(ApiInfosModel).filter(ApiInfosModel.api_url==item.api_url).first()
        if record:
            for k,v in dataclasses.asdict(item).items():
                if hasattr(record,k):
                    setattr(record,k,v)
        else:
            self.session.add(ApiInfosModel(
                **dataclasses.asdict(item)
            ))
        self.session.commit()
        return item

