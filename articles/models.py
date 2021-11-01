import datetime
from django.db.models import fields
from django.db.models.expressions import F
from django.urls import reverse

from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from django.contrib.auth.models import User
from django.utils import timezone
import time
from core.base import BaseModel, TypesChoice

# Create your models here.
LEXERS = [item for item in get_all_lexers() if item[1]]
# 语言选择
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
# 风格选择
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class Types(BaseModel):
    class Meta:
        db_table = "types"
        verbose_name = "类别"
        verbose_name_plural = "类别"
    name = models.CharField(null=True, max_length=255,unique=True,
                            help_text="名称", verbose_name="分类名称")
    pid = models.ForeignKey(to="self", on_delete=models.CASCADE,
                            db_constraint=False, verbose_name="父级分类", null=True, blank=True)
    description = models.TextField(
        null=True, help_text="描述", verbose_name="类型描述")
    type = models.CharField(max_length=64, verbose_name="类别对应的模型",
                            choices=TypesChoice, default="article", null=False, blank=False)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Tags(BaseModel):
    class Meta:
        db_table = "tags"
        verbose_name = "标签"
        verbose_name_plural = "标签"
    name = models.CharField(null=True, max_length=255,unique=True,
                            help_text="名称", verbose_name="标签名称")
    description = models.TextField(
        null=True, help_text="描述", verbose_name="标签描述")
    type = models.CharField(max_length=64, verbose_name="标签对应的模型",
                            choices=TypesChoice, default="article", null=False, blank=False)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name


class Projects(BaseModel):
    Project_Status = [
        ("dev", "development"),
        ("finish", "finish")
    ]

    class Meta:
        db_table = "projects"
        verbose_name = "项目"
        verbose_name_plural = "项目"
    name = models.CharField(max_length=256, verbose_name="项目名称", null=False)
    summary = models.TextField(verbose_name="项目描述", null=True)
    url = models.CharField(max_length=128, verbose_name="项目地址")
    status = models.CharField(max_length=32, verbose_name="项目状态",
                              choices=Project_Status, default="dev", null=False, blank=False)


