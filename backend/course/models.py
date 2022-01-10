from re import T
from typing import ChainMap
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL
from django.db.models.fields import CharField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from student.models import Student

# Create your models here.

class Course(models.Model):        # 继承Django已经写好的增删查改
    cid = models.CharField(primary_key=True,max_length=30)
    name = models.CharField(max_length=20)
    choosed_sum = models.IntegerField(default=0)
    fcourse = models.ForeignKey('Course',blank=True, null=True, related_name='course_self',on_delete=SET_NULL)
    intro = models.CharField(max_length=200, default='精品书法课程')
    admission_time  = models.DateField(auto_now_add=True)         #记录入学（创建该对象）时间
    photo = models.ImageField(max_length=100,default='http://127.0.0.1:8000/upload/default.jpg')        #回头写路径
    class Meta:
        db_table='course'

class section(models.Model):
    # id = models.CharField(primary_key=True)
    sec_id = models.CharField(primary_key=True ,max_length=8)
    choosed = models.IntegerField(verbose_name='已选人数',default='0')
    capacity = models.IntegerField(verbose_name='课容量',default='50')
    start = models.DateField(null=False,blank=False)
    end = models.DateField(null=False,blank=False)
    classroom = models.ForeignKey('classroom',related_name='section_self', null  = True,on_delete=SET_NULL)
    Course = models.ForeignKey('Course',related_name='section_self',on_delete=CASCADE)
    time_slot = ManyToManyField('time_slot',related_name='time_slot')
    
class take(models.Model):
    Student = models.ForeignKey('student.Student',related_name='take_self',on_delete=CASCADE) #关联 #student.Student必须使用完整包名！
    status = models.CharField(max_length=10,choices=(('ing','上课中'),('todo','待开课'),('ed','上课中')))
    section = models.ForeignKey('section',related_name='take_self',on_delete=CASCADE) #关联
    # evaluation = models.ForeignKey('evaluation',on_delete=models.SET_NULL)

class teach(models.Model):
    Teacher = models.ForeignKey('teacher.Teacher',related_name='teach_self',on_delete=CASCADE)
    status = models.CharField(max_length=10,choices=(('ing','上课中'),('todo','待开课'),('ed','上课中')))
    section = models.ForeignKey('section',related_name='teach_self',on_delete=CASCADE) #关联

class time_slot(models.Model):
    time_slot_id = models.CharField(primary_key=True ,max_length=10)
    day = models.CharField(max_length=5, choices=((1,'周一'),(2,'周二'),(3,'周三'),(4,'周四'),(5,'周五'),(6,'周六'),(7,'周日')))
    start = models.DateTimeField(null=False,blank=False)
    end = models.DateTimeField(null=False,blank=False)

    #可以设置
class classroom(models.Model):
    classroom_id = CharField(primary_key=True,max_length=4)
    name = CharField(max_length=10)
    address = CharField(max_length=30,unique=True)