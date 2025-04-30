from django.db import models
# from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Add your custom fields here
    phone = models.CharField(null=True)
    email = models.CharField(max_length=250, null=True, blank=True)
    digits = models.IntegerField(null=True, blank=True)
    failed_attempts = models.IntegerField(null=True, default=0)
    code_generation_time = models.DateTimeField(null=True)
    class LockedStatus(models.TextChoices):
        YES = "yes", "Yes"
        NO = "no", "No"

    locked = models.CharField(
        max_length=3,
        choices=LockedStatus.choices,
        default=LockedStatus.NO
    )

    def __str__(self):
        return self.username
    
class Permission(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="notes")

    def __str__(self):
        return self.title