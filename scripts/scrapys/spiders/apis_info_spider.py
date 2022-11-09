import scrapy
# from scr.items import ApiInfoItem
from scrapys.items.api_collector_items import ApiInfoItem
# from tutorial.database.models import ApiInfosModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import CloseSpider
from scrapy import signals
import datetime

class TianYanApisSpider(scrapy.Spider):
    name = "ac-spider-天眼数据"
    platform = "天眼数据"

    urls = [
        "https://www.tianyandata.cn/product"
    ]
    domain = "https://www.tianyandata.cn"
    all_domains=["https://www.tianyandata.cn"]
    custom_settings = {
        'ITEM_PIPELINES': {
            'scrapys.pipelines.api_collector_pl.ApiInfoBasePipeline': 300
        },
        'MEDIA_ALLOW_REDIRECTS' : True,
        'LOG_LEVEL':"INFO",
        'HTTPERROR_ALLOWED_CODES' :[301,302],
    }
    item = ApiInfoItem

    header = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Host": "www.tianyandata.cn",
        "If-None-Match": "4b49-VhWi6bPOfJ9/omFgkwFSqWB7q+U",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": 1,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52",
        "sec-ch-ua": '"Chromium";v="106", "Microsoft Edge";v="106", "Not;A=Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",

    }

    # db_model = ApiInfosModel
    # db_unique_field = "api_url"
    # db_unique_field = ("api_name","platform")

    series_map = {
        "身份核实":"生活相关",
        "运营商":"运行商相关",
        "银行卡":"生活相关", 
        "车辆":"车辆相关",
        "智能识别":"生活相关",
        "IP系列":"生活相关",
        "物流快递":"生活相关"
    }


    def __init__(self, name=None,db_uri=None, unique_flag=None,**kwargs):
        self.unique_flag = unique_flag
        self.db_uri = db_uri
        self.engine = create_engine(db_uri)
        self.session_factory = sessionmaker(bind=self.engine)
        self.session = self.session_factory()
        self.exception = None
        super().__init__(name, **kwargs)

    
    @classmethod    
    def from_crawler(cls,crawler, *args, **kwargs):
        db_uri = crawler.settings.get("API_INFO_DB_URI")
        spider = cls(*args,db_uri=db_uri,**kwargs)
        crawler.signals.connect(spider.on_closed,signals.spider_closed)
        crawler.signals.connect(spider.on_error,signals.spider_error)
        return spider


    def start_requests(self):
        if not self.unique_flag:
                self.exception = "缺少UNIQUE FLAG,禁止运行."
                raise CloseSpider(reason=self.exception) # closeSpider只能在callback时
        for url in self.urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse_series,
                # headers=self.headers
            )  


    def parse_series(self, response, **kwargs):
        self.logger.info(f'api info spider:{self.platform} start...')
        series_types_xpath = r'//*[@id="__layout"]/div/div[2]/div/div[2]/a/text()'
        series_href_xpath = r'//*[@id="__layout"]/div/div[2]/div/div[2]/a/@href'
        series_name_list = response.xpath(series_types_xpath).getall()
        series_href_list = response.xpath(series_href_xpath).getall()
        for series_name,series_href in zip(series_name_list,series_href_list):
            if series_name in self.series_map:
                product_page_url = f"{self.domain}{series_href}"
                self.logger.info(f"({self.platform})解析类别{series_name}对应的详情页:{product_page_url}")
                yield scrapy.Request(
                    url=product_page_url,
                    callback=self.parse_product_page,
                    cb_kwargs={
                        "series_name":series_name
                    }
                )


    def parse_product_page(self,response,series_name,**kwargs):
        product_detail_href_xpath = f'//div[@class="main-content-box"]/a/@href'
        product_name_xpath = f'//div[@class="main-content-box"]/a/p[1]/text()'
        product_price_xpath = f'//div[@class="main-content-box"]/a/p[2]/text()'

        product_detail_path_list,product_name_list,product_price_list = \
            response.xpath(product_detail_href_xpath).getall(),\
            response.xpath(product_name_xpath).getall(),\
            response.xpath(product_price_xpath).getall(),

        for path,name,price in zip(product_detail_path_list,product_name_list,product_price_list):
            absolute_url = f"{self.domain}{path}"
            item = self._create_item(
                url=absolute_url,
                series_name=series_name,
                name=name,
                price=price
            )
            yield item
    

    def _create_item(self,url,series_name,name,price):
        new_item = ApiInfoItem(
            platform=self.platform,
            is_free= True if float(price) <= 0 else False,
            api_type=self.series_map.get(series_name),
            api_name=name,
            api_url=url,
            api_price=price
        )
        return new_item 

    def on_closed(self,spider,reason):
        finish_time=datetime.datetime.strftime(datetime.datetime.utcnow(), "%Y-%m-%d %H:%M:%S")
        if spider.exception or reason !="finished":
            sql = f"update ac_spider_run_record set result=1,err_reason='{str(spider.exception)}',finish_time='{finish_time}'  WHERE unique_flag='{spider.unique_flag}'"
        else:
            sql = f"update ac_spider_run_record set result=0,finish_time='{finish_time}'  WHERE unique_flag='{spider.unique_flag}'"
        spider.logger.info(sql)
        spider.session.execute(sql)
        spider.session.commit()
        spider.session.close()
        spider.logger.info(f">>> spider close {reason}{type(reason)}")

    
    def on_error(self,failure, response, spider):
        spider.logger.info(f"error happen in callback func")
        spider.exception=str(failure).replace("'","\"")