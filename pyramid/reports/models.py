from django.db import models
from authentication.models import CustomUser

# Create your models here.

class User_login_activity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="user_activity", null=True) # User ID reference
    username = models.CharField(max_length=100, null=True)
    success = models.BooleanField(default=True)
    ip_address = models.GenericIPAddressField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

class Settings_history(models.Model):
    minimum_characters = models.IntegerField(null=True, blank=True)
    contain_upper_case = models.BooleanField(default=False)
    contain_lower_case = models.BooleanField(default=False)
    contain_special_case = models.BooleanField(default=False)
    contain_number = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="settings_history")
