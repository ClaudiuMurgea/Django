from rest_framework import serializers
from .models import Permission
from api.models import CustomUser
# from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # checks on both ways, coming and going
        fields = ["id", "username", "password"]
        # we want to accept passwrd when we are accepting but we don't want to return a password
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class PermisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "title", "content", "created_at", "author"]
        extra_kwargs = {"author": {"read_only": True}}
