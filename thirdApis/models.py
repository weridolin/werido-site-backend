from django.db import models

# Create your models here.
from core.base import BaseModel


SrcTypes = [
    ("self","self"),
    ("xl","xl"),    
    ("tx","tx"),   
]
class ShortUrlRecords(BaseModel):
    class Meta:
        db_table = "short_uri_records"
        verbose_name = "短链接记录"
        verbose_name_plural = "短链接记录"
        unique_together = (
            ('type','url'),  # 联合唯一
        )
    url = models.URLField(null=False,help_text="url", verbose_name="url")
    short_flag = models.CharField(max_length=64,null=True,default="undefined",help_text="短链接",verbose_name="短链接")
    description = models.TextField(null=True, help_text="描述", verbose_name="url描述")
    type = models.CharField(max_length=16, verbose_name="类别对应的模型",
                            choices=SrcTypes, default="self", null=False, blank=False)
    expire_time = models.DateTimeField(verbose_name="过期时间",null=False,help_text="过期时间")

    def __unicode__(self):
        return self.short_flag

    def __str__(self):
        return self.short_flag
