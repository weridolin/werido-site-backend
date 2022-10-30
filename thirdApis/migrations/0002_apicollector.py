# Generated by Django 4.0.4 on 2022-10-29 09:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thirdApis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiCollector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('platform', models.CharField(default='uncle-lin', help_text='api所属平台', max_length=64, verbose_name='api所属平台')),
                ('is_free', models.BooleanField(default=False, help_text='是否免费', verbose_name='是否免费')),
                ('api_type', models.CharField(default='', help_text='api所属类别', max_length=64, verbose_name='api所属类别')),
                ('api_name', models.CharField(default='unknown', help_text='api名称', max_length=64, verbose_name='api名称')),
                ('api_icon', models.CharField(help_text='api对应的icon', max_length=64, verbose_name='api对应的icon')),
                ('api_url', models.URLField(default='unknown', help_text='api对应的url', verbose_name='api对应的url')),
                ('clicked', models.PositiveIntegerField(default=0, help_text='点击次数', verbose_name='点击次数')),
                ('expire_time', models.DateTimeField(default=datetime.datetime(2022, 11, 5, 17, 50, 46, 670012), help_text='过期时间', verbose_name='过期时间')),
            ],
            options={
                'verbose_name': '各大Api集合',
                'verbose_name_plural': '各大Api集合',
                'db_table': 'api_collector',
            },
        ),
    ]
