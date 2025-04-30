from rest_framework import serializers
from .models import CustomUser

# When registering a user, the register serializer create user function was created to modify the regular return of the jwt package into {}
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["username", "password"]  # Specify necessary fields only

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return {} #Return an empty JSON response