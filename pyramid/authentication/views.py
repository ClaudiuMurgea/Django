from rest_framework import generics
from .serializers import UserSerializer, SettingsSerializer, SettingsPermission, IsManagerGroupOrSuperuser
from rest_framework_simplejwt import serializers
from rest_framework.permissions import IsAuthenticated
from django.core.mail import send_mail
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime, timedelta
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from .models import Settings
from rest_framework import status
from reports.models import Settings_history
from django.utils.timezone import now
from pyramid.custom_settings import PIN_MEASURE, PIN_EXPIRATION_TIME
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import Group
class SettingsListCreate(generics.ListCreateAPIView):
    serializer_class = SettingsSerializer
    permission_classes = [IsAuthenticated, SettingsPermission]

    def get_queryset(self):
        user = self.request.user
        return Settings.objects.filter(user_id=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            settings_instance = serializer.save(user_id=self.request.user.id)

            Settings_history.objects.create(
                user_id=settings_instance.user_id,
                minimum_characters=settings_instance.minimum_characters,
                contain_upper_case=settings_instance.contain_upper_case,
                contain_lower_case=settings_instance.contain_lower_case,
                contain_special_case=settings_instance.contain_special_case,
                contain_number=settings_instance.contain_number,
                created_at=settings_instance.created_at,  # Use the same timestamp
            )
            return JsonResponse({"message": "Settings saved successfully"})
        else:
            raise serializers.ValidationError(serializer.errors) 
        
class SettingsUpdate(generics.UpdateAPIView):
    serializer_class = SettingsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Settings.objects.filter(user_id=user)
    
    def perform_update(self, serializer):
        settings_instance = serializer.save(user_id=self.request.user.id)

        Settings_history.objects.create(
                user_id=settings_instance.user_id,
                minimum_characters=settings_instance.minimum_characters,
                contain_upper_case=settings_instance.contain_upper_case,
                contain_lower_case=settings_instance.contain_lower_case,
                contain_special_case=settings_instance.contain_special_case,
                contain_number=settings_instance.contain_number,
                created_at=settings_instance.created_at,  # Use the same timestamp
            )
        return JsonResponse({"message": "Settings saved successfully"})

class SettingsDelete(generics.DestroyAPIView):
    serializer_class = SettingsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Settings.objects.filter(user_id=user)

class RegisterUserAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserListView(APIView):
    permission_classes = [IsAuthenticated]  # Requires authentication

    def get(self, request):
        users = CustomUser.objects.all()  # Fetch all users
        serializer = UserSerializer(users, many=True)  # Serialize multiple users
        return Response(serializer.data)

class UpdateUserAPIView(APIView):
    def put(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)

        # If password is present, hash it before saving
        data = request.data.copy()
        if 'password' in data:
            data['password'] = make_password(data['password'])

        serializer = UserSerializer(user, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UnlockUserAPIView(APIView):
    permission_classes = [IsManagerGroupOrSuperuser]
    
    def post(self, request, pk):
        try:
            user = CustomUser.objects.get(pk=pk)
            user.is_active = True
            user.failed_attempts = 0
            user.save()
            return Response({}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({}, status=status.HTTP_404_NOT_FOUND)
        
class RoleSettingsAPIView(APIView):
    def get(self, request):
        try:
            groups = Group.objects.prefetch_related("settings").all()  # Optimize query

            result = []
            for group in groups:
                if hasattr(group, "settings") and group.settings:
                    fields = {
                        field.name: getattr(group.settings, field.name)
                        for field in group.settings._meta.fields if field.name not in ["id", "_state", "group"]
                    }
                    fields["group"] = group.name  # Convert Group object to string
                    result.append(fields)
            
            return Response(result if result else {"error": "No settings found for any group"}, status=200)
        except:
            return JsonResponse({}, status=400)

class AssignUserToGroupAPIView(APIView):
    def post(self, request):
        username = request.data.get("username")
        role = request.data.get("role")

        if not username or not role:
            return Response({"error": "Username and group_name are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            group = Group.objects.get(name=role)
        except Group.DoesNotExist:
            return Response({"error": "Group not found."}, status=status.HTTP_404_NOT_FOUND)

        #The clear is not a necessity but it will be used to ensure only 1 group is assigned 
        user.groups.clear() 
        user.groups.add(group)
        #"message": f"User '{username}' added to group '{role}'."
        return Response({}, status=status.HTTP_200_OK)

@csrf_exempt
def mail_user(request):
    # return JsonResponse({"status": "ok"})
    if request.method == "POST":
        try:
            # creating a 6 digit password reset code unique to each user
            random_number = random.randint(100000, 999999)
            data = json.loads(request.body)
            data_type = data.get("type")
            data_value = data.get("value")
            timestamp = datetime.now()

            if data_type and data_value:  # Validate input
                filter_kwargs = {data_type: data_value}
                query = CustomUser.objects.filter(**filter_kwargs).update(pin=random_number, code_generation_time=timestamp)
            
                if query > 0:
                    username = request.user.username
                    send_mail(subject='That`s your subject',
                          message='Hello ' + username +
                          '! \n Your password reset code ' +
                          str(random_number),
                          from_email='egt.pyramid.com',
                          recipient_list=['useremail@gmail.com'])
                    #Success
                    return JsonResponse({"pin": random_number})
                else:
                    #Value does not exist in database
                    return JsonResponse({}, status=404)
            else:
                #Missing required fields
                return JsonResponse({}, status=400)
        except json.JSONDecodeError:
            #Invalid JSON
            return JsonResponse({}, status=400)
    return JsonResponse({}, status=400)

@csrf_exempt
def verify_code(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            data_type = data.get("type")
            data_value = data.get("value")
            data_pin = data.get("pin")

            if data_type and data_value and data_pin:  # Validate input
                result = CustomUser.objects.filter(**{data_type: data_value}).values("pin", "code_generation_time").first()
                if result:
                    dbTime = result['code_generation_time']
                    current_time = now()

                    time_difference = abs(current_time - dbTime)

                    if time_difference > timedelta(**{PIN_MEASURE: PIN_EXPIRATION_TIME}):
                        #Pin is old
                        return JsonResponse({"code":2}, status=404)
                    else:

                        #Pin is recent enough
                        pin = result['pin']
                        if(int(pin) == int(data_pin)):
                            return JsonResponse({}, status=200)
                        else:
                            #Pin do not match
                            return JsonResponse({"code":1}, status=404)
                else:
                    # No email or phone found in the database
                    return JsonResponse({}, status=404)
            return JsonResponse({}, status=400)
        except:
            #Invalid JSON
            return JsonResponse({}, status=400)

@csrf_exempt
def update_user_password(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            data_type     = data.get("type")
            data_value    = data.get("value")
            data_password = data.get("password")
            
            if data_type and data_value and data_password:  # Validate input
                # Fetch current hashed password
                result = CustomUser.objects.filter(**{data_type: data_value}).values("password").first()
                if result:
                    current_hashed_password = result["password"]
                    # Check if the new password is the same or contains the old password (as substring)
                    # WARNING: You don't store the raw password, so can't check if the new contains the old raw password
                    # Instead, just check if it's the same password using Django's check_password
                    if check_password(data_password, current_hashed_password):
                        return JsonResponse({"code": 5}, status=400)

                    # Update password (it's valid and different)
                    new_hashed_password = make_password(data_password)
                    time = datetime.now()

                    ALLOWED_FIELDS = {"username", "email"}  # Only allow these fields for data_type
                    if data_type not in ALLOWED_FIELDS:
                        return JsonResponse({"error": "Invalid field name"}, status=400)

                    CustomUser.objects.filter(**{data_type: data_value}).update(
                        password=new_hashed_password,
                        password_changed_at=time
                    )
                    return JsonResponse({})
                else:
                    return JsonResponse({"error": "User not found"}, status=404) #cannot update a missing user

            #Missing required fields
            return JsonResponse({}, status=401)
        except:
            #Invalid JSON
            return JsonResponse({}, status=401)
