from django.db import models
# from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
# from django.contrib.auth.models import Group, Permission
# from django.contrib.contenttypes.models import ContentType

class CustomUser(AbstractUser):
    # Add your custom fields here
    phone = models.CharField(max_length=150, null=True)
    email = models.CharField(max_length=150, null=True, blank=True)
    pin = models.IntegerField(null=True, blank=True)
    failed_attempts = models.IntegerField(null=True, default=0)
    code_generation_time = models.DateTimeField(null=True)

    def __str__(self):
        return self.username
    
class Setting(models.Model):
    minimum_characters = models.IntegerField(null=True, blank=True)
    contain_upper_case = models.BooleanField(default=False)
    contain_lower_case = models.BooleanField(default=False)
    contain_special_case = models.BooleanField(default=False)
    contain_number = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="settings")

    def __str__(self):
        return self.title

# def create_roles():
#     admin_group, _ = Group.objects.get_or_create(name="Admin")
#     user_group, _ = Group.objects.get_or_create(name="User")

#     # Assign permissions to Admin
#     content_type = ContentType.objects.get_for_model(CustomUser)
#     permissions = Permission.objects.filter(content_type=content_type)
#     admin_group.permissions.set(permissions)  # Admin gets all permissions