import json,urllib.parse,datetime
from django.core.paginator import Page
from django.db.models import manager
from rest_framework import viewsets
from datetime import date
from rest_framework.response import Response
from django.db.models import Q,Min,Avg,Max,Sum,F
from .models import Course,section,time_slot,classroom,take,teach
from .serializers import CourseDetailSerializer, CourseSerializer
from .serializers import SectionDetailSerializer, SectionSerializer, SectionSec_idSerializer
from .serializers import Time_slotSerializer, Time_slotIdSerializer,Time_slotDetailSerializer
from .serializers import ClassroomDetailSerializer
from .serializers import TakeDetailSerializer,TakeSerializer
from .serializers import TeachDetailSerializer,TeachSerializer
from django.db import transaction


from rest_framework.views import APIView
from .pagination import MyLimitOffsetPagination
# Create your views here.


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseDetailSerializer


class CourseListView(APIView):
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
            courseInfoList = Course.objects.order_by('cid')
        else:
            courseInfoList = Course.objects.filter(**queryset).order_by('cid')

        if courseInfoList.exists() == False:
            return Response(ret)
        
        # 获取分页并做序列化
        page = MyLimitOffsetPagination()
        page_roles = page.paginate_queryset(
            queryset=courseInfoList, request=request, view=self)
        roles_ser = CourseDetailSerializer(instance=page_roles, many=True)
        for item in roles_ser.data:
            # print(item)
            item['photo']=urllib.parse.unquote(item['photo'])
            # print(item)
        ret['msg'] = '成功'
        ret['data'] = roles_ser.data
        ret['lens'] = len(courseInfoList)
        courseInfoList = CourseSerializer(courseInfoList, many=True)

        currentPage=request.query_params['currentPage']
        pageSize=request.query_params['pageSize']

        ret['hasPrevious'] = currentPage!='1'

        ret['pages'] = (ret['lens']-1) // int(pageSize) +1

        ret['hasNext'] = (int(currentPage)!=ret['pages'])
        ret['current'] = currentPage        

        return Response(ret)

class addCourseView(APIView):
    @transaction.atomic
    def post(self, request):
        # print(request.data)
        req = request.data
        # 获得cid

        #数据过滤
        toPop=[]
        for key in req:
            if req[key]=='':
                toPop.append(key)
        for key in toPop:
            req.pop(key)

        if(Course.objects.all().exists()==False):
            next_num= 30001
        else:
            next_num = int(Course.objects.last().cid) + 1

        req['cid'] = '{:0>5d}'.format(next_num)
        cid = '{:0>5d}'.format(next_num)
        
        #外键无法在创建的时候以id的形式添加，可以在update中按主键添加或在create中以外键_id的形式添加
        if(('fcourse' in req)==True):
            fcourse=req['fcourse']
            req.pop('fcourse')
            Course.objects.create(**req)
            Course.objects.filter(cid=cid).update(fcourse=fcourse)
        else:
            Course.objects.create(**req)

        response = {
            'code': 20000,
            'success': 'true',
            'message': '请求成功'
        }
        return Response(response)

class deleteCourseView(APIView):
    # authentication_classes = [Authentication]   #  添加认证
    # permission_classes = []      # 不尽兴权限控制
    @transaction.atomic
    def delete(self, request, pk):
        ret = {'code': 20000, 'msg': None, 'data': None, 'lens': None}
        courseDeleting = Course.objects.filter(cid=pk)
        if courseDeleting.exists() == False:
            ret['code'] = 10000
            return Response(ret)
        # print(courseDeleting)
        ret['msg'] = '成功'
        ret['data'] = CourseDetailSerializer(courseDeleting, many=True).data

        courseDeleting.delete()
        return Response(ret)

class updateCourseView(APIView):
    @transaction.atomic
    def put(self, request, pk):
        # print(request.data)
        req = request.data
        # 获得cid
        #数据过滤
        toPop=[]
        for key in req:
            if req[key]=='':
                toPop.append(key)
        for key in toPop:
            req.pop(key)

        Course.objects.filter(cid=pk).update(**req)
        if(('fcourse' in req)==True and req['fcourse']!=''):
            Course.objects.filter(cid=pk).update(fcourse=req["fcourse"])
        else:
            Course.objects.filter(cid=pk).update(fcourse=None)
        req['cid'] = pk

        course = Course.objects.filter(cid=pk)
        serializer = CourseSerializer(course, many=True)
        serializer.data[0]['photo']=urllib.parse.unquote(serializer.data[0]['photo'])
        
        response = {
            'code': 20000,
            'data': {'course': serializer.data[0]},
            'success': 'true',
            'message': '请求成功'
        }
        return Response(response)


