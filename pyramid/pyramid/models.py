from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    digits = models.IntegerField()
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username
