from django.db import models
from authentication.models import CustomUser

# Create your models here.

class User_login_activity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True) # User ID reference
    username = models.CharField(max_length=100, null=True)
    action = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
