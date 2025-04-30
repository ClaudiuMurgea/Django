from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import login
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from reports.models import User_logs
from django.utils.timezone import now
from api.models import CustomUser
from django.core.mail import send_mail

User = get_user_model()

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
            
            User_logs.objects.create(
                user_id=user.id,
                username=user.username,
                ip_address=ip_address,
                action='SUCCESSFUL_LOGIN',
                timestamp=now()
            )

            if user.failed_attempts >= 5:
                return Response({"detail": "Account locked due to multiple failed login attempts."}, status=status.HTTP_403_FORBIDDEN)
            else:
                CustomUser.objects.filter(id=user.id).update(failed_attempts=0, locked="no")

            return Response(response.data, status=status.HTTP_200_OK)
        except Exception as e:
            # ❌ FAILURE: If serializer raises an error (e.g. wrong username/password)
            username = request.data.get("username")
            ip_address = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', 'Unknown'))

            #check if the given username is correct, if it is, we populate the user_id, otherwise the user_id will stay NULL
            user = User.objects.filter(username=username).first()
            user_id = user.id if user else None  # Get user_id or None if not found

            # Create a log entry
            User_logs.objects.create( 
                username=username,
                user_id=user_id,
                ip_address=ip_address,  
                action="FAILED_LOGIN", 
                timestamp=now()
            ) 

            if user_id != None:
                if user.failed_attempts < 5:
                    user.failed_attempts += 1
                elif user.failed_attempts >= 5 and user.locked == "no":
                    user.locked = "yes"
                    send_mail(subject='That`s your subject',
                        message='Hello ' + username +
                        '! \n Your account has been locked due to 5 consecutive failures to login!',
                        from_email='egt.pyramid.com',
                        recipient_list=['useremail@gmail.com'])
                user.save()

        return Response({'message': 'Invalid credentials or internal error'}, status=status.HTTP_401_UNAUTHORIZED)