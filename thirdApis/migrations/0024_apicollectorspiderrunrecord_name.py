# Generated by Django 4.0.4 on 2022-11-07 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thirdApis', '0023_alter_apicollector_expire_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='apicollectorspiderrunrecord',
            name='name',
            field=models.CharField(default=3, help_text='脚本名称', max_length=128, verbose_name='脚本名称'),
            preserve_default=False,
        ),
    ]