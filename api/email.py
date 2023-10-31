from contio_backend import settings
from django.core.mail import send_mail
import json
import time
from django.utils import timezone
from src.models import OriginEmailStatus, Meeting
from django.conf import settings
import datetime
import sys
from http.server import BaseHTTPRequestHandler
import os
import django
# You stay here please!
django.setup()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))


class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        unsent_emails = OriginEmailStatus.objects.filter(email_sent=False)
        for email_status in unsent_emails:
            print('in loop...')
            current_time = timezone.now()
            link = email_status.generatedLink
            creation_time = email_status.created_at
            send_delay = email_status.send_delay
            print('delay:', send_delay)
            target_time = creation_time + datetime.timedelta(days=send_delay)
            print('Target Time: ' + target_time.strftime("%m/%d/%Y, %H:%M:%S"))
            tolerance = datetime.timedelta(seconds=60)
            if current_time >= target_time:
                send_scheduled_email(email_status)
                print('sending, please work...')
            else:
                print('No emails or not time yet.')

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(
            'Email Checking executed successfully. Please work!'.encode('utf-8'))


def send_scheduled_email(email_status):
    print(f"Attempting to send email to: {email_status.email}")

    print(f"Meeting Generated Link: {email_status.generatedLink}")

    matching_meetings = Meeting.objects.filter(
        origin=email_status.generatedLink)
    print(matching_meetings)

    subject = 'Your scheduling responses'
    message = f'Hi There, thank you for using Contio!\n\n'

    if matching_meetings:
        message += 'Here are the responses of your scheduled meeting:\n\n'

        meeting_info = {}

        for meeting in matching_meetings:
            meeting_date = meeting.date.strftime('%B %d, %Y at %I:%M %p')
            user_name = meeting.name

            if meeting_date in meeting_info:
                meeting_info[meeting_date]['count'] += 1
                meeting_info[meeting_date]['users'].append(user_name)
            else:
                meeting_info[meeting_date] = {
                    'count': 1, 'users': [user_name]}

        for meeting_date, info in meeting_info.items():
            count = info['count']
            if count > 2:
                users = ', '.join(info['users'])
                message += f'{users} selected the meeting on {meeting_date}.\n'
            else:
                users = 'and '.join(info['users'])
                message += f'{users} selected the meeting on {meeting_date}.\n'
    else:
        message += 'Oh no! You got no responses 😢. Maybe try smoke signals?\n'

    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email_status.email, ]

    email_status.email_sent = True
    email_status.save()

    try:
        print("Before sending email...")
        print(f"Subject: {subject}")
        print(f"Message: {message}")
        print(f"From: {email_from}")
        print(f"To: {recipient_list}")

        send_mail(subject, message, email_from, recipient_list)

        print("Email sent successfully.")

    except Exception as e:
        print(f"Email sending error: {str(e)}")
