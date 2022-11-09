# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import dataclasses
from typing import Optional
import scrapy
import datetime


class ApicollectorItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def init_time():
    return  datetime.datetime.now()+datetime.timedelta(days=7)


@dataclasses.dataclass
class ApiInfoItem():
    
    platform:Optional[str] = dataclasses.field(default="undefined")
    is_free :Optional[bool] = dataclasses.field(default=False)
    api_type:Optional[str] = dataclasses.field(default="undefined")
    api_name:Optional[str] = dataclasses.field(default="undefined")
    api_icon:Optional[str] = dataclasses.field(default="undefined")
    api_url:Optional[str] = dataclasses.field(default="undefined")
    clicked:Optional[int] = dataclasses.field(default=0)
    expire_time:Optional[str] = dataclasses.field(default_factory=init_time)
    api_price:Optional[float] = dataclasses.field(default_factory=0.0)
    api_price_unit:Optional[str] = dataclasses.field(default="元/次")