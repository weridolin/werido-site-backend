from django.apps import AppConfig
import datetime,os,sys
class ThirdapisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'thirdApis'


    def ready(self) -> None:
        # 创建内置的spider脚本资源
        print("update builtin spider script resource...")
        # from thirdApis.models import ApiCollectorSpiderResourceModel
        # from django.conf import settings
        # from django.contrib.auth.models import User

        # user = User.objects.filter(is_superuser=True).first()
        # ApiCollectorSpiderResourceModel.objects.update_or_create(
        #     name="ac-spider-天眼数据",
        #     defaults={
        #         "script_path":os.path.join(settings.SPIDER_DIR,"spiders","apis_info_spider.py"),
        #         "user":user,
        #         "description":"天眼数据平台api信息采集spider"
        #     },

        # )


        return super().ready()
