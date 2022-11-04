from distutils import log
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from utils.http_ import HTTPResponse
from thirdApis.models import ApiCollectorSpiderRunRecord
from thirdApis.apiCollector.serializers import ApiCollectorSpiderRunRecordSerializer
import datetime,os,sys
from django.conf import settings
import subprocess
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rbac.permission import RbacModelPermission

class TaskOperationView(APIView):

    # permission默认view,即为get不加权限限制.
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,RbacModelPermission]
    queryset = ApiCollectorSpiderRunRecord.objects.all()

    def get(self, request, format=None):
        """
            Return a list of all users.
        """
        print(type(request.user),request.user)
        only_running = request.data.get("only_running")
        if only_running:
            records = ApiCollectorSpiderRunRecord.objects.filter(result=2).all()
        else:
            records = ApiCollectorSpiderRunRecord.objects.all()
        return HTTPResponse(
            data=ApiCollectorSpiderRunRecordSerializer(records,many=True).data
        )    


    def post(self, request, format=None):
        run_at_once = request.data.get("run_at_once")
        if run_at_once:
            log_path,pid = self._start_spider()
            run_record = ApiCollectorSpiderRunRecord(
                pid = pid,
                log_path = log_path,
            )
            run_record.save()
            return HTTPResponse(
                message="spider启动成功!"
            )

        else:
            return HTTPResponse(
                message="api-collector-spider会固定在周末启动"
            )

    def _start_spider(self):
        time =  datetime.datetime.strftime(datetime.datetime.now(),"%Y-%m-%d-%H-%M-%S")
        log_path = os.path.join(settings.LOG_ROOT,f"{time}_spider.log")
        pid_path = os.path.join(settings.LOG_ROOT,f"spider_pid.txt")
        scrapy_cmd = f"scrapy crawl ApisSpider_TianYan --logfile {log_path} --pidfile {pid_path}"
        python_exc = sys.executable
        cmd = f"{python_exc} -m {scrapy_cmd}"
        print("exec command",cmd)
        p = subprocess.Popen(args=cmd,cwd=settings.SPIDER_DIR)
        return log_path,p.pid



