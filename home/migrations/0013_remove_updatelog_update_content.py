# Generated by Django 4.0.4 on 2023-09-02 16:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_updatelog_commit_content_updatelog_commit_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='updatelog',
            name='update_content',
        ),
    ]