class getCourseView(APIView):
    def get(self, request, pk):
        # 获得cid

        course = Course.objects.filter(cid=pk)

        serializer = CourseSerializer(course, many=True)
        serializer.data[0]['photo']=urllib.parse.unquote(serializer.data[0]['photo'])

        response = {
            'code': 20000,
            'data': {'course': serializer.data[0]},
            'success': 'true',
            'message': '请求成功'
        }
        return Response(response)

class getAllCourse(APIView):
    def get(self, request):
        course = Course.objects.all()
        serializer = CourseSerializer(course, many=True)
        for item in serializer.data:
            # print(item)
            item['photo']=urllib.parse.unquote(item['photo'])
            # print(item)

        response = {
            'code': 20000,
            'data': {'allCourse': serializer.data},
            'success': 'true',
            'message': '请求成功'
        }
        return Response(response)   

class getFrontCourseInfoView(APIView):
    def get(self, request, pk):
        # 获得cid

        course = Course.objects.filter(cid=pk)

        courseSerializer = CourseSerializer(course, many=True)
        courseSerializer.data[0]['photo']=urllib.parse.unquote(courseSerializer.data[0]['photo'])

        sectionObject = section.objects.filter(Course__cid=pk)

        sectionSerializer = SectionSerializer(sectionObject, many=True)
        # hotIndex=(courseSerializer.data[0]['choosed_sum'],Course.objects.all().aggregate(Sum("choosed_sum"))['choosed_sum__sum'])
        # print(hotIndex)
        if courseSerializer.data[0]['choosed_sum']==0:
            hotIndex=0
        else:
            hotIndex=100*(courseSerializer.data[0]['choosed_sum']/Course.objects.all().aggregate(Sum("choosed_sum"))['choosed_sum__sum'])
            hotIndex=round(hotIndex,2)
        response = {
            'code': 20000,
            'data': {
                'course': courseSerializer.data[0],
                'sectionList':sectionSerializer.data,
                'hotIndex':hotIndex
            },
            'success': 'true',
            'message': '请求成功'
        }
        return Response(response)
#########################################################
#########################################################
#########################################################

class SectionListView(APIView):
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
        sectionInfoList = section.objects.all()
        # print(sectionInfoList)

        if 'Course_name' in queryset:
            sectionInfoList = section.objects.filter(Course__name=queryset['Course_name'])
            queryset.pop('Course_name')
        if 'Teacher_name' in queryset:
            sectionInfoList = sectionInfoList.filter(teach_self__Teacher__name=queryset['Teacher_name'])
            queryset.pop('Teacher_name')
        if 'start_end' in queryset:
            start = queryset['start_end'][0][0:10]
            end = queryset["start_end"][1][0:10]
            sectionInfoList = sectionInfoList.filter(start__gte=start).filter(end__lte=end)
            queryset.pop('start_end')

        if queryset == {}:
            sectionInfoList = sectionInfoList.all().order_by('sec_id')
        else:
            sectionInfoList = sectionInfoList.filter(**queryset).order_by('sec_id')
        
        if sectionInfoList.exists() == False:
            return Response(ret)

        page = MyLimitOffsetPagination()
        page_roles = page.paginate_queryset(
            queryset=sectionInfoList, request=request, view=self)
        roles_ser = SectionDetailSerializer(instance=page_roles, many=True)
        # 想完善的话应该写一个关于url的解码（因为序列化的问题）
        print("jofiaehf")
        print(roles_ser.data)
        ret['msg'] = '成功'
        ret['data'] = roles_ser.data
        # print(ret['data'])
        ret['lens'] = len(sectionInfoList)

        return Response(ret)

