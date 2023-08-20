# Generated by Django 4.0.4 on 2023-08-19 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_remove_updatelog_author_updatelog_repo_uri_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='updatelog',
            name='commit_content',
            field=models.TextField(blank=True, null=True, verbose_name='提交详细内容'),
        ),
        migrations.AddField(
            model_name='updatelog',
            name='commit_id',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='提交ID'),
        ),
        migrations.AddField(
            model_name='updatelog',
            name='commit_message',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='提交信息'),
        ),
    ]
