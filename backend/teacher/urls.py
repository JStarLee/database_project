from django.conf.urls import url
from django.urls import path, include
from rest_framework import views
# from .views import myUserInfo
from .views import TeacherListView, deleteTeacherView, getTeacherView, updateTeacherView, addTeacherView,getAllTeacher,getTeacherFrontInfoView


urlpatterns = [
    path('pageTeacherCondition/', TeacherListView.as_view()),
    url(r'^deleteTeacher/(?P<pk>t[0-9]+)$', deleteTeacherView.as_view()),
    url(r'^getTeacher/(?P<pk>t[0-9]+)$', getTeacherView.as_view()),
    url(r'^updateTeacher/(?P<pk>t[0-9]+)$',updateTeacherView.as_view()),
    path('addTeacher/', addTeacherView.as_view()),
    path('getAllTeacher/', getAllTeacher.as_view()),


    path('getTeacherInfoList/', TeacherListView.as_view()),
    # url(r'^getTeacherFrontInfo/(?P<pk>t[0-9]+)$', getTeacherView.as_view()),
    url(r'^getTeacherFrontInfo/(?P<pk>t[0-9]+)$', getTeacherFrontInfoView.as_view()),



]