class Article(BaseModel):
    class Meta:
        db_table = "articles"
        verbose_name = "博客文章"
        verbose_name_plural = "博客文章"
        ordering = ('created',)
    # auto_now = True   # 这个参数的默认值为false，设置为true时，能够在保存该字段时，
    # 将其值设置为当前时间，并且每次修改model，都会自动更新。
    # 因此这个参数在需要存储“最后修改时间”的场景下，十分方便。需要注意的是，
    # 设置该参数为true时，并不简单地意味着字段的默认值为当前时间，
    # 而是指字段会被“强制”更新到当前时间，你无法程序中手动为字段赋值；
    # 如果使用django再带的admin管理器，那么该字段在admin中是只读的
    # updated = models.DateTimeField(
    #     auto_now=True, help_text="最后一次更新时间", verbose_name="更新时间",null=True)

    # auto_now_add = True   这个参数的默认值也为False，设置为True时，会在model对象第一次被创建时，
    # 将字段的值设置为创建时的时间，以后修改对象时，字段的值不会再更新。该属性通常被用在存储“创建时间”的场景下。
    # 与auto_now类似，auto_now_add也具有强制性，一旦被设置为True，就无法在程序中手动为字段赋值，
    # 在admin中字段也会成为只读的。
    # created = models.DateTimeField(
    #     default=timezone.now, help_text="创建时间", verbose_name="创建时间",null=True)

    title = models.CharField(max_length=255, null=True,
                            help_text="标题", verbose_name="标题")
    summary = models.TextField(null=True, help_text="概括", verbose_name="概括")
    content = models.TextField(null=True, help_text="正文", verbose_name="正文")
    likes = models.IntegerField(
        help_text="文章点赞数", verbose_name="文章点赞数", default=0, null=True)

    # 一篇文章对应一个分类，一个分类对应多个文章，分类删除时文章也都删除，分类表为父表
    # type 对应Types的ID
    # FOREGINKEY 参数详解
    type = models.ForeignKey(Types, on_delete=models.SET_NULL, null=True)

    # 文章可以没有标签，因此为标签tags指定了blank = True
    tags = models.ManyToManyField(Tags, blank=True, null=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    # 代码高亮选择
    language = models.CharField(null=True,
                                choices=LANGUAGE_CHOICES, default='python', max_length=100)

    style = models.CharField(choices=STYLE_CHOICES, null=True,
                            default='friendly', max_length=100)

    # 文章浏览量
    # PositiveIntegerField是用于存储正整数的字段
    # default=0设定初始值从0开始
    total_views = models.PositiveIntegerField(default=0, null=True)

    # 文章缩略图图  例如 media/blog/20190226
    # avatar = models.ImageField(upload_to='blog/%Y%m%d/', blank=True,null=True)
    avatar = models.CharField(max_length=254, blank=True, null=True)

    # 文章封面图
    # cover = models.ImageField(upload_to='blog/%Y%m%d/', blank=True,null=True)
    cover = models.CharField(max_length=254, blank=True, null=True)

    head_show = models.BooleanField(default=True, null=True)

    # 是否显示版权所有

    copyright_show = models.BooleanField(default=True, null=True)

    # 是否显示评论
    message_show = models.BooleanField(default=True, null=True)

    # 上一篇文章
    pre = models.ForeignKey("self", on_delete=models.CASCADE, verbose_name="上一篇文章",
                            null=True, blank=True, default=None, related_name="pre_article")

    # 下一篇文章
    next = models.ForeignKey("self", on_delete=models.CASCADE, verbose_name="下一篇文章",
                            null=True, blank=True, default=None, related_name="next_article")

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title

    def created_time_format(self):
        return str(self.created)

    # 保存时处理图片 save()是model内置的方法，它会在model实例每次保存时调用。这里改写它，将处理图片的逻辑“塞进去”
    def save(self, *args, **kwargs):
        # 调用原有的 save() 的功能
        article = super(Article, self).save(*args, **kwargs)
        # super(ArticlePost, self).save(*args, **kwargs)
        # 的作用是调用父类中原有的save()
        # 方法，即将model中的字段数据保存到数据库中。因为图片处理是基于已经保存的图片的，
        # 所以这句一定要在处理图片之前执行，否则会得到找不到原始图片的错误

        # 固定宽度缩放图片大小
        # if self.avatar and not kwargs.get('update_fields'):
        #     # article_detail()视图中为了统计浏览量而调用了save(update_fields=['total_views'])
        #     # 为了排除掉统计浏览量调用的save()，免得每次用户进入文章详情页面都要处理标题图
        #     image = Image.open(self.avatar)
        #     (x, y) = image.size
        #     new_x = 640
        #     new_y = 450
        #     resized_image = image.resize((new_x, new_y), Image.ANTIALIAS)
        #     resized_image.save(self.avatar.path)

        return article

    # 获取文章地址
    def get_absolute_url(self):
        return reverse('blog:article-detail', args=[self.id])

    def article_tags(self):
        tag_ids_objects = Tags.objects.get(article_id=self.id)
        for i in tag_ids_objects:
            tag_name = Tags.objects.get(id=i.Tags_id)



class ArticleComments(BaseModel):

    class Meta:
        db_table = "article_comments"
        verbose_name = "文章评论"
        verbose_name_plural = "文章评论"
        ordering = ('created',)
    
    body = models.TextField(help_text="评论内容", verbose_name="评论内容", null=True)

    qq = models.CharField(max_length=64, help_text="留言人QQ",
                        verbose_name="留言人qq", null=True)

    email = models.EmailField(
        help_text="留言人邮箱", verbose_name="留言人邮箱", null=True)

    is_valid = models.BooleanField(
        help_text="是否合法(显示)", verbose_name="是否合法(显示)", default=True)

    name = models.CharField(max_length=64, help_text="留言用户姓名",
                            verbose_name="留言用户姓名", default="游客")

    ip = models.GenericIPAddressField(
        verbose_name="调用的IP地址", null=True, blank=True)

    loc_province = models.CharField(
        max_length=256, verbose_name="调用地址(省份)", null=True)
    loc_country = models.CharField(
        max_length=256, verbose_name="调用地址(国家)", null=True)
    loc_city = models.CharField(
        max_length=256, verbose_name="调用地址(城市)", null=True)

    replay_to =models.ForeignKey("self",on_delete=models.CASCADE,related_name="sitecomment_replay_to",null=True,blank=True)

    article = models.ForeignKey(Article,on_delete=models.CASCADE,related_name="comment_to_article",null=False,blank=False)
        
