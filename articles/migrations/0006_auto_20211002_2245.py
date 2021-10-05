# Generated by Django 3.2.3 on 2021-10-02 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0005_auto_20211002_2048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tags',
            name='name',
            field=models.CharField(help_text='名称', max_length=255, null=True, unique=True, verbose_name='标签名称'),
        ),
        migrations.AlterField(
            model_name='types',
            name='name',
            field=models.CharField(help_text='名称', max_length=255, null=True, unique=True, verbose_name='分类名称'),
        ),
    ]
