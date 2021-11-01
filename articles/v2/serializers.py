'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-10-02 16:08:58
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-11-01 22:07:30
'''
# -*- encoding: utf-8 -*-
from rest_framework import serializers
from articles.models import *


class CommentsSerializer(serializers.ModelSerializer):
    pass


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = [
            "id",
            "name",
            "description",
        ]   

    def update(self, instance, validated_data):
        print("this is update")
        return super().update(instance, validated_data)


    def create(self, validated_data):
        print("this is create")
        return super().create(validated_data)

class TypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Types
        fields = [
            "id",
            "name",
            "description",
        ]


class ArticleCommentSerializer(serializers.ModelSerializer):
    pass


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
        ]

class ArticleBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model= Article
        fields =["id","title"]

class ArticleSerializer(serializers.ModelSerializer):
    type = TypesSerializer()
    tags = TagsSerializer(many=True)
    author = UserSerializer()
    created = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")  # postgres 存的是带时区TZ，这里把它格式化一下
    updated = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    next = ArticleBriefSerializer()
    pre = ArticleBriefSerializer()

    class Meta:
        model = Article
        fields = '__all__'
    

    def validate(self, attrs):
        print(attrs)
        return super().validate(attrs)

    def create(self, validated_data):
        print(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
        
    
