# Generated by Django 4.0.4 on 2023-08-12 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_alter_sitecomments_replay_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitecomments',
            name='replay_to',
            field=models.IntegerField(default=-1, help_text='回复的评论ID(-1表示父节点)', verbose_name='回复的评论ID'),
        ),
    ]
