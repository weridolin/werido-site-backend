# Generated by Django 4.0.4 on 2023-02-15 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('thirdApis', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chatgptmessage',
            name='conversation_id',
        ),
    ]