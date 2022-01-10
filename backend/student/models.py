from django.db import models

# Create your models here.
class StudentUsers(models.Model):  # 继承Django已经写好的增删查改
    sid = models.CharField(primary_key=True,max_length=30)
    s_username = models.CharField(max_length=10)
    s_password = models.CharField(max_length=20)
    class Meta:
        db_table='student_users'

class Student(models.Model):        # 继承Django已经写好的增删查改
    sid = models.CharField(primary_key=True,max_length=30)
    name = models.CharField(max_length=10)
    sex = models.CharField(max_length=5, choices=(('1','男'),('2','女')),null=True,blank=True)
    photo = models.ImageField(max_length=100,default='http://127.0.0.1:8000/upload/defalut_avatar_1.jpg')        #回头写路径
    admission_time  = models.DateField(auto_now_add=True)         #记录入学（创建该对象）时间
    intro = models.CharField(max_length=200, default='书法爱好者一名~')

    class Meta:
        db_table='student'
