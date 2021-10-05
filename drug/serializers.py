'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-10-04 02:01:01
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-10-04 02:03:17
'''

from rest_framework import serializers
from drug.models import DrugWords

class DrugWordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DrugWords
        fields = "__all__"