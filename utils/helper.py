# -*- encoding: utf-8 -*-
'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-10-04 10:01:15
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-10-05 11:23:06
'''

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