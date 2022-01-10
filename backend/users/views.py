from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, renderer_classes
from django.contrib.auth import get_user_model
from django.db.models.query import QuerySet
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import request
from rest_framework.generics import ListAPIView
import random
from django.db import transaction

from rest_framework_jwt.utils import jwt_decode_handler
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from student.models import Student
from teacher.models import Teacher

from users.serializers import myUserSerializer
from users.serializers import myUserDetailSerializer

from .models import myUser

# Create your views here.

class myUserViewSet(viewsets.ModelViewSet):
    queryset = myUser.objects.all()
    serializer_class = myUserSerializer


User = get_user_model()


# class myUserInfo():


@api_view(['GET', 'POST'])
def info(request):
    if request.method == 'GET':
        token = request.GET.get('token')
        if token==None:
            response = {
                'code': 10000,
                # 'success': 'true',
                # 'message': '请求成功'
            }
            return Response(response)
        # 顶一个空数组来接收token解析后的值
        toke_user = []
        toke_user = jwt_decode_handler(token)
        # 获得user_id
        user_name = toke_user["username"]
        print(user_name)

        # 通过user_id查询用户信息pk
        # user_info = dir(User.objects.get(username= user_name))
        user_info = User.objects.get(username=user_name)

        serializer = myUserDetailSerializer(user_info)
        print(serializer.data)
        response = {
            'code': 20000,
            'data': serializer.data
            # 'success': 'true',
            # 'message': '请求成功'
        }
        return Response(response)
@api_view(['GET', 'POST'])
@transaction.atomic
def register(request):
  
    if request.method == 'POST':
        pass
        form = request.data
        print(form)
        username = form['username']
        password = form['password']
        roles = form['roles']
        
        # 使用内置User自带create_user方法创建用户，不需要使用save()
        id=''
        
        if roles=='2':
            if(Student.objects.all().exists()==False):
                id= 10001
            else:
                id = int(Student.objects.last().sid[1:]) + 1
            id = 's'+'{:0>5d}'.format(id)
            User.objects.create_user(username=username,password=password, email='example@example.com', roles=roles, uid=id)

            Student.objects.create(sid=id,name=username)
        elif roles=='1':
            if(Teacher.objects.all().exists()==False):
                id= 10001
            else:
                id = int(Teacher.objects.last().tid[1:]) + 1
            id = 't'+'{:0>5d}'.format(id)
            User.objects.create_user(username=username,password=password, email='example@example.com', roles=roles, uid=id)
            Teacher.objects.create(tid=id,name=username)

        response = {
            'code': 20000,

        }
        return Response(response)
@api_view(['GET', 'POST'])
def logout(request):
    if request.method == 'POST':

        response = {
            'code': 20000,
            # 'success': 'true',
            # 'message': '请求成功'
        }
        return Response(response)

# @api_view(['GET', 'POST'])
# @transaction.atomic
# def register(request):
  
#     if request.method == 'POST':
#         pass
#         form = request.data
#         print(form)
#         username = form['username']
#         password = form['password']
#         roles = form['roles']
        
#         # 使用内置User自带create_user方法创建用户，不需要使用save()
#         id=''
        
#         if roles=='2':
#             if(Student.objects.all().exists()==False):
#                 id= 10001
#             else:
#                 id = int(Student.objects.last().sid[1:]) + 1
#             id = 's'+'{:0>5d}'.format(id)
#             User.objects.create_user(username=username,password=password, email='example@example.com', roles=roles, uid=id)

#             Student.objects.create(sid=id,name=username)
#         elif roles=='1':
#             if(Teacher.objects.all().exists()==False):
#                 id= 10001
#             else:
#                 id = int(Teacher.objects.last().tid[1:]) + 1
#             id = 't'+'{:0>5d}'.format(id)
#             User.objects.create_user(username=username,password=password, email='example@example.com', roles=roles, uid=id)
#             Teacher.objects.create(tid=id,name=username)

#         response = {
#             'code': 20000,

#         }
#         return Response(response)




