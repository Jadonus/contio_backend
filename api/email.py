# Import necessary modules
from http.server import BaseHTTPRequestHandler
import os
import django

django.setup()
import sys
from django.conf import settings
from src.models import OriginEmailStatus, Meeting
from django.utils import timezone
import time
import json
from django.core.mail import send_mail

# Initialize Django
from contio_backend import settings  # Replace 'myproject' with your project name

# Add your project's base directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Your send_scheduled_emails function
def send_scheduled_emails():
    current_time = timezone.now()

    # Get all unsent emails scheduled for sending
    unsent_emails = OriginEmailStatus.objects.filter(email_sent=False)

    # Print a message or handle output as needed
    print(f'Sending emails to {len(unsent_emails)} recipients.')

    for email_status in unsent_emails:
        print(f"Attempting to send email to: {email_status.email}")

        # Fetch all Meetings with a matching origikn
        print(f"OriginEmailStatus Origin: {email_status.origin}")

        matching_meetings = Meeting.objects.filter(origin=email_status.generatedLink)
        print(f"Meeting Generated Link: {email_status.generatedLink}")

        subject = 'Your scheduling responses'
        message = f'Hi There, thank you for using Contio!\n\n'

        if matching_meetings:
            # Create a message to include details of all matching meetings
            message += 'Here are the responses of your scheduled meeting:\n\n'

            meeting_info = {}

            for meeting in matching_meetings:
                meeting_date = meeting.date.strftime('%B %d, %Y at %I:%M %p')
                user_name = meeting.name

                # Update the meeting_info dictionary
                if meeting_date in meeting_info:
                    meeting_info[meeting_date]['count'] += 1
                    meeting_info[meeting_date]['users'].append(user_name)
                else:
                    meeting_info[meeting_date] = {'count': 1, 'users': [user_name]}

            for meeting_date, info in meeting_info.items():
                count = info['count']
                users = ', '.join(info['users'])
                message += f'{users} selected the meeting on {meeting_date}:\n'
        else:
            # If no matching meetings found, include a message indicating so
            message += 'Oh no! You got no responses 😢. Maybe try smoke signals?\n'

        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email_status.email, ]

        # Update the email_sent status to True before sending the email
        email_status.email_sent = True
        email_status.save()

        try:
            # Debugging: Print before sending the email
            print("Before sending email...")
            print(f"Subject: {subject}")
            print(f"Message: {message}")
            print(f"From: {email_from}")
            print(f"To: {recipient_list}")

            # Send the email
            send_mail(subject, message, email_from, recipient_list)

            # Debugging: Print after sending the email
            print("Email sent successfully.")

            # Delete the OriginEmailStatus record after sending the email
        except Exception as e:
            # Debugging: Print any exceptions that occur during email sending
            print(f"Email sending error: {str(e)}")

# Define the handler for Vercel
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Call your script here when a GET request is made
        send_scheduled_emails()
        
        # Respond with a success message
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('Script executed successfully'.encode('utf-8'))
        return
# Entry point for Vercel
