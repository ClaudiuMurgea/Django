from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
import json
# from django.contrib.auth.models import BaseUserManager

class CustomUser(AbstractUser):
    # Add your custom fields here
    ROLE_CHOICES = (
        ('cashier', 'Cashier'),
        ('attendant', 'Attendant'),
        ('manager', 'Manager'),
    )
    phone = models.CharField(max_length=150, null=True)
    email = models.CharField(max_length=150, null=True, blank=True)
    pin = models.IntegerField(null=True, blank=True)
    failed_attempts = models.IntegerField(null=True, default=0)
    code_generation_time = models.DateTimeField(null=True)
    password_changed_at = models.DateTimeField(null=True)

class Settings(models.Model):
    minimum_characters = models.IntegerField(null=True, blank=True)
    contain_upper_case = models.BooleanField(default=False)
    contain_lower_case = models.BooleanField(default=False)
    contain_special_case = models.BooleanField(default=False)
    contain_number = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    group = models.OneToOneField(  # each group can have only one settings row
        Group, on_delete=models.CASCADE, related_name="settings"
    )

    def __str__(self):
        fields = {
            field.name: getattr(self, field.name) for field in self._meta.fields if field.name not in ["id", "group"]
        }
        
        # Convert datetime field to ISO format for better readability
        fields["created_at"] = fields["created_at"].isoformat() if fields["created_at"] else None
        
        # Convert group to its string representation (just its name)
        fields["group"] = self.group.name if self.group else None

        formatted_fields = ", ".join(f'"{key}": {repr(value)}' for key, value in fields.items())
        return f"{{ {formatted_fields} }}"