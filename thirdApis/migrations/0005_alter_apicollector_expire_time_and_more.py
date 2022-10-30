# Generated by Django 4.0.4 on 2022-10-30 07:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thirdApis', '0004_apicollectorspiderrunrecord_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apicollector',
            name='expire_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 11, 6, 15, 31, 13, 514099), help_text='过期时间', verbose_name='过期时间'),
        ),
        migrations.AlterField(
            model_name='apicollectorspiderrunrecord',
            name='finish_time',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 30, 15, 31, 13, 515098), help_text='完成时间', verbose_name='完成时间'),
        ),
        migrations.AlterField(
            model_name='apicollectorspiderrunrecord',
            name='result',
            field=models.SmallIntegerField(default=2, help_text='脚本运行结果,成功为0,异常为1,正在运行为2', verbose_name='脚本运行结果,成功为0,异常为1,正在运行为2'),
        ),
    ]
