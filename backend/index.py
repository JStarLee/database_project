from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.response import Response
import urllib.parse

from teacher.serializers import TeacherDetailSerializer
from teacher.models import Teacher

from course.serializers import CourseDetailSerializer
from course.models import Course
class getIndexDataView(APIView):
    def get(self,request):
        # print(request)
        teacherList = Teacher.objects.order_by('tid')
        teacherList = TeacherDetailSerializer(teacherList,many=True)
        courseList = Course.objects.order_by('-choosed_sum')
        courseList = CourseDetailSerializer(courseList,many=True)

        for item in teacherList.data:
            # print(item)
            item['photo']=urllib.parse.unquote(item['photo'])
            # print(item)
            
        for item in courseList.data:
            print(item)
            item['photo']=urllib.parse.unquote(item['photo'])
            # print(item)
        response = {
            'code': 20000,
            'data':{
                'teacherList':teacherList.data[0:8],
                'courseList':courseList.data[0:8]
            }
        }
        return Response(response)