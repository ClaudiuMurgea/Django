from rest_framework import serializers
from .models import Permission

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "title", "content", "created_at", "user"]
        extra_kwargs = {"user": {"read_only": True}}