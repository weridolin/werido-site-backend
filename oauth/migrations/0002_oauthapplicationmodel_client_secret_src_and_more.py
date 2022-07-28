# Generated by Django 4.0.4 on 2022-06-05 07:29

from django.db import migrations, models
import oauth2_provider.generators


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='oauthapplicationmodel',
            name='client_secret_src',
            field=models.CharField(blank=True, db_index=True, default=oauth2_provider.generators.generate_client_secret, help_text='secret src code before hash', max_length=255),
        ),
        migrations.AlterField(
            model_name='oauthapplicationmodel',
            name='authorization_grant_type',
            field=models.CharField(choices=[('authorization-code', '授权码'), ('implicit', 'Implicit'), ('password', '账号密码'), ('client-credentials', 'Client credentials'), ('openid-hybrid', 'OpenID connect hybrid')], max_length=32),
        ),
    ]