class TakeSectionListView(APIView):
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
        sectionInfoList = section.objects.all()
        if 'sid' in queryset:
            start_endList=[]
            classroomList=[]
            CourseList=[]

            sid = queryset['sid']
            queryset.pop('sid')
            # 时间不冲突，时段不冲突，教室不冲突
            hasTake = take.objects.filter(Student__sid=sid)
            hasTake = TakeDetailSerializer(hasTake,many=True).data
            # print(hasTake)
            sectionQ2=None
            if len(hasTake)!=0:
                sectionQ2=section.objects.filter(sec_id='1')

                for item in hasTake:
                    # print(item)
                    # print("sectionQ2-1:")
                    # print(sectionQ2)
                    sectionQ1=section.objects.exclude(start__gte=hasTake[0]['section']['end'])
                    sectionQ1=sectionQ1.exclude(end__lte=hasTake[0]['section']['start'])                
                    for part in item['section']['time_slot']:
                        # time_slotIdList.append(part['time_slot_id'])
                        sectionQ1=sectionQ1.exclude(time_slot__time_slot_id=part['time_slot_id'])
                    start_endList.append([item['section']['start'],item['section']['end']])
                    classroomList.append(item['section']['classroom']['classroom_id'])
                    CourseList.append(item['section']['Course']['cid'])
                    sectionQ2=(sectionQ2|sectionQ1)
                # print("sectionQ2-2:")
                # print(sectionQ2)
                    
            # for item in time_slotIdList:
            #     sectionInfoList=sectionInfoList.exclude(time_slot__time_slot_id=item)

            for item in start_endList:
                sectionInfoList=sectionInfoList.filter(Q(start__gte=item[1])|Q(end__lte=item[0]))
            
            if sectionQ2!=None:
                sectionInfoList=(sectionInfoList|sectionQ2)
            # 注意未来解决左闭右开问题
            for item in classroomList:
                sectionInfoList=sectionInfoList.exclude(classroom__classroom_id=item)
            for item in CourseList:
                sectionInfoList=sectionInfoList.filter(Q(Course__fcourse__cid=item)|Q(Course__fcourse__isnull=True))
            if CourseList==[]:
                sectionInfoList=sectionInfoList.filter(Course__fcourse__isnull=True)
        # print('#####first#####')
        # print(queryset)
            
        if 'Course_name' in queryset:
            sectionInfoList = sectionInfoList.filter(Course__name=queryset['Course_name'])
            queryset.pop('Course_name')
        if 'Teacher_name' in queryset:
            sectionInfoList = sectionInfoList.filter(teach_self__Teacher__name=queryset['Teacher_name'])
            queryset.pop('Teacher_name')
        if 'start_end' in queryset:
            start = queryset['start_end'][0][0:10]
            end = queryset["start_end"][1][0:10]
            sectionInfoList = sectionInfoList.filter(start__gte=start).filter(end__lte=end)
            queryset.pop('start_end')
        sectionInfoList = sectionInfoList.filter(choosed__lt=F('capacity'))
        if queryset == {}:
            sectionInfoList = sectionInfoList.all().order_by('sec_id')
        else:
            sectionInfoList = sectionInfoList.filter(**queryset).order_by('sec_id')

        if sectionInfoList.exists() == False:
            return Response(ret)

        page = MyLimitOffsetPagination()
        page_roles = page.paginate_queryset(
            queryset=sectionInfoList, request=request, view=self)
        roles_ser = SectionDetailSerializer(instance=page_roles, many=True)
        # 想完善的话应该写一个关于url的解码（因为序列化的问题）
        ret['msg'] = '成功'
        ret['data'] = roles_ser.data
        # print(ret['data'])
        ret['lens'] = len(sectionInfoList)

        return Response(ret)

