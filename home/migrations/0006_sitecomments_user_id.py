# Generated by Django 4.0.4 on 2023-08-10 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_backgroundmusic_table_alter_friendslink_table_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitecomments',
            name='user_id',
            field=models.IntegerField(blank=True, help_text='留言用户ID', null=True, verbose_name='留言用户ID'),
        ),
    ]
