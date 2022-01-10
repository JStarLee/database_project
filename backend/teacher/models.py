from django.db import models

# Create your models here.

class TeacherUsers(models.Model):
    tid = models.CharField(primary_key=True,max_length=30)
    t_username = models.CharField(max_length=10)
    t_password = models.CharField(max_length=20)
    class Meta:
        db_table='teacher_users'

class Teacher(models.Model):        # 继承Django已经写好的增删查改
    tid = models.CharField(primary_key=True,max_length=30)
    name = models.CharField(max_length=10)
    sex = models.CharField(max_length=5, choices=(('1','男'),('2','女')),null=True,blank=True)
    photo = models.ImageField(max_length=100,default='http://127.0.0.1:8000/upload/teacher_default.jpg')        #回头写路径
    admission_time  = models.DateField(auto_now_add=True)         #记录入学（创建该对象）时间
    be_good_at = models.CharField(max_length=5,choices=(('1','楷书'),('2','行书')),null=True,blank=True)
    intro = models.CharField(max_length=200, default='书法爱好者一名~')
    class Meta:
        db_table='teacher'
