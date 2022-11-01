# Generated by Django 4.0.4 on 2022-11-01 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('group_name', models.CharField(help_text='用户组名称', max_length=128, verbose_name='用户组名称')),
                ('p_id', models.IntegerField(default=-1, help_text='父用户组名称', verbose_name='父用户组名称')),
            ],
            options={
                'verbose_name': 'rbac_用户组',
                'verbose_name_plural': 'rbac_用户组',
                'db_table': 'rbac_group',
            },
        ),
        migrations.CreateModel(
            name='GroupRoleShip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('group_id', models.IntegerField(db_index=True, help_text='用户组id', verbose_name='用户组id')),
                ('role_id', models.IntegerField(db_index=True, help_text='角色id', verbose_name='角色id')),
            ],
            options={
                'verbose_name': 'rbac_组与角色关联表',
                'verbose_name_plural': 'rbac_组与角色关联表',
                'db_table': 'rbac_group_role',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('menu_name', models.CharField(help_text='菜单名称', max_length=128, verbose_name='菜单名称')),
                ('menu_url', models.CharField(help_text='菜单url', max_length=128, verbose_name='菜单url')),
                ('p_id', models.IntegerField(help_text='父级菜单', verbose_name='父级菜单')),
            ],
            options={
                'verbose_name': 'rbac_菜单',
                'verbose_name_plural': 'rbac_菜单',
                'db_table': 'rbac_menu',
            },
        ),
        migrations.CreateModel(
            name='MenuPermissionShip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('menu_id', models.IntegerField(help_text='菜单id', verbose_name='菜单id')),
                ('permission_id', models.IntegerField(help_text='对应的权限id', verbose_name='对应的权限id')),
            ],
            options={
                'verbose_name': 'rbac_菜单权限关联表',
                'verbose_name_plural': 'rbac_菜单权限关联表',
                'db_table': 'rbac_permission_menu',
            },
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('op_name', models.CharField(help_text='操作名称', max_length=128, verbose_name='操作名称')),
                ('op_model', models.IntegerField(help_text='操作的表', verbose_name='操作的表')),
                ('p_id', models.IntegerField(help_text='父操作ID', verbose_name='父操作ID')),
            ],
            options={
                'verbose_name': 'rbac_表操作权限',
                'verbose_name_plural': 'rbac_表操作权限',
                'db_table': 'rbac_operation',
            },
        ),
        migrations.CreateModel(
            name='OperationPermissionShip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('op_id', models.IntegerField(help_text='操作id', verbose_name='操作id')),
                ('permission_id', models.IntegerField(help_text='对应的权限id', verbose_name='对应的权限id')),
            ],
            options={
                'verbose_name': 'rbac_表操作权限关联表',
                'verbose_name_plural': 'rbac_表操作权限关联表',
                'db_table': 'rbac_operation_permission',
            },
        ),
        migrations.CreateModel(
            name='Permissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('permission_id', models.IntegerField(db_index=True, help_text='对应权限种类表中的ID', verbose_name='对应权限种类表中的ID')),
                ('permission_type', models.IntegerField(db_index=True, help_text='权限类型', verbose_name='权限类型')),
            ],
            options={
                'verbose_name': 'rbac_权限表',
                'verbose_name_plural': 'rbac_权限表',
                'db_table': 'rbac_permission',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('role_name', models.CharField(help_text='用户角色', max_length=128, verbose_name='用户角色')),
            ],
            options={
                'verbose_name': 'rbac_用户角色',
                'verbose_name_plural': 'rbac_用户角色',
                'db_table': 'rbac_role',
            },
        ),
        migrations.CreateModel(
            name='RolePermissionShip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('role_id', models.IntegerField(db_index=True, help_text='角色ID', verbose_name='角色ID')),
                ('permission_id', models.IntegerField(db_index=True, help_text='权限ID', verbose_name='权限ID')),
            ],
            options={
                'verbose_name': 'rbac_角色权限关联表',
                'verbose_name_plural': 'rbac_角色权限关联表',
                'db_table': 'rbac_role_permission',
            },
        ),
        migrations.CreateModel(
            name='UserGroupShip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('group_id', models.IntegerField(db_index=True, help_text='用户组id', verbose_name='用户组id')),
                ('user_id', models.IntegerField(db_index=True, help_text='用户id', verbose_name='用户id')),
            ],
            options={
                'verbose_name': 'rbac_组与用户关联表',
                'verbose_name_plural': 'rbac_组与用户关联表',
                'db_table': 'rbac_group_user',
            },
        ),
        migrations.CreateModel(
            name='UserRoleShip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('user_id', models.IntegerField(db_index=True, help_text='用户id', verbose_name='用户id')),
                ('role_id', models.IntegerField(db_index=True, help_text='角色id', verbose_name='角色id')),
            ],
            options={
                'verbose_name': 'rbac_用户与角色关联表',
                'verbose_name_plural': 'rbac_用户与角色关联表',
                'db_table': 'rbac_user_role',
            },
        ),
    ]
