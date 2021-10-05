'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-05-16 12:32:46
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-10-05 12:57:16
'''
from json.decoder import JSONDecodeError
import re,json
from articles.v1.serializers import *
from articles.models import *
# Create your views here.
from rest_framework.exceptions import UnsupportedMediaType
from django.http import Http404,HttpResponseBadRequest,HttpResponseNotFound,HttpResponseNotAllowed
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from articles.utils import model2json
from rest_framework.parsers import JSONParser,FormParser
from rest_framework.decorators import parser_classes
from articles.v1.signals import update_pre_and_next,update_pre_and_next_signal
## APIVIEWS:
# The following methods are called directly by the view's .dispatch() method.
#  These perform any actions that need to occur before or 
# after calling the handler methods such as .get(), .post(), put(), patch() and .delete().

class ArticleViews(APIView):
    """文章接口"""

    parser_classes=[JSONParser]
    page = 1
    default_page_num = 6

            
    def get(self, request, pk=None, format=None):
        if pk:
            try:
                article = Article.objects.get(pk=pk)
                serializer = ArticleSerializer(instance =article)
                # 取出文章评论
                # comments = Comments.objects.filter(article=id)
                # res = {"article":serializer_article.data,"comments":"todo"}
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Article.DoesNotExist:
                return HttpResponseNotFound("can not find article!")    
        else:
            page = request.query_params.get("page",None) 
            page_num = request.query_params.get("page_num",self.default_page_num)
            if page and page_num:
                print(f"page:{page},page_num:{page_num}")
                _from = int((int(page) - 1) * int(page_num))
                _to = int((int(page)) * int(page_num))
                articles = Article.objects.all().order_by(
                    "-created")[_from:_to]
            else:
                articles = Article.objects.all().order_by("-created")
            last_page = articles.count()/page_num if articles.count()%page_num==0 else (articles.count()/page_num +1)
            serializer = ArticleSerializer(articles,many =True)
            payload = {"data":serializer.data,"last_page":int(last_page),"count":articles.count()}
            
            return Response(payload,status=status.HTTP_200_OK)

    def post(self,request,*args,**kwargs):
        if request.data:  
            type = Types.objects.get(name = request.data.get("type")) or None
            user = User.objects.get(id=1)
            tags = []
            for name in request.data.get("tags"):
                tags.append(Tags.objects.get(name = name))
            request.data.pop("type")
            request.data.pop("tags")
            try:
                pre = Article.objects.filter(author = user).latest("id")
            except Article.DoesNotExist:
                pre = None 
            article = Article.objects.create(type= type,author=user,pre=pre,**request.data) 
            article.tags.set(tags)
            article.save()
            update_pre_and_next_signal.send(sender=article.__class__, created=True,instance=article)
            return Response(
                {"msg":f"create article success! {model2json(article)}"},
                status=status.HTTP_200_OK)
        else:
            return HttpResponseBadRequest(                
                json.dumps({"msg":F"request data can not be None"},
                ensure_ascii=False)
            )               

    def put(self,request,pk=None,*args,**kwargs):
        if pk:
            try:
                article = Article.objects.get(pk=pk)
                data_ = request.data
                for key,value in data_.items():
                    if  hasattr(article,key):
                        setattr(article,key,value)
                article.save()
                return Response(
                    {"msg":f"update article success,article:{model2json(article)}"},
                    status=status.HTTP_200_OK) 
            except JSONDecodeError:
                return HttpResponseBadRequest(                
                    json.dumps({"msg":F"invalid request data:{request.data}"},
                    ensure_ascii=False)
                )   
            except Article.DoesNotExist:
                print(">>>not exist!")
                return HttpResponseNotFound(                
                    json.dumps({"msg":F"delete article fail! id :{pk}"},
                    ensure_ascii=False)
                )   
        else:
            return HttpResponseBadRequest(
            json.dumps({"msg":"please choose an article first!"},ensure_ascii=False)
            )

    def delete(self,request,pk=None,*args,**kwargs):
        if pk:
            try:
                article = Article.objects.get(pk=pk)
                article.delete()
                return Response(
                    {"msg":F"delete article success! id :{pk}"},
                    status=status.HTTP_200_OK)
            except Article.DoesNotExist:
                print(">>>not exist!")
                return HttpResponseNotFound(                
                    json.dumps({"msg":F"delete article fail! id :{pk}"},
                    ensure_ascii=False)
                )     
        else:
            return HttpResponseBadRequest(
            json.dumps({"msg":"article ID cannot be None!" },ensure_ascii=False)
            )

    def patch(self,request,*args,**kwargs):
        return HttpResponseNotAllowed(permitted_methods=["get","post","put","delete"])
    
    def handle_exception(self, exc):
        if isinstance(exc,UnsupportedMediaType):
            exc.detail = f"不支持的content-type: {self.request.content_type},只支持 application/json"       
        return super().handle_exception(exc)



class SearchViews(APIView):
    # search API return ARTICLE Brief info
    # authentication_classes=[]
    def get(self, request):
        title = request.GET.get("title", None)
        if title:
            article_list = Article.objects.filter(title__icontains=title).order_by("-created")
            serializer = ArticleBriefSerializer(article_list, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(None,status=status.HTTP_404_NOT_FOUND)

class TagsViews(APIView):

    def get(self, request):
        tags = Tags.objects.all()
        tags_serializer = TagsSerializer(tags, many=True)
        return Response(tags_serializer.data, status=status.HTTP_200_OK)


class TypesViews(APIView):

    def get(self, request):
        types = Types.objects.all()
        types_serializer = TypesSerializer(types, many=True)
        return Response(types_serializer.data, status=status.HTTP_200_OK)


class GetArticleCountViews(APIView):

    def get(self, request):
        import json
        obs = Article.objects.all()
        return Response({"count": len(obs)}, status=status.HTTP_200_OK)

