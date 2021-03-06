# Generated by Django 3.2.3 on 2021-10-05 04:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_delete_sitescomments'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleComments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
                ('body', models.TextField(help_text='评论内容', null=True, verbose_name='评论内容')),
                ('qq', models.CharField(help_text='留言人QQ', max_length=64, null=True, verbose_name='留言人qq')),
                ('email', models.EmailField(help_text='留言人邮箱', max_length=254, null=True, verbose_name='留言人邮箱')),
                ('is_valid', models.BooleanField(default=True, help_text='是否合法(显示)', verbose_name='是否合法(显示)')),
                ('name', models.CharField(default='游客', help_text='留言用户姓名', max_length=64, verbose_name='留言用户姓名')),
                ('ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='调用的IP地址')),
                ('loc_province', models.CharField(max_length=256, null=True, verbose_name='调用地址(省份)')),
                ('loc_country', models.CharField(max_length=256, null=True, verbose_name='调用地址(国家)')),
                ('loc_city', models.CharField(max_length=256, null=True, verbose_name='调用地址(城市)')),
                ('article', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment_to_article', to='articles.article')),
                ('replay_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sitecomment_replay_to', to='articles.articlecomments')),
            ],
            options={
                'verbose_name': '文章评论',
                'verbose_name_plural': '文章评论',
                'db_table': 'article_comments',
                'ordering': ('created',),
            },
        ),
    ]
