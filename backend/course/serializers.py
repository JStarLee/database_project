from django.db import models
from django.db.models import fields
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Course, classroom,section, time_slot,teach,take
import urllib.parse

class CourseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"
        depth = 1

class Time_slotDetailSerializer(serializers.ModelSerializer):
    start = serializers.DateTimeField(read_only=True,format='%H:%M')
    end = serializers.DateTimeField(read_only=True,format='%H:%M')

    class Meta:
        model = time_slot
        fields = '__all__'
class Time_slotSerializer(serializers.ModelSerializer):
    start = serializers.DateTimeField(read_only=True,format='%H:%M')
    end = serializers.DateTimeField(read_only=True,format='%H:%M')

    class Meta:
        model = time_slot
        fields = ('start','end')
class Time_slotIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = time_slot
        fields = ('time_slot_id',)  #要加,
class ClassroomDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = classroom
        fields = "__all__"
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"         #不要使用[]，要使用（）

class SectionDetailSerializer(serializers.ModelSerializer):
    time_slot = Time_slotDetailSerializer(many=True)
    class Meta:
        model = section
        fields = "__all__"
        depth = 1

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = section
        fields = "__all__"
        
class SectionSec_idSerializer(serializers.ModelSerializer):
    class Meta:
        model = section
        fields = ('sec_id',)         #不要使用[]，要使用（）


class TakeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = take
        fields = "__all__"
        depth = 2


class TeachDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = teach
        fields = "__all__"
        depth = 2

class TakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = take
        fields = "__all__"


class TeachSerializer(serializers.ModelSerializer):
    class Meta:
        model = teach
        fields = "__all__"
