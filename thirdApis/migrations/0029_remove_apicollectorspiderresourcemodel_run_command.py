# Generated by Django 4.0.4 on 2022-11-09 07:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('thirdApis', '0028_apicollectorspiderresourcemodel_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apicollectorspiderresourcemodel',
            name='run_command',
        ),
    ]