class TeachSectionListView(APIView):
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
        sectionInfoList = section.objects.all()
        if 'tid' in queryset:
            time_slotIdList=[]
            start_endList=[]
            classroomList=[]
            # CourseList=[]

            tid = queryset['tid']
            queryset.pop('tid')
            # 时间不冲突，时段不冲突，教室不冲突
            hasTeach = teach.objects.filter(Teacher__tid=tid)
            hasTeach = TeachDetailSerializer(hasTeach,many=True).data
            # print(hasTeach)
            sectionQ2=None
            if len(hasTeach)!=0:
                sectionQ2=section.objects.filter(sec_id='1')

                for item in hasTeach:
                    # print(item)
                    # print("sectionQ2-1:")
                    # print(sectionQ2)
                    sectionQ1=section.objects.exclude(start__gte=hasTeach[0]['section']['end'])
                    sectionQ1=sectionQ1.exclude(end__lte=hasTeach[0]['section']['start'])                
                    for part in item['section']['time_slot']:
                        # time_slotIdList.append(part['time_slot_id'])
                        sectionQ1=sectionQ1.exclude(time_slot__time_slot_id=part['time_slot_id'])
                    start_endList.append([item['section']['start'],item['section']['end']])
                    classroomList.append(item['section']['classroom']['classroom_id'])
                    sectionQ2=(sectionQ2|sectionQ1)
                # print("sectionQ2-2:")
                # print(sectionQ2)
                    
            # for item in time_slotIdList:
            #     sectionInfoList=sectionInfoList.exclude(time_slot__time_slot_id=item)

            for item in start_endList:
                sectionInfoList=sectionInfoList.filter(Q(start__gte=item[1])|Q(end__lte=item[0]))
            
            if sectionQ2!=None:
                sectionInfoList=(sectionInfoList|sectionQ2)
            # 注意未来解决左闭右开问题
            for item in classroomList:
                sectionInfoList=sectionInfoList.exclude(classroom__classroom_id=item)

            # for item in hasTeach:
            #     for part in item['section']['time_slot']:
            #         time_slotIdList.append(part['time_slot_id'])
            #     start_endList.append([item['section']['start'],item['section']['end']])
            #     classroomList.append(item['section']['classroom']['classroom_id'])
            #     # CourseList.append(item['section']['Course']['cid'])
            # # print(time_slotIdList)
            # # print(start_endList)
            # # print(classroomList)
            # for item in time_slotIdList:
            #     sectionInfoList=sectionInfoList.exclude(time_slot__time_slot_id=item)

            # for item in start_endList:
            #     sectionInfoList=sectionInfoList.filter(Q(start__gte=item[1])|Q(end__lte=item[0]))
            # # 注意未来解决左闭右开问题
            # for item in classroomList:
            #     sectionInfoList=sectionInfoList.exclude(classroom__classroom_id=item)

        print('#####first#####')
        print(queryset)

        if 'Course_name' in queryset:
            sectionInfoList = sectionInfoList.filter(Course__name=queryset['Course_name'])
            queryset.pop('Course_name')
        if 'Teacher_name' in queryset:
            sectionInfoList = sectionInfoList.filter(teach_self__Teacher__name=queryset['Teacher_name'])
            queryset.pop('Teacher_name')
        if 'start_end' in queryset:
            start = queryset['start_end'][0][0:10]
            end = queryset["start_end"][1][0:10]
            sectionInfoList = sectionInfoList.filter(start__gte=start).filter(end__lte=end)
            queryset.pop('start_end')

        if queryset == {}:
            sectionInfoList = sectionInfoList.all().order_by('sec_id')
        else:
            sectionInfoList = sectionInfoList.filter(**queryset).order_by('sec_id')

        if sectionInfoList.exists() == False:
            return Response(ret)

        page = MyLimitOffsetPagination()
        page_roles = page.paginate_queryset(
            queryset=sectionInfoList, request=request, view=self)
        roles_ser = SectionDetailSerializer(instance=page_roles, many=True)
        # 想完善的话应该写一个关于url的解码（因为序列化的问题）
        ret['msg'] = '成功'
        ret['data'] = roles_ser.data
        print(ret['data'])
        ret['lens'] = len(sectionInfoList)

        return Response(ret)


class addSectionView(APIView):
    @transaction.atomic
    def post(self, request):
        print(request.data)
        req = request.data
        # 获得cid
        if(section.objects.all().exists()==False):
            next_num= 100001
        else:
            next_num = int(section.objects.last().sec_id) + 1

        sec_id = '{:0>6d}'.format(next_num)
        start = req["start_end"][0][0:10]
        end = req["start_end"][1][0:10]
        section.objects.create(sec_id=sec_id,
                                capacity=req['capacity'],start=start,
                                end=end,Course_id=req['Course'],classroom_id=req['classroom'])        
        section_object=section.objects.filter(sec_id=sec_id)      
                                # ,time_slot=  
        # list=req['time_slot'].split(",")
        for item in req['time_slot']:
            print(item)
            time_slot_object = time_slot.objects.filter(time_slot_id=item)[0]
            print(time_slot_object)
            section_object[0].time_slot.add(item)
        response = {
            'code': 20000,
            # 'data': {'section': serializer.data[0]}
            # 'success': 'true',
            # 'message': '请求成功'
        }
        return Response(response)

