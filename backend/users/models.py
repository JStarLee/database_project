from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class myUser(AbstractUser):
    """
    用户类拓展
    """
    uid = models.CharField(max_length=6,null=True)
    name = models.CharField(max_length=30, null=True, blank=True, verbose_name="姓名" )
    avatar = models.CharField(max_length=100, null=True, blank=True, verbose_name="头像",default='http://127.0.0.1:8000/upload/default_superadmin1.png')
    roles = models.CharField(max_length=10,choices=(('1','学生'),('2','教师'),('3','管理员')), default="1", verbose_name="角色")
    

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username