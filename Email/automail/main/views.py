from django.shortcuts import render,redirect,HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Employee, Log
from .serializers import EmployeeSerializer
from rest_framework.renderers import JSONRenderer
from datetime import datetime
from pprint import pprint
from django.conf import settings
from django.core.mail import send_mail



@api_view()
def home(request):
    emp = Employee.objects.all()
    serializer = EmployeeSerializer(emp,many = True)
    json_data = JSONRenderer().render(serializer.data)

# Storing todays date to compare
    today = datetime.now().strftime("%d-%m")
    print("today- ",today)
    
# Making 2 lists to store events 
    birthdays = []
    anniversaries = []

# Iterating over all the objects to check for bday
    for item in emp.values('id', 'name', 'birthday', 'doj','email'):
        bday = item['birthday'].strftime("%d-%m")
        if bday == today:
            his_id = item['id']
            his_name = item['name']
            his_reason = 'Birthday'
            email = item['email']
            birthdays.append([his_id,his_name,his_reason,email])
#  SENDING EMAIL
            subject = 'Congratulations On Your Birthday!!'
            message = f'Hi {his_name},  Cheers to more fun, more memories, and more cake, Happy Birthday.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [ email,]
            send_mail( subject, message, email_from, recipient_list )

        # checking for work anniversary

        doj = item['doj'].strftime("%d-%m")
        if doj == today:
            his_id = item['id']
            his_name = item['name']
            his_reason = 'Work Anniversary'
            email = item['email']
            anniversaries.append([his_id,his_name,his_reason,email])
#   Sending Email
            subject = 'Congratulations On Your Work Anniversary!!'
            message = f'Hi {his_name}, Best wishes as you continue to build your career with our team! Happy work anniversary!.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail( subject, message, email_from, recipient_list )
            
#making entry in Log Table

    if len(birthdays)>0:
        for bday in birthdays:
            newlog = Log(date = datetime.now(),emp_id = bday[0],emp_name = bday[1],event = bday[2],email = bday[3])
            newlog.save()

    if len(anniversaries)>0:
        for ann in anniversaries:
            newlog = Log(date = datetime.now(),emp_id = ann[0],emp_name = ann[1],event = ann[2], email = ann[3])
            newlog.save()    
    
    if len(birthdays) == 0 and len(anniversaries) == 0 :
        newlog = Log(date = today,emp_id = 'Null',emp_name = 'Null',event = 'Null')
        newlog.save()




    
    return HttpResponse(json_data,content_type='application/json')
