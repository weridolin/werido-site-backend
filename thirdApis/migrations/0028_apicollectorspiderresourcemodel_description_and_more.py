# Generated by Django 4.0.4 on 2022-11-08 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thirdApis', '0027_alter_apicollectorspiderresourcemodel_last_run_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='apicollectorspiderresourcemodel',
            name='description',
            field=models.TextField(help_text='脚本描述', null=True, verbose_name='脚本描述'),
        ),
        migrations.AddField(
            model_name='apicollectorspiderrunrecord',
            name='err_reason',
            field=models.TextField(help_text='错误信息', null=True, verbose_name='错误信息'),
        ),
    ]
