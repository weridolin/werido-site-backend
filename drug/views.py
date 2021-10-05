'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-10-04 01:55:10
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-10-04 23:09:43
'''
from inspect import FrameInfo, indentsize
from django.db import models
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from drug.serializers import DrugWordsSerializer
from drug.models import DrugWords
from django_redis import get_redis_connection
from redis.client import Redis
from utils.models import DrugBrief
from utils.helper import queryset2list
import json
from rest_framework.decorators import action
from rest_framework import status

class DrugWordsViewSet(viewsets.ModelViewSet):
    serializer_class = DrugWordsSerializer
    # queryset = DrugWords.objects.all() # 这里是针对所有的请求都会以这个为标准

    def get_queryset(self):
        conn:Redis = get_redis_connection("default")
        key = DrugBrief.from_model("words").cache_key
        res = conn.get(key)
        if res:
            # print(json.loads(res))
            return json.loads(res)
        else:
            words_list = DrugWords.objects.all()
            conn.set(key,json.dumps(DrugWordsSerializer(words_list,many=True).data,ensure_ascii=False))        
            conn.expire(key,12*60*60)# 过期时间设置为半天，到期自动清除
            return words_list
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


    @action(methods=["get"],detail=False,url_name="random word")
    def random(self,request):
        # 随机返回一条
        import random
        last_id = request.query_params.get("last_id",-1)
        queryset = self.get_queryset()
        while True:
            index = random.randint(0,len(queryset)-1)
            if index!=last_id:
                break
            else:
                print("last id== index",index)
        item  = queryset[index]
        serializer = DrugWordsSerializer(instance=item)
        return Response(serializer.data,status=status.HTTP_200_OK)