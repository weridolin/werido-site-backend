from email import header
from rest_framework.generics import CreateAPIView,RetrieveAPIView
from thirdApis.shortUrls.serializers import ShortUrlSerializer
from thirdApis.models import ShortUrlRecords
from rest_framework.permissions import AllowAny
from utils.http_ import HTTPResponse
import datetime
from django_redis import get_redis_connection
from redis.client import Redis
from utils.models import ShortUrlKey
from rest_framework import status

class ShortUrlRecordApis(CreateAPIView):
    queryset = ShortUrlRecords.objects.all()
    serializer_class = ShortUrlSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        timedelta = request.data.pop("expire_time",24*3600)
        expire_time = datetime.datetime.now()+datetime.timedelta(seconds=timedelta)
        long_url = request.data.pop("url")
        count = self.queryset.count()
        record:ShortUrlRecords = ShortUrlRecords.objects.filter(type=request.data.get("type","self"),url=long_url).first()
        if record:
            conn:Redis = get_redis_connection("default") # return redis client:<redis.client.Redis>
            conn.set(ShortUrlKey.create(record.short_flag),record.url,ex=timedelta)
            return HTTPResponse(data=ShortUrlSerializer(record).data,message="create short url success" ,app_code="thirdApis")

        short_flag = longUrl2Short(count=count)
        print(f">>> change {long_url} to short url {short_flag}")
        serializer = self.get_serializer(data={
            "url":long_url,
            "expire_time":expire_time,
            "short_flag":short_flag,
            **request.data
        })
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        conn:Redis = get_redis_connection("default") # return redis client:<redis.client.Redis>
        conn.set(ShortUrlKey.create(short_flag),long_url,ex=timedelta)
        return HTTPResponse(data=serializer.data,message="create short url success" ,app_code="thirdApis")


def longUrl2Short(count):
    _62_count = To62(count)
    # return f"{request.scheme}://{request.META['SERVER_NAME']}:{request.META['SERVER_PORT']}/api/v1/third/shortUrl/{To62(count)}"
    return _62_count

import itertools,string
NUM = list(itertools.chain(string.digits, string.ascii_uppercase, string.ascii_lowercase))

def To62(number):
    number+=123456
    len_count = len(NUM)
    result_value = []
    while number >= len_count:
        number, remain = divmod(number, len_count)
        result_value.append(NUM[remain])
    result_value.append(NUM[number])
    result_value.reverse()

    result = "".join(result_value)
    return result



class RedirectToRealUrl(RetrieveAPIView):
    
    def get(self,request,short_number,*args, **kwargs):
        conn:Redis = get_redis_connection("default") # return redis client:<redis.client.Redis>
        long_url = conn.get(ShortUrlKey.create(short_number))
        print(f">>> get  long url {long_url} by short number:{short_number}")
        if not long_url:
            return HTTPResponse(
                status=status.HTTP_404_NOT_FOUND,
                message=f"can not find long url by :{short_number}",
                code=-1,
                app_code="thirdApis"
            )       
        else:
            return HTTPResponse(
                status=status.HTTP_302_FOUND,
                app_code="thirdApis",
                headers={"Location":long_url} #浏览器自动跳转
            )