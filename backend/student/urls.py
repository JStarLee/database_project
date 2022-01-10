from django.conf.urls import url
from django.urls import path, include
from rest_framework import views
# from .views import myUserInfo
from .views import StudentListView, deleteStudentView, getStudentView, updateStudentView, addStudentView, getAllStudent


urlpatterns = [
    path('pageStudentCondition/', StudentListView.as_view()),
    url(r'^deleteStudent/(?P<pk>s[0-9]+)$', deleteStudentView.as_view()),
    url(r'^getStudent/(?P<pk>s[0-9]+)$', getStudentView.as_view()),
    url(r'^updateStudent/(?P<pk>s[0-9]+)$',updateStudentView.as_view()),
    path('addStudent/', addStudentView.as_view()),
    path('getAllStudent/', getAllStudent.as_view()),

]
