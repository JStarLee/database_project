"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.db import router, utils
from django.urls import path,include
from rest_framework import routers
from users.views import myUserViewSet
import tools,index
from backend.settings import STATIC_URL

from django.views.static import serve
import backend.settings
router=routers.DefaultRouter()
router.register('users/myuser',myUserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include(router.urls)),
    path('upload/<path>',serve,{'document_root':backend.settings.UPLOAD_FILE}),

    path('users/',include("users.urls")),
    path('edu/teacher/',include("teacher.urls")),
    path('edu/student/',include("student.urls")),
    path('edu/course/',include("course.urls")),
    path('edu/section/',include("course.urls")),
    path('edu/time_slot/',include("course.urls")),
    path('edu/classroom/',include("course.urls")),
    path('edu/take/',include("course.urls")),
    path('edu/teach/',include("course.urls")),


    path('publish/evaluation/',include("evaluation.urls")),
    path('edu/photo',tools.addPhotoView.as_view()),



    #######################前端#######################
    # path('edu/bannerFront/',include("banner.urls")),
    path('edu/teacherFront/',include("teacher.urls")),
    path('edu/courseFront/',include("course.urls")),
    path('edu/sectionFront/',include("course.urls")),


    # path('edu/bannerFront/',include("course.urls")),
    path('edu/indexFront/index',index.getIndexDataView.as_view()),

]