class deleteSectionView(APIView):
    # authentication_classes = [Authentication]   #  添加认证
    # permission_classes = []      # 不尽兴权限控制
    @transaction.atomic
    def delete(self, request, pk):
        ret = {'code': 20000, 'msg': None, 'data': None, 'lens': None}
        sectionDeleting = section.objects.filter(sec_id=pk)
        if sectionDeleting.exists() == False:
            ret['code'] = 10000
            return Response(ret)
        # print(sectionDeleting)
        ret['msg'] = '成功'
        ret['data'] = SectionDetailSerializer(sectionDeleting, many=True).data
        sectionDeleting.delete()
        return Response(ret)

class updateSectionView(APIView):
    @transaction.atomic
    def put(self, request, pk):
        print(request.data)
        req = request.data
        # 获得start,end
        start = req["start_end"][0][0:10]
        end = req["start_end"][1][0:10]
        section_object=section.objects.filter(sec_id=pk)
        section_object.update(capacity=req['capacity'],start=start,
                                end=end,Course_id=req['Course'],classroom_id=req['classroom'])        
        section_object[0].time_slot.clear()
        list=req['time_slot']
        for item in list:
            print(item)
            time_slot_object = time_slot.objects.filter(time_slot_id=item)[0]
            print(time_slot_object)
            section_object[0].time_slot.add(item)
        #将多对多的关系添加到section中
        
        #保存section的多对多关系
        # section.save()
        sectionObject = section.objects.filter(sec_id=pk)
        serializer = SectionDetailSerializer(sectionObject, many=True)
        print(serializer.data)
        response = {
            'code': 20000,
            'data': {'sectionObject': serializer.data[0]},
            'success': 'true',
            'message': '请求成功'
        }
        return Response(response)


class getSectionView(APIView):
    def get(self, request, pk):
        # print(pk)
        # 获得sec_id

        sectionObject = section.objects.filter(sec_id=pk)

        serializer = SectionDetailSerializer(sectionObject, many=True)
        serializer = SectionSerializer(sectionObject, many=True)

        # print(serializer.data)
        response = {
            'code': 20000,
            'data': {'section': serializer.data[0]}
            # 'success': 'true',
            # 'message': '请求成功'
        }
        return Response(response)
class getAllSectionSec_id(APIView):
    def get(self, request):
        sectionObject = section.objects.all()
        print('hhh')
        serializer = SectionSec_idSerializer(sectionObject, many=True)
        print(serializer.data)
        response = {
            'code': 20000,
            'data': {'sectionCid': serializer.data}
        }
        return Response(response)   


class getFrontSectionInfoView(APIView):
    def get(self, request, pk):
        # print(pk)
        # 获得sec_id

        sectionObject = section.objects.filter(sec_id=pk)

        serializer = SectionDetailSerializer(sectionObject, many=True)
        for item in serializer.data:
            item['Course']['photo']=urllib.parse.unquote(item['Course']['photo'])
        # print(serializer.data)
        response = {
            'code': 20000,
            'data': {'section': serializer.data[0]}
            # 'success': 'true',
            # 'message': '请求成功'
        }
        return Response(response)

#########################################################
#########################################################
#########################################################

class Time_slotListView(APIView):
    # authentication_classes = [Authentication]   #  添加认证
    # permission_classes = []      # 不尽兴权限控制

    def get(self, request):
        ret = {'code': 20000, 'msg': None, 'data': None, 'lens': None}
        time_slotList = time_slot.objects.filter(day='周一').order_by('time_slot_id')
        if time_slotList.exists() == False:
            return Response(ret)
        time_slotInfoList = Time_slotSerializer(instance=time_slotList, many=True)
        # for item in time_slotInfoList.data:
        #     item['start']=item['start'][-9:-4]
        #     item['end']=item['end'][-9:-4]

        day = ['周一','周二','周三','周四','周五','周六','周日']
        time_slot_idList = time_slot.objects.all().order_by('time_slot_id')

        time_slot_idList=Time_slotIdSerializer(instance=time_slot_idList, many=True)

        # print(time_slot_idList.data)
        formal_idList = [{},{},{},{},{}]
        for i in range(5):
            for j in range(7):
                formal_idList[i][str(j+1)]=(time_slot_idList.data[i+j*5]['time_slot_id'])
        for i in range(5):
            formal_idList[i]['0'] = time_slotInfoList.data[i]['start'] + '-' + time_slotInfoList.data[i]['end']
        # print(formal_idList)
        ret['msg'] = '成功'
        ret['data'] = {
            'time_slot':time_slotInfoList.data,
            'day':day,
            'time_slot_id':formal_idList
        }
        # print(ret)
        return Response(ret)
