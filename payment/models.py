from django.db import models

# Create your models here.

## 打赏
class Reward(models.Model):
    class Meta:
        db_table = "payment_reward"
        verbose_name = "打赏"
        verbose_name_plural = "打赏"
    id = models.UUIDField(primary_key=True, verbose_name="ID")
    user = models.ForeignKey(to="user.User", on_delete=models.CASCADE,db_constraint=False, verbose_name="用户",null=True,blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="金额")
    pay_time = models.DateTimeField(auto_now_add=True, verbose_name="支付时间", help_text="支付时间")
    # pay_type = models.CharField(max_length=64, verbose_name="支付类型", help_text="支付类型",null=True,blank=True)
    pay_status = models.CharField(max_length=64, verbose_name="支付状态", help_text="支付状态")
    pay_order = models.CharField(max_length=64, verbose_name="支付订单", help_text="支付订单")
    pay_channel = models.CharField(max_length=64, verbose_name="支付渠道", help_text="支付渠道")
    # pay_result = models.TextField(verbose_name="支付结果", help_text="支付结果")
    pay_ip = models.GenericIPAddressField(verbose_name="支付IP", help_text="支付IP")
    pay_device = models.CharField(max_length=64, verbose_name="支付设备", help_text="支付设备")
    pay_location = models.CharField(max_length=64, verbose_name="支付地点", help_text="支付地点")
    pay_user_agent = models.CharField(max_length=255, verbose_name="支付UA", help_text="支付UA")
    # pay_referer = models.CharField( max_length=255, verbose_name="支付来源", help_text="支付来源")
    pay_note = models.TextField(verbose_name="支付备注", help_text="支付备注",null=True,blank=True)
    pay_extra = models.TextField(verbose_name="支付额外信息", help_text="支付额外信息",null=True,blank=True)
    pay_callback = models.CharField(max_length=255, verbose_name="支付回调", help_text="支付回调")
    pay_callback_time = models.DateTimeField(verbose_name="支付回调时间", help_text="支付回调时间",null=True,blank=True)
    pay_callback_status = models.CharField(max_length=64, verbose_name="支付回调状态", help_text="支付回调状态",null=True,blank=True,default="uncallback")
    expire_time = models.DateTimeField(verbose_name="过期时间", help_text="过期时间")
    # pay_callback_result = models.TextField(