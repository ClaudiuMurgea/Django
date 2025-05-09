from rest_framework_simplejwt.views import TokenObtainPairView
from authentication.serializers import CustomTokenObtainPairSerializer
from django.contrib.auth import login
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from reports.models import User_login_activity
from django.utils.timezone import now
from authentication.models import CustomUser
from django.core.mail import send_mail
from datetime import datetime
from rest_framework.exceptions import ValidationError
from pyramid.custom_settings import USER_MAXIMUM_FAILED_ATTEMPTS

User = get_user_model()

# The Login jwt package serializer was modified to raise exception on failed login attempt that can be customized here

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer #not the default TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            # ✅ SUCCESS: If serializer.validate() runs without error
            response = super().post(request, *args, **kwargs)
            username = request.data.get("username")
 
            # Log in the authenticated user
            user = CustomUser.objects.get(username=username)
            if user:
                login(request, user)

            ip_address = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', 'Unknown'))
            
            User_login_activity.objects.create(
                user_id=user.id,
                username=user.username,
                ip_address=ip_address,
                timestamp=now()
            )

            if user.failed_attempts >= USER_MAXIMUM_FAILED_ATTEMPTS and user.is_active == 0:
                # Account locked due to multiple failed login attempts
                return Response(status=status.HTTP_423_LOCKED)
            else:
                user.failed_attempts = 0
                user.save()

            # Get user's groups
            groups = user.groups.all().values_list("name", flat=True)  # Returns a list of group names

            # Asign Super Admin if the user is superuser or the Group that it belongs to as a Role
            response.data['role'] = "Super Admin" if user.is_superuser else user.groups.first().name if user.groups.exists() else None
            return Response(response.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            detail = e.detail.get("detail")
            username = request.data.get("username")
            ip_address = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', 'Unknown'))
            currentDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            user = User.objects.filter(username=username).first()
            user_id = user.id if user else None  # Get user_id or None if not found

            # Create a log entry
            User_login_activity.objects.create( 
                username=username,
                user_id=user_id,
                ip_address=ip_address,  
                success=0, 
                timestamp=now()
            ) 
            if detail[0] == "expired":
                return Response({"code": 4}, status=status.HTTP_403_FORBIDDEN)
            
        except Exception as e:
            # ❌ FAILURE: If serializer raises an error (e.g. wrong username/password)
            username = request.data.get("username")
            ip_address = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', 'Unknown'))
            currentDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            user = User.objects.filter(username=username).first()
            user_id = user.id if user else None  # Get user_id or None if not found

            # Create a log entry
            User_login_activity.objects.create( 
                username=username,
                user_id=user_id,
                ip_address=ip_address,  
                success=0, 
                timestamp=now()
            ) 
            if user_id != None:
                if user.failed_attempts < USER_MAXIMUM_FAILED_ATTEMPTS:
                    user.failed_attempts += 1
                    user.save()
                    return Response({"incorrect credentials"})
                elif user.failed_attempts >= USER_MAXIMUM_FAILED_ATTEMPTS and user.is_active == 1:
                    user.is_active = 0
                    send_mail(subject='That`s your subject',
                        message='Hello ' + username +
                        '! \n Your account has been locked for security reasons' +
                        '  \n The last failed attempt occured on : ' + currentDate +
                        '  \n From a device using the IP: ' + ip_address,
                        from_email='egt.pyramid.com',
                        recipient_list=['useremail@gmail.com'])
                    user.save()
                    return Response({"code": 3}, status=status.HTTP_403_FORBIDDEN)
            # return Response(status=status.HTTP_423_LOCKED)

        return Response({}, status=status.HTTP_401_UNAUTHORIZED)

