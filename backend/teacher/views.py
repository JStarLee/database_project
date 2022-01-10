import json, urllib.parse
from django.core.paginator import Page
from django.db.models import manager
from rest_framework import viewsets
from django.db import transaction


from rest_framework.response import Response
# from backend.course.serializers import SectionSerializer

from teacher.serializers import TeacherDetailSerializer
from course.serializers import SectionDetailSerializer

from course.models import section

from .models import Teacher
from users.models import myUser
from rest_framework.views import APIView
from .pagination import MyLimitOffsetPagination
# Create your views here.

class TeacherListView(APIView):
    # authentication_classes = [Authentication]   #  添加认证
    # permission_classes = []      # 不尽兴权限控制
    @transaction.atomic
    def get(self, request):
        ret = {'code': 20000, 'msg': None, 'data': None, 'lens': None}

        queryset = request.query_params['Queryset']
        queryset = json.loads(queryset)
        #数据过滤
        toPop=[]
        for key in queryset:
            if queryset[key]=='':
                toPop.append(key)
        for key in toPop:
            queryset.pop(key)
        if queryset == {}:
            userInfoList = Teacher.objects.order_by('tid')
        else:
            userInfoList = Teacher.objects.filter(**queryset).order_by('tid')

        if userInfoList.exists() == False:
            return Response(ret)

        # 获取分页并做序列化
        page = MyLimitOffsetPagination()
        page_roles = page.paginate_queryset(
            queryset=userInfoList, request=request, view=self)
        roles_ser = TeacherDetailSerializer(instance=page_roles, many=True)
        for item in roles_ser.data:
            print(item)
            item['photo']=urllib.parse.unquote(item['photo'])
            print(item)
        ret['msg'] = '成功'
        ret['data'] = roles_ser.data
        ret['lens'] = len(userInfoList)
        userInfoList = TeacherDetailSerializer(userInfoList, many=True)

        currentPage=request.query_params['currentPage']
        pageSize=request.query_params['pageSize']

        ret['hasPrevious'] = currentPage!='1'


        ret['pages'] = (ret['lens']-1) // int(pageSize) +1

        ret['hasNext'] = (int(currentPage)!=ret['pages'])
        ret['current'] = currentPage

        return Response(ret)

class addTeacherView(APIView):
    @transaction.atomic
    def post(self, request):
        print(request.data)
        req = request.data
        # 获得tid

        #数据过滤
        toPop=[]
        for key in req:
            if req[key]=='':
                toPop.append(key)
        for key in toPop:
            req.pop(key)
 
        if(Teacher.objects.all().exists()==False):
            next_num= 10001
        else:
            next_num = int(Teacher.objects.last().tid[1:]) + 1
        print(next_num)
        id = 't'+'{:0>5d}'.format(next_num)
        req['tid'] = id
        Teacher.objects.create(**req)
        myUser.objects.create_user(username=req['name'],password='123456', email='example@example.com', roles='1', uid=id)
        # 系统创建用户，默认密码为123456
        # teacher = Teacher.objects.filter()
        # serializer = TeacherDetailSerializer(teacher, many=True)
        # print(serializer.data)
        response = {
            'code': 20000,
            # 'data': {'teacher': serializer.data[0]},
            'success': 'true',
            'message': '请求成功'
        }
        return Response(response)

class deleteTeacherView(APIView):
    # authentication_classes = [Authentication]   #  添加认证
    # permission_classes = []      # 不尽兴权限控制
    @transaction.atomic
    def delete(self, request, pk):
        ret = {'code': 20000, 'msg': None, 'data': None, 'lens': None}
        teacherDeleting = Teacher.objects.filter(tid=pk)
        if teacherDeleting.exists() == False:
            ret['code'] = 10000
            return Response(ret)
        # print(teacherDeleting)
        ret['msg'] = '成功'
        ret['data'] = TeacherDetailSerializer(teacherDeleting, many=True).data
        
        teacherDeleting.delete()
        myUser.objects.filter(uid=pk).delete()
        return Response(ret)

class updateTeacherView(APIView):
    @transaction.atomic
    def put(self, request, pk):
        print(request.data)
        req = request.data
        #数据过滤
        toPop=[]
        for key in req:
            if req[key]=='':
                toPop.append(key)
        for key in toPop:
            req.pop(key)

        Teacher.objects.filter(tid=pk).update(**req)
        req['tid'] = pk
        teacher = Teacher.objects.filter(tid=pk)
        serializer = TeacherDetailSerializer(teacher, many=True)
        serializer.data[0]['photo']=urllib.parse.unquote(serializer.data[0]['photo'])

        response = {
            'code': 20000,
            'data': {'teacher': serializer.data[0]},
            'success': 'true',
            'message': '请求成功'
        }
        return Response(response)

class getTeacherView(APIView):
    
    def get(self, request, pk):

        teacher = Teacher.objects.filter(tid=pk)

        serializer = TeacherDetailSerializer(teacher, many=True)
        serializer.data[0]['photo']=urllib.parse.unquote(serializer.data[0]['photo'])

        response = {
            'code': 20000,
            'data': {'teacher': serializer.data[0]},
            'success': 'true',
            'message': '请求成功'
        }
        return Response(response)
class getAllTeacher(APIView):
    def get(self, request):
        teacher = Teacher.objects.all()
        serializer = TeacherDetailSerializer(teacher, many=True)
        for item in serializer.data:
            print(item)
            item['photo']=urllib.parse.unquote(item['photo'])
            print(item)

        response = {
            'code': 20000,
            'data': {'allTeacher': serializer.data},
            'success': 'true',
            'message': '请求成功'
        }
        return Response(response) 


class getTeacherFrontInfoView(APIView):
    def get(self, request, pk):

        teacher = Teacher.objects.filter(tid=pk)

        serializerTeacher = TeacherDetailSerializer(teacher, many=True)
        serializerTeacher.data[0]['photo']=urllib.parse.unquote(serializerTeacher.data[0]['photo'])
        sectionObject = section.objects.filter(teach_self__Teacher__tid=pk)
        serializerSection = SectionDetailSerializer(sectionObject, many=True)
        for i in range(len(sectionObject)):
            serializerSection.data[i]['Course']['photo']=urllib.parse.unquote(serializerSection.data[i]['Course']['photo'])
        print(sectionObject)
        response = {
            'code': 20000,
            'data': {
                'teacher': serializerTeacher.data[0],
                'courseList':serializerSection.data},
            'success': 'true',
            'message': '请求成功'
        }
        return Response(response)

