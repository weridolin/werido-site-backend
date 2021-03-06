'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-10-04 02:01:01
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-10-05 18:48:23
'''

from rest_framework import serializers
from home.models import *

class UpdateLogSerializer(serializers.ModelSerializer):
    finish_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")  # postgres 存的是带时区TZ，这里把它格式化一下
    
    class Meta:
        model = UpdateLog
        fields = "__all__"
        depth = 1

class FriendsLinkSerializer(serializers.ModelSerializer):
    updated = serializers.DateTimeField(format="%Y-%m-%d") 

    class Meta:
        model = FriendsLink
        fields = "__all__"


class BackGroundMusicSerializer(serializers.ModelSerializer):
        class Meta:
            model = BackGroundMusic
            fields = "__all__"


class SiteCommentsSerializer(serializers.ModelSerializer):

    created  = serializers.SerializerMethodField()

    class Meta:
        model = SiteComments
        fields = '__all__'

    def get_created(self,obj):
        date_str = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S").to_internal_value(value=obj.created)
        return int(date_str.timestamp())