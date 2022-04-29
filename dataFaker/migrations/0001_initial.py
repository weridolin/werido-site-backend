# Generated by Django 3.2.3 on 2022-04-28 02:50

import dataFaker.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DataFakerRecordInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('record_key', models.CharField(db_index=True, max_length=255, verbose_name='记录唯一标识')),
                ('is_delete', models.BooleanField(default=False, verbose_name='是否删除')),
                ('expire_time', models.DateTimeField(verbose_name='过期时间')),
                ('file', models.FileField(max_length=255, null=True, upload_to=dataFaker.models.file_directory_path)),
                ('download_code', models.CharField(max_length=255, null=True, verbose_name='文件下载码')),
                ('is_finish', models.BooleanField(default=False, verbose_name='数据是否已经生成完成')),
                ('fields', models.JSONField(default=[], verbose_name='字段集')),
                ('count', models.IntegerField(default=0, verbose_name='数据条数')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='文件上传所属用户')),
            ],
            options={
                'verbose_name': '假数据生成记录表',
                'verbose_name_plural': '假数据生成记录表',
                'db_table': 'faker_record',
            },
        ),
    ]