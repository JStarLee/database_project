from django.http import response
from django.urls import path,include
from rest_framework import views
from rest_framework_jwt.views import obtain_jwt_token
# from .views import myUserInfo
from .views import info, logout, register


urlpatterns = [
    path('login/',obtain_jwt_token),
    path('register/',register),
    path('logout/',logout),
    path('info/',info),
    # path('update/',put),
]
