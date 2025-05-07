from django.db import models
from authentication.models import CustomUser

# Create your models here.
class Permission(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="permissions")

    def __str__(self):
        return self.title