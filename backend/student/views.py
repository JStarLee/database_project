import json, urllib.parse

from rest_framework import viewsets

from rest_framework.response import Response
from django.db import transaction
from student.serializers import StudentUsersSerializer, StudentDetailSerializer
from .models import StudentUsers, Student
from users.models import myUser
from rest_framework.views import APIView
from .pagination import MyLimitOffsetPagination
# Create your views here.

class StudentUsersViewSet(viewsets.ModelViewSet):
    queryset = StudentUsers.objects.all()
    serializer_class = StudentUsersSerializer


class StudentListView(APIView):
    # authentication_classes = [Authentication]   #  添加认证
    # permission_classes = []      # 不尽兴权限控制

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
            userInfoList = Student.objects.order_by('sid')
        else:
            userInfoList = Student.objects.filter(**queryset).order_by('sid')

        if userInfoList.exists() == False:
            return Response(ret)

        # 获取分页并做序列化
        page = MyLimitOffsetPagination()
        page_roles = page.paginate_queryset(
            queryset=userInfoList, request=request, view=self)
        roles_ser = StudentDetailSerializer(instance=page_roles, many=True)
        for item in roles_ser.data:
            print(item)
            item['photo']=urllib.parse.unquote(item['photo'])
            print(item)
        ret['msg'] = '成功'
        ret['data'] = roles_ser.data
        ret['lens'] = len(userInfoList)

        return Response(ret)

class addStudentView(APIView):
    @transaction.atomic
    def post(self, request):
        print(request.data)
        req = request.data
        # 获得sid

        #数据过滤
        toPop=[]
        for key in req:
            if req[key]=='':
                toPop.append(key)
        for key in toPop:
            req.pop(key)
        if(Student.objects.all().exists()==False):
            next_num= 10001
        else:
            next_num = int(Student.objects.last().sid[1:]) + 1
        print(next_num)
        id = 's'+'{:0>5d}'.format(next_num)
        req['sid'] = id
        Student.objects.create(**req)
        myUser.objects.create_user(username=req['name'],password='123456', email='example@example.com', roles='2', uid=id)
        # 系统创建用户，默认密码为123456
        response = {
            'code': 20000,
            # 'data': {'student': serializer.data[0]}
            # 'success': 'true',
            # 'message': '请求成功'
        }
        return Response(response)

class deleteStudentView(APIView):
    @transaction.atomic
    # authentication_classes = [Authentication]   #  添加认证
    # permission_classes = []      # 不尽兴权限控制

    def delete(self, request, pk):
        ret = {'code': 20000, 'msg': None, 'data': None, 'lens': None}
        studentDeleting = Student.objects.filter(sid=pk)
        if studentDeleting.exists() == False:
            ret['code'] = 10000
            return Response(ret)
        # print(studentDeleting)
        ret['msg'] = '成功'
        ret['data'] = StudentDetailSerializer(studentDeleting, many=True).data
        studentDeleting.delete()
        myUser.objects.filter(uid=pk).delete()
        return Response(ret)

class updateStudentView(APIView):
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
        Student.objects.filter(sid=pk).update(**req)
        req['sid'] = pk

        student = Student.objects.filter(sid=pk)
        serializer = StudentDetailSerializer(student, many=True)
        serializer.data[0]['photo']=urllib.parse.unquote(serializer.data[0]['photo'])

        response = {
            'code': 20000,
            'data': {'student': serializer.data[0]},
            'success': 'true',
            'message': '请求成功'
        }
        return Response(response)


class getStudentView(APIView):
    def get(self, request, pk):

        student = Student.objects.filter(sid=pk)

        serializer = StudentDetailSerializer(student, many=True)
        serializer.data[0]['photo']=urllib.parse.unquote(serializer.data[0]['photo'])

        response = {
            'code': 20000,
            'data': {'student': serializer.data[0]},
            'success': 'true',
            'message': '请求成功'
        }
        return Response(response)

class getAllStudent(APIView):
    def get(self, request):
        student = Student.objects.all()
        serializer = StudentDetailSerializer(student, many=True)
        for item in serializer.data:
            print(item)
            item['photo']=urllib.parse.unquote(item['photo'])
            print(item)

        response = {
            'code': 20000,
            'data': {'allStudent': serializer.data},
            'success': 'true',
            'message': '请求成功'
        }
        return Response(response) 


