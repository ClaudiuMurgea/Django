from django.http import HttpResponse
from django.core.mail import send_mail
import sqlite3
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def mail_user(request):
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

            if data_type and data_value:  # Validate input
                # Check if data value exists
                if data_type == 'email':
                    cursor.execute(
                        f"SELECT COUNT(*) FROM api_user_details WHERE email = '{data_value}'")
                elif data_type == 'phone':
                    cursor.execute(
                        f"SELECT COUNT(*) FROM api_user_details WHERE phone = '{data_value}'")

                result = cursor.fetchone()[0]
                if result > 0:
                    # Update the code column in user details table
                    cursor.execute(
                        f"UPDATE api_user_details SET digits = {random_number} WHERE {data_type} = '{data_value}'")
                    # kept for reference -> "UPDATE api_user_details SET digits = ? WHERE user_id = (SELECT id FROM auth_user WHERE username = ?)", (random_number, username))
                    # the pros would be that email wouldnt be needed inside the user_details_table
                    conn.commit()
                    return JsonResponse({"status": "success"})
                else:
                    return JsonResponse({"status": "No records of the given value"}, status=401)

                username = request.user.username
                send_mail(subject='That`s your subject',
                          message='Hello ' + username +
                          '! \n Your password reset code ' +
                          str(random_number),
                          from_email='egt.pyramid.com',
                          recipient_list=['useremail@gmail.com'])

                conn.close()
            else:
                return JsonResponse({"status": "Missing required fields"}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({"status": "fail", "error": "Invalid JSON"}, status=400)

    return JsonResponse({"status": "fail", "error": "Invalid request method"}, status=405)


#
