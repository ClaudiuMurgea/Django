from django.http import HttpResponse
from django.core.mail import send_mail
import sqlite3
import random


def simple_mail(request):

    random_number = random.randint(100000, 999999)
    user = request.user
    username = user.username
    conn = sqlite3.connect("database.db")
#
    # Connect to your SQLite database
    cursor = conn.cursor()

    # Check if the user exists
    cursor.execute("SELECT COUNT(*) FROM auth_user WHERE name = ?", (username))
    result = cursor.fetchone()[0]

    if result > 0:
        # Update the 'digits' column in 'details' table
        cursor.execute(
            "UPDATE api_user_details SET digits = ? WHERE user_id = (SELECT id FROM user WHERE name = ?)", (random_number, username))
        conn.commit()
        print("Digits updated successfully!")
    else:
        print("Sorry, user not found.")
    conn.close()
#
    send_mail(subject='That`s your subject',
              message='Hello ' + username +
              ' \\n Your password reset code ' + str(random_number),
              from_email='egt.pyramid.com',
              recipient_list=['cloudymail1@gmail.com'])

    return HttpResponse('Message send!')
