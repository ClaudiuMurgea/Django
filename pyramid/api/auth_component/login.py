from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import login
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from reports.models import User_login_activity
from django.utils.timezone import now
from api.models import CustomUser
from django.core.mail import send_mail
from datetime import datetime

User = get_user_model()

# The Login jwt package serializer was modified to raise exception on failed login attempt that can be customized here
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # You can add custom claims to the token here (optional)
        token['username'] = user.username
        return token

    def validate(self, attrs):
        try:
            # ✅ SUCCESS: If credentials are valid, this returns the tokens and adds extra data
            data = super().validate(attrs)
            # data.update({
            #     'message': 'Login successful',
            #     'username': self.user.username
            # })
            return data
        except Exception as e:
            # ❌ FAILURE: If credentials are invalid, this raises an error caught in the view
            raise e  # Let the view handle the failure response


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
                action='SUCCESSFUL_LOGIN',
                timestamp=now()
            )

            if user.failed_attempts >= 5:
                # Account locked due to multiple failed login attempts
                return Response({"code": 3}, status=status.HTTP_403_FORBIDDEN)
            else:
                CustomUser.objects.filter(id=user.id).update(failed_attempts=0, locked="no")

            return Response(response.data, status=status.HTTP_200_OK)
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
                action="FAILED_LOGIN", 
                timestamp=now()
            ) 

            if user_id != None:
                if user.failed_attempts < 5:
                    user.failed_attempts += 1
                    user.save()
                    return Response({}, status=status.HTTP_401_UNAUTHORIZED)
                elif user.failed_attempts >= 5 and user.locked == "no":
                    user.locked = "yes"
                    send_mail(subject='That`s your subject',
                        message='Hello ' + username +
                        '! \n Your account has been locked for security reasons' +
                        '  \n The last failed attempt occured on : ' + currentDate +
                        '  \n From a device using the IP: ' + ip_address,
                        from_email='egt.pyramid.com',
                        recipient_list=['useremail@gmail.com'])
                    user.save()
                    return Response({"code": 3}, status=status.HTTP_403_FORBIDDEN)
                

        return Response({}, status=status.HTTP_401_UNAUTHORIZED)