import requests
import os
import sys
import re
import json
from bs4 import BeautifulSoup
# from covid19._dict import city_adcode_ref,province_adcode_ref

DataSrc = {
    "url": r"https://ncov.dxy.cn/ncovh5/view/pneumonia",
    "name":"丁香园"
}


class CovidSpider:

    name = "covid-spider"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9;charset=utf-8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.52",


    }

    def parse_page(self, url=DataSrc["url"]):
        res = requests.get(url=url, headers=self.headers)
        print(res.content)
        if 200 <= res.status_code <= 300:
            # res.encoding = res.apparent_encoding
            res = res.content.decode("utf-8")
            soup = BeautifulSoup(res, 'html.parser')
            cities_info = soup.find_all(
                "script", attrs={"id": "fetchRecentStatV2"})
            if cities_info:
                self.parse_city(cities_info[0].get_text())
            countries_info = soup.find_all(
                "script", attrs={"id": "getListByCountryTypeService2true"})
            if countries_info:
                self.parse_country(res=countries_info[0].get_text())
    

            # print(cities_info)

    def parse_city(self, res):
        """
            城市信息:
                "provinceName": "广东省",
                "provinceShortName": "广东",
                "yesterdayLocalConfirmedCount": 1686,//本土新增
                "yesterdayAsymptomaticCount": 4816, //本土无症状
                "currentConfirmedCount": 13254, //现存确诊
                "confirmedCount": 44315, //累计确诊
                "dangerCountIncr": 1,
                "currentDangerCount": 5177, //风险地区
                "locationId": 440000,
                "statisticsData": "https://file1.dxycdn.com/2020/0223/281/3398299758115524068-135.json",

        """
        filter_info = re.search(r'\[(.*)\]', res)
        if filter_info:
            # print(filter_info.groups())
            filter_info = json.loads(filter_info.group(0))
            cities_item_list = list()
            province_item_list = list()
            for province_info in filter_info:
                cities_info = province_info.get("cities")
                for city_info in cities_info:
                    ## 生成城市信息
                    city_item = {
                        "city_name":city_info["cityName"],
                        "current_confirmed_count":city_info["currentConfirmedCount"],
                        "current_confirmed_count_no_symptom":city_info["yesterdayAsymptomaticCount"],
                        "confirmed_count":city_info["confirmedCount"],
                        # "city_code":self._get_city_adcode(
                        #     province=city_info["provinceName"],
                        #     city=city_info["cityName"]
                        # )
                    }
                    cities_item_list.append(city_item)
                # 生成省份信息
                province_item = {
                    "province_name":province_info["provinceName"],
                    "current_confirmed_count":province_info["currentConfirmedCount"],
                    "current_confirmed_count_no_symptom":province_info["yesterdayAsymptomaticCount"],
                    "confirmed_count":province_info["confirmedCount"],
                    # "province_code":province_adcode_ref.get(province_info["provinceName"])
                }
                province_item_list.append(province_item)
                
        print(province_item_list)
        print(cities_item_list)


    def _get_city_adcode(self, province, city):
        return
        for province_info in city_adcode_ref:
            if province_info["provice"]==province:
                for city_info in province_info["city"]:
                    if city_info["name"]==city:
                        return city_info["adcode"]

    def parse_country(self, res):
        filter_info = re.search(r'\[(.*)\]', res)
        if filter_info:
            print(">>>get country info",filter_info.group(0))
            filter_info = json.loads(filter_info.group(0))
            country_item_list = list()
            for country_info in filter_info:
                country_item = {
                    # "country_code":country_info[""],
                    "country_name_cn":country_info["provinceName"],
                    "country_name_en":country_info["countryFullName"],
                    "confirmed_count":country_info["confirmedCount"],
                    "cured_count":country_info["curedCount"],
                    "dead_count":country_info["deadCount"]
                }
                country_item_list.append(country_item)





if __name__ == "__main__":
    # res = "[]222[]"
    # filter_info = re.search(r'\[\]',res)
    # print(filter_info,filter_info.groups(),filter_info.group(0))
    CovidSpider().parse_page()