@transaction.atomic
def time_slotInit():
    day=['周一','周二','周三','周四','周五','周六','周日']
 
    start=[ '2000-01-01 08:00',
            '2000-01-01 10:15',
            '2000-01-01 14:00',
            '2000-01-01 16:15',
            '2000-01-01 19:00',
            ]
    end=[   '2000-01-01 09:45',
            '2000-01-01 12:00',
            '2000-01-01 15:45',
            '2000-01-01 18:00',
            '2000-01-01 20:45',
        ]
    for i in range(7):
        for j in range(5):
            time_slot.objects.create(time_slot_id=str(i+1)+'-'+str(j+1),
                                    day=day[i],start=start[j],end=end[j])

class updateTime_slotView(APIView):
    @transaction.atomic
    def put(self, request):
        print(request.data)
        req = request.data
        # 获得time_slot_id
        time_slotObject=time_slot.objects.all().order_by('time_slot_id')
        if(time_slotObject.exists()==False):
            time_slotInit()
        for i in range(7):
            for j in range(5):
                print(req[j])
                print(req[j]['start'])
                print(req[j]['end'])
                time_slotObject=time_slotObject=time_slot.objects.filter(time_slot_id=str(i+1)+'-'+str(j+1))
                time_slotObject.update(start='2000-01-01 '+req[j]['start'],end='2000-01-01 '+req[j]['end'])

        serializer = Time_slotSerializer(time_slotObject, many=True)
        print(serializer.data)
        response = {
            'code': 20000,

        }

        return Response(response)

class getAllTime_slotView(APIView):
    def get(self, request):
        time_slotObject = time_slot.objects.filter(day='周一').order_by('time_slot_id')
        # 2020-01-01 00:00:00
        serializer = Time_slotSerializer(time_slotObject, many=True)
        # for item in serializer.data:
        #     item['start']=item['start'][-9:-4]
        #     item['end']=item['end'][-9:-4]

        print(serializer.data)
        response = {
            'code': 20000,
            'data': {'time_slot': serializer.data}
        }
        return Response(response)
class getAllTime_slotSelectView(APIView):
    def get(self, request):
        time_slotObject = time_slot.objects.all().order_by('time_slot_id')
        # 2020-01-01 00:00:00
        serializer = Time_slotIdSerializer(time_slotObject, many=True)

        print(serializer.data)
        response = {
            'code': 20000,
            'data': {'time_slot': serializer.data}
        }
        return Response(response)

#########################################################
#########################################################
#########################################################

class ClassroomListView(APIView):
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
            classroomInfoList = classroom.objects.order_by('classroom_id')
        else:
            classroomInfoList = classroom.objects.filter(**queryset).order_by('classroom_id')

        if classroomInfoList.exists() == False:
            return Response(ret)
        # print(classroomInfoList)

        page = MyLimitOffsetPagination()
        # print(page)
        page_roles = page.paginate_queryset(
            queryset=classroomInfoList, request=request, view=self)
        # print(page_roles)
        roles_ser = ClassroomDetailSerializer(instance=page_roles, many=True)


        ret['msg'] = '成功'
        ret['data'] = roles_ser.data
        print(ret['data'])
        ret['lens'] = len(classroomInfoList)

        return Response(ret)

class addClassroomView(APIView):
    @transaction.atomic
    def post(self, request):
        print(request.data)
        req = request.data
                #数据过滤
        toPop=[]
        for key in req:
            if req[key]=='':
                toPop.append(key)
        for key in toPop:
            req.pop(key)

        if(classroom.objects.all().exists()==False):
            next_num= 1001
        else:
            next_num = int(classroom.objects.last().classroom_id) + 1

        req['classroom_id'] = '{:0>4d}'.format(next_num)
        classroom_id = '{:0>4d}'.format(next_num)

        classroom.objects.create(**req)  
        response = {
            'code': 20000,
            'success': 'true',
            'message': '请求成功'
        }

        return Response(response)

