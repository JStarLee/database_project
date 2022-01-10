from django.db import models
from django.db.models import fields
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import myUser


# User = get_user_model()
class myUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = myUser
        fields = "__all__"
        # fields = ["username","password"]


class myUserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列表类
    """
    class Meta:
        model = myUser
        fields = ["username", "roles", "avatar", "uid"]

        # fields = "__all__"

