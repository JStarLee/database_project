from django.db import models
from django.db.models import fields
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import StudentUsers,Student

class StudentUsersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = StudentUsers
        fields = "__all__"

class StudentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = "__all__"