class deleteClassroomView(APIView):
    @transaction.atomic
    # authentication_classes = [Authentication]   #  添加认证
    # permission_classes = []      # 不尽兴权限控制

    def delete(self, request, pk):
        ret = {'code': 20000, 'msg': None, 'data': None, 'lens': None}
        classroomDeleting = classroom.objects.filter(classroom_id=pk)
        if classroomDeleting.exists() == False:
            ret['code'] = 10000
            return Response(ret)
        # print(classroomDeleting)
        ret['msg'] = '成功'
        ret['data'] = ClassroomDetailSerializer(classroomDeleting, many=True).data
        classroomDeleting.delete()
        return Response(ret)

class updateClassroomView(APIView):
    @transaction.atomic
    def put(self, request, pk):
        req = request.data
        # 获得classroom_id
        #数据过滤
        toPop=[]
        for key in req:
            if req[key]=='':
                toPop.append(key)
        for key in toPop:
            req.pop(key)
        classroom.objects.filter(classroom_id=pk).update(**req)
        classroomObject = classroom.objects.filter(classroom_id=pk)
        serializer = ClassroomDetailSerializer(classroomObject, many=True)
        print(serializer.data)
        response = {
            'code': 20000,
            'success': 'true',
            'message': '请求成功'
        }
        return Response(response)


class getClassroomView(APIView):
    def get(self, request, pk):
        classroomObject = classroom.objects.filter(classroom_id=pk)

        serializer = ClassroomDetailSerializer(classroomObject, many=True)
        # print(serializer.data)
        response = {
            'code': 20000,
            'data': {'classroom': serializer.data[0]},
            'success': 'true',
            'message': '请求成功'
        }
        return Response(response)

class getAllClassroom(APIView):
    def get(self, request):
        classroomObject = classroom.objects.all()

        serializer = ClassroomDetailSerializer(classroomObject, many=True)
        # print(serializer.data)
        response = {
            'code': 20000,
            'data': {'classroom': serializer.data},
            'success': 'true',
            'message': '请求成功'
        }
        return Response(response)

class TakeListView(APIView):
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
            takeInfoList = take.objects.order_by('id')
        else:
            takeInfoList = take.objects.filter(**queryset).order_by('id')

        if takeInfoList.exists() == False:
            return Response(ret)
        
        # 获取分页并做序列化
        page = MyLimitOffsetPagination()
        page_roles = page.paginate_queryset(
            queryset=takeInfoList, request=request, view=self)
        roles_ser = TakeDetailSerializer(instance=page_roles, many=True)


        ret['msg'] = '成功'
        ret['data'] = roles_ser.data
        ret['lens'] = len(takeInfoList)

        return Response(ret)

class addTakeView(APIView):
    @transaction.atomic
    def post(self, request):
        print(request.data)
        req = request.data
        # 获得id

        #前端规定一定要交填满的表
        
        #外键无法在创建的时候以id的形式添加，可以在update中按主键添加或在create中以外键_id的形式添加

        take.objects.create(Student_id=req['Student'],section_id=req['section'],status=req['status'])
        sectionObject=section.objects.filter(sec_id=req['section'])
        info=SectionSerializer(sectionObject,many=True).data[0]
        print(info)
        sectionObject.update(choosed=info['choosed']+1)
        courseObject=Course.objects.filter(cid=info['Course'])
        info=CourseSerializer(courseObject,many=True).data[0]

        courseObject.update(choosed_sum=info['choosed_sum']+1)
        response = {
            'code': 20000,
            'success': 'true',
            'message': '请求成功'
        }
        return Response(response)

class deleteTakeView(APIView):
    @transaction.atomic
    # authentication_classes = [Authentication]   #  添加认证
    # permission_classes = []      # 不尽兴权限控制

    def delete(self, request, pk):
        ret = {'code': 20000, 'msg': None, 'data': None, 'lens': None}
        takeDeleting =take.objects.filter(id=pk)
        sectionObject=section.objects.filter(take_self__id=pk)
        info=SectionSerializer(sectionObject,many=True).data[0]
        print(info)
        sectionObject.update(choosed=info['choosed']-1)
        if takeDeleting.exists() == False:
            ret['code'] = 10000
            return Response(ret)
        # print(takeDeleting)
        ret['msg'] = '成功'
        ret['data'] = TakeDetailSerializer(takeDeleting, many=True).data

        takeDeleting.delete()
        return Response(ret)

