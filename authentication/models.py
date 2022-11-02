'''
Description: 
email: 359066432@qq.com
Author: lhj
software: vscode
Date: 2021-09-11 15:01:27
platform: windows 10
LastEditors: lhj
LastEditTime: 2021-11-29 00:30:37
'''

from statistics import mode
from django.db import models
from django.contrib.auth.models import User
from importlib_metadata import NullFinder
from core.base import BaseModel
# Create your models here.


def user_directory_path(instance, filename):

    return 'user/profiles/user_{0}/avator{1}'.format(instance.user.id, filename)


class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age = models.IntegerField(verbose_name="年龄", null=True, blank=True)
    location = models.CharField(max_length=127, verbose_name="所在地", null=True, blank=True)
    QQ = models.CharField(max_length=127, verbose_name="qq", null=True, blank=True)
    telephone = models.CharField(max_length=127, verbose_name="电话", null=True, blank=True, db_index=True)
    gender = models.CharField(max_length=16, default="man")
    avator = models.ImageField(upload_to=user_directory_path, max_length=127, verbose_name="用户头像")

    first_login = models.BooleanField(verbose_name="是否首次登录",default=True) # 首次登录前端提示要完善个人资料

    # roles = models.ManyToManyField(
    #     verbose_name='具有的所有角色',
    #     to="Role",
    #     blank=True,
    #     related_name="user_roles",
    #     through="UserRoleMemberShip",
    #     through_fields=("userprofile","role"))

    class Meta:
        db_table = 'user_profile'
        verbose_name = '用户档案'
        verbose_name_plural = '用户档案'


    @classmethod
    def get_db_fields(cls):
        return ["QQ","location","telephone","gender","avator","age"]
    
    def save(self, *args,**kwargs) -> None:
        # print(type(self.avator))
        return super().save(*args,**kwargs)


oauth_type =(
    (1, "qq"),
    (2, "wechat"),
    (3, "weibo"),
    (4, "github"),
    (5, "gitee"),
)
class ThirdOauthInfo(BaseModel):
    class Meta:
        db_table = 'third_auth_info'
        verbose_name = '第三方登录信息表'
        verbose_name_plural = verbose_name

    user = models.OneToOneField(User,on_delete=models.CASCADE ,db_constraint=False, related_name='third_oauth',null=True,blank=True)
    oauth_type = models.SmallIntegerField( verbose_name="第三方登录类型", null=False, blank=False,choices=oauth_type)
    oauth_id = models.IntegerField(null=False,blank=False,verbose_name="用户ID")
    oauth_count = models.CharField(max_length=128,verbose_name="登陆的账户",null=True,blank=True)
    oauth_name = models.CharField(max_length=128,verbose_name="登录用户名",null=True,blank=True)
    oauth_phone = models.CharField(max_length=128,verbose_name="手机号",null=True,blank=True)
    oauth_email = models.EmailField(verbose_name="登录的邮箱",null=True,blank=True)
    oauth_avatar_url = models.CharField(max_length=256,verbose_name="头像链接url",null=True,blank=True)
    is_bind = models.BooleanField(verbose_name="是否已经绑定账户",null=False,blank=False,default=False)

    @classmethod
    def from_gitee(cls,*args,**kwargs):
        return cls(
            oauth_type=5,
            oauth_id = kwargs.get("id",None),
            oauth_count = kwargs.get("login",None),
            oauth_phone = kwargs.get("phone",None),
            oauth_email = kwargs.get("email",None),
            oauth_avatar_url = kwargs.get("avatar_url",None),
            oauth_name = kwargs.get("name",None)
        )


    def update(self,data):
        if isinstance(data,dict):
            print(data)
            if self.oauth_type == 5:
                ## update gitee user info
                self.oauth_id = data.get("id",None)
                self.oauth_count = data.get("login",None)
                self.oauth_phone = data.get("phone",None)
                self.oauth_email = data.get("email",None)
                self.oauth_avatar_url = data.get("avatar_url",None)
                self.oauth_name = data.get("name",None)
        else:
            raise TypeError(">>> auth info can only support dict")
        self.save()
        

# class UserRoleMemberShip(BaseModel):
#     userprofile= models.ForeignKey(UserProfile,verbose_name="角色对应的用户",on_delete=models.CASCADE)
#     role = models.ForeignKey('Role',verbose_name="角色名称",on_delete=models.CASCADE)
    
#     class Meta:
#         db_table = "user_role"
#         verbose_name = u'用户角色关系表'
#         verbose_name_plural = verbose_name   


# Create your models here.
################################## RBAC #############################
# 身份分类
# role_choices = (
#     ("1", "admin"),
#     ("2", "guest"),
#     ("3", "normal"),
#     ("4", "VIP1"),
#     ("5", "VIP2"),
#     ("6", "VIP3"),
# )

# class Role(BaseModel):
#     # default admin/guest/normal
#     # role_choices = (
#     #     ("1", "admin"),
#     #     ("2", "guest"),
#     #     ("3", "normal"),
#     #     ("4", "VIP1"),
#     #     ("5", "VIP2"),
#     #     ("6", "VIP3"),
#     # )
#     name = models.CharField(max_length=256, verbose_name="角色名称",null=False, blank=False, unique=True, default="guest")
#     permissions = models.ManyToManyField(to="Permission", related_name="role_permission", verbose_name="角色拥有的权限")
#     description = models.CharField(max_length=256,verbose_name="描述",null=True)

#     class Meta:
#         db_table = 'role'
#         verbose_name = '角色表'
#         verbose_name_plural = verbose_name

#     def __str__(self) -> str:
#         return self.name

# class Permission(BaseModel):
    
#     type_choice = [("menu", "menu"), ("button", "button")]
#     name = models.CharField(max_length=256, verbose_name="权限名字", unique=True, null=False, blank=False)
#     url = models.CharField(max_length=300, verbose_name="权限url地址", null=True, blank=True)
#     icon = models.CharField(max_length=300, verbose_name="权限图标", null=True, blank=True)
#     type = models.CharField(max_length=32, verbose_name="类型",default="menu", 
#         null=False, blank=False, choices=type_choice)
#     # menu = models.ForeignKey(to="Menu",db_constraint=False,verbose_name="对应的菜单",blank=True,null=True,on_delete=models.CASCADE)
#     pid = models.ForeignKey("self", db_constraint=False, verbose_name="父级权限",
#         on_delete=models.CASCADE, null=True, blank=True)

#     def __str__(self) -> str:
#         return f"{self.name}"

#     class Meta:
#         db_table = 'permissions'
#         verbose_name = u"api权限表"
#         verbose_name_plural = u"api权限表"
#         ordering = ["id"]


