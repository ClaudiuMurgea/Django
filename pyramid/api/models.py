from django.db import models
from django.contrib.auth.models import User


class Permission(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    role = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="notes")

    def __str__(self):
        return self.title


class User_details(models.Model):
    phone = models.CharField()
    email = models.CharField(max_length=250, null=True, blank=True)
    digits = models.IntegerField(null=True, blank=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owner")
