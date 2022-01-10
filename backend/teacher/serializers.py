from django.db import models
from django.db.models import fields
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import TeacherUsers,Teacher

class TeacherUsersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TeacherUsers
        fields = "__all__"

class TeacherDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = "__all__"