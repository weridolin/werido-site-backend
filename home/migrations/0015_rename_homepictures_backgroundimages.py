# Generated by Django 4.0.4 on 2024-03-10 04:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0014_alter_updatelog_finish_time'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='HomePictures',
            new_name='BackGroundImages',
        ),
    ]
