# Generated by Django 4.0.4 on 2024-04-07 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thirdApis', '0005_gptconversation_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gptconversation',
            name='platform',
            field=models.CharField(choices=[('chatGPT', 'chatGPT'), ('通义千问', '通义千问')], help_text='平台名称', max_length=64, verbose_name='平台名称'),
        ),
        migrations.AlterField(
            model_name='gptmessage',
            name='interrupt_reason',
            field=models.CharField(blank=True, help_text='停止类型', max_length=128, null=True, verbose_name='停止类型'),
        ),
    ]
