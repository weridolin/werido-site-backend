# from django.test import TestCase

# Create your tests here.

import numpy
import pandas
import datetime
import _dict


# city data

# insert_sql_template = """
# INSERT INTO covid19_city_data (created,updated,city_code,current_confirmed_count,confirmed_count,cured_count,dead_count, \
# city_name,current_confirmed_count_no_symptom,city_name_en,country_name_cn,country_name_en,province_code,province_name,\
# province_name_en) \
# VALUES ('{created}','{updated}','{city_code}','{current_confirmed_count}','{confirmed_count}','{cured_count}','{dead_count}',\
# '{city_name}','{current_confirmed_count_no_symptom}','{city_name_en}','{country_name_cn}','{country_name_en}','{province_code}','{province_name}','{province_name_en}');"""


# excel_path = f"D:\code\python\site\DXYArea.csv"

# df = pandas.read_csv(excel_path)


# def get_city_adcode(province, name):
#     for province_info in _dict.city_adcode_ref:
#         if province_info["provice"] in province:
#             for city_info in province_info["city"]:
#                 if city_info["name"] in name:
#                     return city_info["adcode"]


# def get_province_code(province):
#     return _dict.province_adcode_ref.get(province)

# import os
# with open(os.path.join(os.path.dirname(__file__),"data.sql"),"a",encoding="utf-8") as f:
#     for index,line in df.iterrows():
#         # print(line,type(line))
#         # break
#         try:
#             insert_sql = insert_sql_template.format(
#                 created=line["updateTime"],
#                 updated=line["updateTime"],
#                 city_code=get_city_adcode(line["provinceName"],line["cityName"]),
#                 city_name=line["cityName"],
#                 city_name_en=line["cityEnglishName"].replace("'","''"),
#                 province_name=line["provinceName"],
#                 province_name_en=line["provinceEnglishName"].replace("'","''"),
#                 country_name_cn=line["countryName"],
#                 country_name_en=_dict.country_name_map.get(line["countryName"]),
#                 confirmed_count=int(line["city_confirmedCount"]),
#                 cured_count=int(line["city_curedCount"]),
#                 dead_count=int(line["city_deadCount"]),
#                 current_confirmed_count=-1,
#                 current_confirmed_count_no_symptom=-1,
#                 province_code=get_province_code(line["provinceName"])
#             )
#             f.write(insert_sql)
#             # break
#         except:
#             continue


# news
import os

insert_sql_template2 = """INSERT INTO covid19_news (created,updated,title,\
loc,src,url,type,summary) \
VALUES ('{created}','{updated}','{title}','{loc}','{src}','{url}','{type}','{summary}');"""

excel_path = f"D:\code\python\site\DXYNews.csv"


df = pandas.read_csv(
    excel_path,

)

with open(os.path.join(os.path.dirname(__file__), "news.sql"), "a", encoding="utf-8") as f:
    for index, line in df.iterrows():
        if line["sourceUrl"] is numpy.nan:
            continue
        else:
            try:
                insert_sql = insert_sql_template2.format(
                    created=line["pubDate"],
                    updated=line["pubDate"],
                    title=line["title"],
                    loc=line["infoSource"],
                    src=line["infoSource"],
                    url=line["sourceUrl"],
                    type=line["category"],
                    summary=line["summary"]
                )
                f.write(insert_sql+'\n')
            except:
                raise
