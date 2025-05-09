from rest_framework import serializers
from .models import Settings
from authentication.models import CustomUser
from django.contrib.auth.models import Group
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from datetime import timedelta
from django.utils.timezone import now
from pyramid.custom_settings import PASSWORD_MEASURE, PASSWORD_EXPIRATION_TIME
from rest_framework.permissions import BasePermission

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # checks on both ways, coming and going
        fields = [
            'id', 'username', 'password', 'first_name', 'last_name',
            'phone', 'email', 'is_staff', 'is_superuser','is_active'
            ]
        # we want to accept passwrd when we are accepting but we don't want to return a password
        extra_kwargs = {
            "password": {"write_only": True},
            'is_staff': {'default': False},
            'is_superuser': {'default': False}
            }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # You can add custom claims to the token here (optional)
        token['username'] = user.username
        return token

    def validate(self, attrs):
        try:
            # ✅ SUCCESS: If credentials are valid, this returns the tokens and adds extra data
            data = super().validate(attrs)
            user = self.user
            password_changed_at = user.password_changed_at
            current_time = now()
            password_age = abs(current_time - password_changed_at)
            
            if password_age > timedelta(**{PASSWORD_MEASURE: PASSWORD_EXPIRATION_TIME}):
                raise serializers.ValidationError({"detail":"expired"})
            
            return data
        except Exception as e:
            # ❌ FAILURE: If credentials are invalid, this raises an error caught in the view
            raise e  # Let the view handle the failure response   

# This permission allows access to Super Admin or Manager
class IsManagerGroupOrSuperuser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            user and
            user.is_authenticated and
            (user.is_superuser or user.groups.filter(name="Manager").exists())
        )
    
# This permission allows access Manager
class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name="Manager").exists()

# This permission allows access Attendent
class IsAttendent(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name="Attendent").exists()

# This permission allows access Cashier
class IsCashier(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.groups.filter(name="Cashier").exists()

class SettingsPermission(BasePermission):
    """
    Custom permission for Settings model:
    - Manager: full access
    - Attendent: create only
    - Cashier: read only
    """
    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        if user.groups.filter(name="Manager").exists():
            return True  # all permissions

        if user.groups.filter(name="Attendent").exists():
            if request.method in ['GET', 'POST']:
                return True

        if user.groups.filter(name="Cashier").exists():
            if request.method in ['GET']: 
                return True
        return False

# recieves a username and a group, to asign a group to the user           
    
class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settings
        # fields = ["id", "minimum_characters", "contain_upper_case", "contain_lower_case", "contain_special_case", "contain_number", "created_at", "user"]
        fields = '__all__'
        extra_kwargs = {"user": {"read_only": True}}

class GroupSettingsSerializer(serializers.ModelSerializer):
    settings = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ["name", "settings"]

    def get_settings(self, obj):
        settings = getattr(obj, "settings", None)  # Retrieve OneToOneField
        return SettingsSerializer(settings).data if settings else None