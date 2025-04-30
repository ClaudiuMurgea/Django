from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import generics
from .serializers import UserSerializer, PermisionSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Permission
from django.core.mail import send_mail
import sqlite3
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.hashers import make_password
from datetime import datetime, timedelta, timezone

User = get_user_model()

class PermissionListCreate(generics.ListCreateAPIView):
    serializer_class = PermisionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Permission.objects.filter(role=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(role=self.request.user)
        else:
            print(serializer.errors)


class PermissionDelete(generics.DestroyAPIView):
    serializer_class = PermisionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Note.objects.filter(role=user)


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

from django.http import HttpResponse
from django.core.mail import send_mail
import sqlite3
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from datetime import datetime, timedelta, timezone

User = get_user_model()  # ✅ This will point to api.CustomUser

@csrf_exempt
def mail_user(request):
    # return JsonResponse({"status": "ok"})
    if request.method == "POST":
        try:
            # creating a 6 digit password reset code unique to each user
            random_number = random.randint(100000, 999999)
            conn = sqlite3.connect("db.sqlite3")
            # Connect to your SQLite database
            cursor = conn.cursor()

            data = json.loads(request.body)
            data_type = data.get("type")
            data_value = data.get("value")
            timestamp = datetime.now()

            if data_type and data_value:  # Validate input
                cursor.execute(
                    f"UPDATE api_customuser SET pin = {random_number} , code_generation_time='{ timestamp }' WHERE {data_type} = '{data_value}'")
                conn.commit()
                conn.close() 
                if cursor.rowcount > 0:
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
            conn = sqlite3.connect("db.sqlite3")
            # Connect to your SQLite database
            cursor = conn.cursor()

            data = json.loads(request.body)
            data_type = data.get("type")
            data_value = data.get("value")
            data_pin = data.get("pin")     

            if data_type and data_value and data_pin:  # Validate input


                # Select code if email or phone is correct and exists, with a code not older than 60minutes
                cursor.execute(
                        f"SELECT pin, code_generation_time FROM api_customuser WHERE {data_type} = '{ data_value }'")
                
                result = cursor.fetchone()
                conn.close()
                #protect against no entry in db
                if result is None:
                    # No email or phone found in the database
                    return JsonResponse({}, status=404)
                
                dbTime_str = result[1]
                nowTime_str = datetime.utcnow().isoformat(timespec="milliseconds") + "Z"
                # Parse dbTime (naive datetime, assuming it's in UTC or local timezone — adjust if needed)
                dbTime = datetime.strptime(dbTime_str, "%Y-%m-%d %H:%M:%S.%f").replace(tzinfo=timezone.utc)
                # Parse nowTime (ISO 8601 string with 'Z' meaning UTC)
                nowTime = datetime.strptime(nowTime_str, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
                # Compare
                time_difference = nowTime - dbTime

                if time_difference > timedelta(minutes=3):
                    #Pin is old
                    return JsonResponse({"code":2}, status=404)
                else:
                    #Pin is recent enough
                    pin = result[0]
                    if(int(pin) == int(data_pin)):
                        return JsonResponse({})
                    else:
                        #Pin do not match 
                        return JsonResponse({"code":1}, status=404)

            return JsonResponse({}, status=400)
        except:
            #Invalid JSON
            return JsonResponse({}, status=400)

@csrf_exempt
def update_user_password(request):
    if request.method == "POST":
        try:
            conn = sqlite3.connect("db.sqlite3")
            # Connect to your SQLite database
            cursor = conn.cursor()

            data = json.loads(request.body)
            data_type     = data.get("type")
            data_value    = data.get("value")     
            data_password = data.get("password")
            if data_type and data_value and data_password:  # Validate input
                hashed_password = make_password(data_password)
                
                cursor.execute(
                        f"UPDATE api_customuser SET password = '{hashed_password}' WHERE {data_type} = '{data_value}'")
                conn.commit()
                conn.close()

                if cursor.rowcount > 0:
                    return JsonResponse({})
                else:
                    #Value does not exist in database
                    return JsonResponse({}, status=401)
            #Missing required fields
            return JsonResponse({}, status=401)
        except:
            #Invalid JSON
            return JsonResponse({}, status=401)  
    