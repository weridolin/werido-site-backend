# -*- encoding: utf-8 -*-
import pytz,datetime
from typing import Iterable


def queryset2list(queryset):
    assert isinstance(queryset,Iterable),f"queryset:{queryset} is not iterable"
    res = [item for item in queryset]
    return res


import json
def parse_ip(ip=None):
    if ip:
        # Create your tests here.
        import requests
        print(">>>","get location by ip ,url:",f"http://ip-api.com/json/{ip}")
        res = requests.get(url=f"http://ip-api.com/json/{ip}")
        ## {'status': 'success', 'country': 'China', 'countryCode': 'CN', 'region': 'FJ', 
        # 'regionName': 'Fujian', 'city': 'Quanzhou', 'zip': '', 
        # '         lat': 24.9139, 'lon': 118.5858, 'timezone': 'Asia/Shanghai', 
        # 'isp': 'Chinanet', 'org': 'Chinanet FJ', 'as': 'AS4134 CHINANET-BACKBONE', 'query': '110.84.0.129'}
        return res.json()
    

def parse_user_agent(ua):
    ## 判断是移动端还是PC端
    return ua,"mobile"


def nativeTime2utcTime(nativeTime:str):
    dt_naive = datetime.datetime.strptime(nativeTime, "%Y-%m-%d %H:%M:%S")
    # 将 naive datetime 转换为 aware datetime，指定时区为中国标准时间（东八区）
    china_tz = pytz.timezone('Asia/Shanghai')
    dt_aware = china_tz.localize(dt_naive)
    # 将 aware datetime 转换为 ISO 8601 格式字符串
    iso_format_with_timezone = dt_aware.isoformat()
    return iso_format_with_timezone

