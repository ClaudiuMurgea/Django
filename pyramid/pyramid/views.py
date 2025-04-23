from django.http import HttpResponse
from django.core.mail import send_mail
import random


def simple_mail(request):

    random_number = random.randint(100000, 999999)
    user = request.user

    send_mail(subject='That`s your subject',
              message='That`s your message body' + ' ' + user.username,
              from_email='',
              recipient_list=['cloudymail1@gmail.com'])

    return HttpResponse('Message send!')
