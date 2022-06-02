# Generated by Django 3.2.7 on 2022-03-25 01:54

import authentication.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='权限名字')),
                ('url', models.CharField(blank=True, max_length=300, null=True, verbose_name='权限url地址')),
                ('icon', models.CharField(blank=True, max_length=300, null=True, verbose_name='权限图标')),
                ('type', models.CharField(choices=[('menu', 'menu'), ('button', 'button')], default='menu', max_length=32, verbose_name='类型')),
                ('pid', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='authentication.permission', verbose_name='父级权限')),
            ],
            options={
                'verbose_name': 'api权限表',
                'verbose_name_plural': 'api权限表',
                'db_table': 'permissions',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('name', models.CharField(default='guest', max_length=256, unique=True, verbose_name='角色名称')),
                ('description', models.CharField(max_length=256, null=True, verbose_name='描述')),
                ('permissions', models.ManyToManyField(related_name='role_permission', to='authentication.Permission', verbose_name='角色拥有的权限')),
            ],
            options={
                'verbose_name': '角色表',
                'verbose_name_plural': '角色表',
                'db_table': 'role',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('age', models.IntegerField(blank=True, null=True, verbose_name='年龄')),
                ('location', models.CharField(blank=True, max_length=127, null=True, verbose_name='所在地')),
                ('QQ', models.CharField(blank=True, max_length=127, null=True, verbose_name='qq')),
                ('telephone', models.CharField(blank=True, db_index=True, max_length=127, null=True, verbose_name='电话')),
                ('gender', models.CharField(default='man', max_length=16)),
                ('avator', models.ImageField(max_length=127, upload_to=authentication.models.user_directory_path, verbose_name='用户头像')),
                ('first_login', models.BooleanField(default=True, verbose_name='是否首次登录')),
            ],
            options={
                'verbose_name': '用户档案',
                'verbose_name_plural': '用户档案',
                'db_table': 'user_profile',
            },
        ),
        migrations.CreateModel(
            name='UserRoleMemberShip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.role', verbose_name='角色名称')),
                ('userprofile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.userprofile', verbose_name='角色对应的用户')),
            ],
            options={
                'verbose_name': '用户角色关系表',
                'verbose_name_plural': '用户角色关系表',
                'db_table': 'user_role',
            },
        ),
        migrations.AddField(
            model_name='userprofile',
            name='roles',
            field=models.ManyToManyField(blank=True, related_name='user_roles', through='authentication.UserRoleMemberShip', to='authentication.Role', verbose_name='具有的所有角色'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
