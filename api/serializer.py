from rest_framework import serializers

from  django.contrib.auth.models import User

from myapp.models import UserProfile,Video

class UserSerialization(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username","email","password"]

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserProfile
        fields="__all__"

        read_only_fields=["user"]

class VideoSerializer(serializers.ModelSerializer):
     class Meta:
         model=Video
         fields="__all__"