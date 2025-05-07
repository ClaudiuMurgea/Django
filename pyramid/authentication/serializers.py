from rest_framework import serializers
from .models import Setting
from authentication.models import CustomUser
# from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # checks on both ways, coming and going
        fields = ["id", "username", "password", "first_name", "last_name", "email", "phone", "is_staff", "is_superuser"]
        # we want to accept passwrd when we are accepting but we don't want to return a password
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    

class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields = ["id", "minimum_characters", "contain_upper_case", "contain_lower_case", "contain_special_case", "contain_number", "created_at", "user"]
        extra_kwargs = {"user": {"read_only": True}}