class updateTakeView(APIView):
    @transaction.atomic
    def put(self, request, pk):
        print(request.data)
        req = request.data 

        take.objects.filter(id=pk).update(**req)

        takeObject = take.objects.filter(id=pk)
        serializer = TakeSerializer(takeObject, many=True)
        
        response = {
            'code': 20000,
            'data': {'take': serializer.data[0]},
            'success': 'true',
            'message': '请求成功'
        }
        return Response(response)


class getTakeView(APIView):

    def get(self, request, pk):
        # 获得id

        takeObject = take.objects.filter(id=pk)

        serializer = TakeSerializer(takeObject, many=True)

        response = {
            'code': 20000,
            'data': {'take': serializer.data[0]},
            'success': 'true',
            'message': '请求成功'
        }
        return Response(response)

# class getAllTake(APIView):
#     def get(self, request):
#         take = Take.objects.all()
#         serializer = TakeSerializer(take, many=True)
#         for item in serializer.data:
#             print(item)
#             item['photo']=urllib.parse.unquote(item['photo'])
#             print(item)

#         response = {
#             'code': 20000,
#             'data': {'allTake': serializer.data},
#             'success': 'true',
#             'message': '请求成功'
#         }
#         return Response(response)   


class TeachListView(APIView):
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
            teachInfoList = teach.objects.order_by('id')
        else:
            teachInfoList = teach.objects.filter(**queryset).order_by('id')

        if teachInfoList.exists() == False:
            return Response(ret)
        
        # 获取分页并做序列化
        page = MyLimitOffsetPagination()
        page_roles = page.paginate_queryset(
            queryset=teachInfoList, request=request, view=self)
        roles_ser = TeachDetailSerializer(instance=page_roles, many=True)


        ret['msg'] = '成功'
        ret['data'] = roles_ser.data
        ret['lens'] = len(teachInfoList)

        return Response(ret)

class addTeachView(APIView):
    @transaction.atomic
    def post(self, request):
        print(request.data)
        req = request.data
        # 获得id

        #数据过滤
        toPop=[]
        for key in req:
            if req[key]=='':
                toPop.append(key)
        for key in toPop:
            req.pop(key)
        
        #外键无法在创建的时候以id的形式添加，可以在update中按主键添加或在create中以外键_id的形式添加

        teach.objects.create(Teacher_id=req['Teacher'],section_id=req['section'],status=req['status'])
    

        response = {
            'code': 20000,
            'success': 'true',
            'message': '请求成功'
        }
        return Response(response)

class deleteTeachView(APIView):
    # authentication_classes = [Authentication]   #  添加认证
    # permission_classes = []      # 不尽兴权限控制
    @transaction.atomic
    def delete(self, request, pk):
        ret = {'code': 20000, 'msg': None, 'data': None, 'lens': None}
        teachDeleting =teach.objects.filter(id=pk)
        if teachDeleting.exists() == False:
            ret['code'] = 10000
            return Response(ret)
        # print(teachDeleting)
        ret['msg'] = '成功'
        ret['data'] = TeachDetailSerializer(teachDeleting, many=True).data

        teachDeleting.delete()
        return Response(ret)

class updateTeachView(APIView):
    @transaction.atomic
    def put(self, request, pk):
        print(request.data)
        req = request.data 

        teach.objects.filter(id=pk).update(**req)

        teachObject = teach.objects.filter(id=pk)
        serializer = TeachDetailSerializer(teachObject, many=True)
        
        response = {
            'code': 20000,
            'data': {'teach': serializer.data[0]},
            'success': 'true',
            'message': '请求成功'
        }
        return Response(response)

class getTeachView(APIView):
    def get(self, request, pk):
        # 获得id
        teachObject = teach.objects.filter(id=pk)

        serializer = TeachSerializer(teachObject, many=True)

        response = {
            'code': 20000,
            'data': {'teach': serializer.data[0]},
            'success': 'true',
            'message': '请求成功'
        }
        return Response(response)
