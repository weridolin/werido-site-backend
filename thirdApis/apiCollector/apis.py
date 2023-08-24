from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from utils.http_ import HTTPResponse
from thirdApis.models import ApiCollectorSpiderRunRecord,ApiCollector,ApiCollectorSpiderResourceModel
from thirdApis.apiCollector.serializers import ApiCollectorSpiderRunRecordSerializer,ApiInfoSerializer,ApiCollectorSpiderResourceSerializer
import datetime,os,sys
from django.conf import settings
import subprocess
from rest_framework.permissions import IsAuthenticated,AllowAny
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rbac.permission import RbacModelPermission
from rest_framework.decorators import action
from rest_framework import status
from authenticationV1 import V1Authentication
import uuid
class TaskOperationView(APIView):
    
    # permission默认view,即为get不加权限限制.
    authentication_classes = [V1Authentication]
    # permission_classes = [IsAuthenticated,RbacModelPermission]
    # permission_classes = [IsAuthenticated] # 放在网关做了

    queryset = ApiCollectorSpiderRunRecord.objects.all()

    def get(self, request, format=None):
        """
            Return a list of all users.
        """
        only_running = request.data.get("only_running")
        if only_running:
            records = ApiCollectorSpiderRunRecord.objects.filter(result=2).all()
        else:
            records = ApiCollectorSpiderRunRecord.objects.all()
        return HTTPResponse(
            data=ApiCollectorSpiderRunRecordSerializer(records,many=True).data
        )    


    def post(self, request, format=None):
        spider_name = request.data.get("spider_name")
        if not spider_name:
            return HTTPResponse(
                code=-1,
                status=status.HTTP_400_BAD_REQUEST,
                message="spider name不能为空"
            )
        resource = ApiCollectorSpiderResourceModel.objects.filter(name=spider_name).first()
        if not resource:
            return HTTPResponse(
                code=-1,
                status=status.HTTP_400_BAD_REQUEST,
                message=f"未找到[{spider_name}]的相关资源"
            )
        else:
            resource.run_count+=1
            resource.last_run_time=datetime.datetime.now()
            resource.save()

        unique_flag = str(uuid.uuid4())
        log_path,pid,cmd = self._start_spider(spider_name=spider_name,unique_flag=unique_flag)
        run_record = ApiCollectorSpiderRunRecord(
            pid=pid,
            log_path=log_path,
            name=spider_name,
            invoker=request.user,
            unique_flag=unique_flag,
            run_command=cmd
        )
        run_record.save()
        return HTTPResponse(
            message="spider启动成功!"
        )

    def _start_spider(self,spider_name,unique_flag):
        time =  datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d-%H-%M-%S")
        log_path = os.path.join(settings.LOG_ROOT,f"{time}_spider.log")
        pid_path = os.path.join(settings.LOG_ROOT,f"spider_pid.txt")
        scrapy_cmd = f"scrapy crawl {spider_name} --logfile {log_path} --pidfile {pid_path}"
        python_exc = sys.executable
        if sys.platform.lower()=="linux":
            cmd =["python","-m","scrapy","crawl",spider_name,"--logfile",log_path,"--pidfile",pid_path,"-a",f"unique_flag={unique_flag}"]
            print("exec command",cmd,settings.SPIDER_DIR)
            p = subprocess.Popen(args=cmd,cwd=settings.SPIDER_DIR)
        else:
            cmd = f"{python_exc} -m {scrapy_cmd} -a unique_flag={unique_flag}"
            print("exec command",cmd,settings.SPIDER_DIR)
            p = subprocess.Popen(args=cmd,cwd=settings.SPIDER_DIR)
            
        return log_path,p.pid,cmd




class ApiInfoViews(ModelViewSet):

    queryset = ApiCollector.objects.all()
    authentication_classes = []
    # permission_classes = [AllowAny]
    serializer_class  = ApiInfoSerializer
    


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        api_infos = serializer.data
        types = ApiCollector.objects.distinct("api_type").all()
        platforms = ApiCollector.objects.distinct("platform").all()
        return HTTPResponse(
            data={
                "api_infos":api_infos,
                "api_types":[type.api_type for type in types],
                "apu_types_alias":{
                },
                "platform":[platform.platform for platform in platforms]
                
            }
        )

    @action(methods=["POST","GET"],url_name="api-search",detail=False)
    def search(self,request):
        types = request.data.get("types",[])
        prices = request.data.get("price",[])
        platform = request.data.get("platform",[])
        is_free=list()

        for price in prices:
            if price=="收费":
                is_free.append(False)
            elif price=="免费":
                is_free.append(True)
        query_params = dict()
        if types:
            query_params.update({"api_type__in":types})    
        if prices:
            query_params.update({"is_free__in":is_free})    
        if platform:
            query_params.update({"platform__in":platform})    
        
        print("search api condition:",query_params)
        api_infos = ApiCollector.objects.filter(**query_params).all()
        # print("search api condition:",request.data,api_infos)

        return HTTPResponse(
            data={
                "api_infos":ApiInfoSerializer(api_infos,many=True).data,
                "api_types":[],
                "apu_types_alias":{},
                "platform":[]
                
            }
        )

class ApisSpiderResourceViews(APIView):

    queryset = ApiCollectorSpiderResourceModel.objects.all()
    authentication_classes = [V1Authentication]
    # permission_classes = [IsAuthenticated]
    serializer_class  = ApiCollectorSpiderResourceSerializer


    def get(self,request, format=None):
        """
            获取资源列表
        """
        records = ApiCollectorSpiderResourceModel.objects.all()
        # get running records
        running_records = ApiCollectorSpiderRunRecord.objects.filter(
            result=2,name__in=[record.name for record in records]).all()
        return HTTPResponse(
            data=ApiCollectorSpiderResourceSerializer(instance=records,running_records=running_records,many=True).data
        )    
    

    def post(self,request):
        """
            创建一个脚本 
        """
        # print(request.data)
        if ApiCollectorSpiderResourceModel.objects.filter(name=request.data.get("name")).exists():
            return HTTPResponse(
                code=-1,
                status=status.HTTP_400_BAD_REQUEST,
                message=f"名字为[{request.data.get('name')}]已经存在,请重新命名"
            )
        request.data.update({"user":request.user.id})
        serializer = ApiCollectorSpiderResourceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)

        return HTTPResponse(
            message=f"脚本[{request.data.get('name')}]创建成功"
        )
    
    def put(self,request):
        """
            激活一个脚本
        """
