from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from api.models import User_details  # Replace with your actual models
from reports.models import User_logs


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def update_details(sender, instance, created, **kwargs):
    if created:  # Runs only when a new user is registered
        # Replace with actual column updates
        User_details.objects.create(
            phone='', user=instance, digits='0', email='clau@g.com')


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    User_logs.objects.create(title='User logged in ')
