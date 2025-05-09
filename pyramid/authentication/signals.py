from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import Settings
from django.db import connection
from django.contrib.auth.hashers import make_password
from .models import CustomUser
from datetime import datetime

@receiver(post_migrate)
def create_default_groups_and_settings(sender, **kwargs):
    if sender.name == "authentication":
        default_config = {
            "Cashier": {
                "minimum_characters": 6,
                "contain_upper_case": False,
                "contain_lower_case": True,
                "contain_special_case": True,
                "contain_number": True,
            },
            "Attendant": {
                "minimum_characters": 8,
                "contain_upper_case": True,
                "contain_lower_case": True,
                "contain_special_case": True,
                "contain_number": True,
            },
            "Manager": {
                "minimum_characters": 10,
                "contain_upper_case": True,
                "contain_lower_case": True,
                "contain_special_case": True,
                "contain_number": True,
            },
        }
        if "authentication_settings" in connection.introspection.table_names():
            for role_name, settings_values in default_config.items():
                group, created = Group.objects.get_or_create(name=role_name)
                Settings.objects.get_or_create(group=group, defaults=settings_values)
        
        # serializer = UserSerializer(data=request.data)
        # if serializer.is_valid():
        #     serializer.save()

        if not CustomUser.objects.filter(username="eurogames").exists():
            superuser = CustomUser(
                username="eurogames",
                email="email@egt.com",
                phone="+40771694307",
                is_superuser=True,
                is_staff=True,
                password_changed_at=datetime.now(),
                password=make_password("pyramid")  # Manually hash password
            )
            superuser.save()
            manager_group, _ = Group.objects.get_or_create(name="Manager") # in this line _ means i dont need the second value, which is a bool, "created" could have been there and be used further in the code, as needed
            superuser.groups.add(manager_group)



































# from django.contrib.auth.signals import user_login_failed
# from django.contrib.auth.signals import user_logged_in
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.conf import settings
# from reports.models import User_logs
# from django.utils.timezone import now
# from django.contrib.auth.models import User
# from django.http import JsonResponse

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def update_details(sender, instance, created, **kwargs):
#     if created:  # Runs only when a new user is registered
#         # Replace with actual column updates
#         User_details.objects.create(
#             phone='', user=instance, digits='0', email='clau@g.com')


# @receiver(user_logged_in)
# def log_user_login(sender, request, user, **kwargs):
#     ip_address = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', 'Unknown'))
    
#     User_logs.objects.create(
#         user_id=user.id,
#         username=user.username,
#         ip_address=ip_address,
#         action='SUCCESSFUL_LOGIN',
#         timestamp=now()
#     )

# @receiver(user_login_failed)
# def log_failed_login(sender, credentials, request, **kwargs): 
#     username = credentials.get('username', 'Unknown')
#     ip_address = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', 'Unknown'))

#     #check if the given username is correct, if it is, we populate the user_id, otherwise the user_id will stay NULL
#     user = User.objects.filter(username=username).first()
#     user_id = user.id if user else None  # Get user_id or None if not found

#     # Create a log entry
#     User_logs.objects.create( 
#         username=username,
#         user_id=user_id,
#         ip_address=ip_address,  
#         action="FAILED_LOGIN", 
#         timestamp=now()
#     ) 
#     if user_id != None:
#         user_details = User_details.objects.get(user_id=user_id)
#         if user_details.failed_attempt < 5:
#             user_details.failed_attempt += 1
#         elif user_details.failed_attempt >= 5:
#             user_details.locked = "yes"
#         user_details.save()