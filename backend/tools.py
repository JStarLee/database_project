from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.views import APIView
import os
import datetime,backend.settings

from backend.settings import BASE_DIR
# class updateTeacherView(APIView):
#     def put(self, request, pk):
#         print(request.data)
#         req = request.data
#         # 获得tid
#         Teacher.objects.filter(tid=pk).update(
#             name=req['name'], be_good_at=req["be_good_at"], intro=req["intro"])
#         teacher = Teacher.objects.filter(tid=pk)
#         serializer = TeacherDetailSerializer(teacher, many=True)
#         print(serializer.data)
#         response = {
#             'code': 20000,
#             # 'data': {'teacher': serializer.data[0]}
#             # 'success': 'true',
#             # 'message': '请求成功'
#         }
#         return Response(response)

class addPhotoView(APIView):
    def post(self,request):
        # print(request)
        # req = request.data
        image = request.FILES.get('file')
        image_name = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')+image.name     

        f = open(os.path.join(backend.settings.UPLOAD_FILE,image_name), 'wb')

        for chunk in image.chunks():
            f.write(chunk)
        f.close()
        response = {
            'code': 20000,
            'data':{
                'url': 'http://127.0.0.1:8000/upload/'+image_name
            }
        }
        return Response(response)