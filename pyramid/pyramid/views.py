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
                    f"UPDATE api_customuser SET digits = {random_number} , code_generation_time='{ timestamp }' WHERE {data_type} = '{data_value}'")
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
                    return JsonResponse({"status": "success", "digits": random_number})
                else:
                    message = f"The {data_type} doesn't exist in the database!"
                    return JsonResponse({"status": "fail", "error": message}, status=401)
            else:
                return JsonResponse({"status": "fail", "error": "Missing required fields"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"status": "fail", "error": "Invalid JSON"}, status=400)

    return JsonResponse({"status": "fail", "error": "Invalid request method"}, status=405)


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
            data_code = data.get("code")     

            if data_type and data_value and data_code:  # Validate input


                # Select code if email or phone is correct and exists, with a code not older than 60minutes
                cursor.execute(
                        f"SELECT digits, code_generation_time FROM api_customuser WHERE {data_type} = '{ data_value }'")
                
                result = cursor.fetchone()
                conn.close()
                #protect against no entry in db

                # Sample values   
                dbTime_str = result[1]
                nowTime_str = datetime.utcnow().isoformat(timespec="milliseconds") + "Z"

                # Parse dbTime (naive datetime, assuming it's in UTC or local timezone — adjust if needed)
                dbTime = datetime.strptime(dbTime_str, "%Y-%m-%d %H:%M:%S.%f").replace(tzinfo=timezone.utc)

                # Parse nowTime (ISO 8601 string with 'Z' meaning UTC)
                nowTime = datetime.strptime(nowTime_str, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)

                # Compare
                time_difference = nowTime - dbTime

                if time_difference > timedelta(minutes=60):
                    return JsonResponse({"status":"old"})

                else:
                    return JsonResponse({"status":"recent"})

                return JsonResponse({"status":time_difference})

                time_difference = now - result[1]
                return JsonResponse({"status":"old"})

                if time_difference > timedelta(minutes=60):
                    return JsonResponse({"status":"old"})
                else:
                    return JsonResponse({"status":"recent"})

                message = f"The {data_type} is incorrect or more than 60 minutes have passed!"

                if result is None:
                    return JsonResponse({"status": "fail", "error": message})
                else:
                    digits = result[0]

                if(int(digits) == int(data_code)):
                    return JsonResponse({"status":"success"})
                else: 
                    return JsonResponse({"status": "fail", "error": "Digits do not match"})

            return JsonResponse({"status":"fail", "error":"Missing required fields"})
        except:
            return JsonResponse({"status":"fail", "error":"Invalid Json or internal error"})

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
                    return JsonResponse({"status": "success"})
                else:
                    message = f"The {data_type} doesn't exist in the database!"
                    return JsonResponse({"status": "fail", "error": message}, status=401)
            
            return JsonResponse({"status": "fail", "error": "Missing required fields"}, status=401)
        except:
            return JsonResponse({"status":"fail"})  
                