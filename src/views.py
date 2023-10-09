from datetime import datetime, timedelta
from django.conf import settings
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Meeting, OriginEmailStatus
from .utils import get_dates_from_origin_url

from urllib.parse import unquote



class SubmitFormView(APIView):
    def post(self, request, format=None):
        name = request.data.get('name')
        selected_date_str = request.data.get('date')
        origin = request.data.get(
            'x_origin_url', 'default_value_if_header_is_missing')
        print(selected_date_str)
        try:
            selected_date = datetime.strptime(
                selected_date_str, '%B %d, %Y at %I:%M %p')
            selected_date = timezone.make_aware(
                selected_date, timezone.get_default_timezone())
            print(selected_date)
        except ValueError:
            return Response({'error': 'Invalid date format'}, status=status.HTTP_400_BAD_REQUEST)

        # Create a new Meeting instance and save it
        meeting = Meeting(name=name, date=selected_date, origin=origin)
        meeting.save()

        return Response({
            'message': 'Response sent successfully',
        }, status=status.HTTP_200_OK)


class YourNewView(APIView):
    def post(self, request, format=None):
        try:
            data = request.data
            generated_link = data.get('generatedLink')
            origin_url = data.get('x_origin_url', 'default_value_if_header_is_missing')
            email = data.get('email')
            sentime=data.get('sentime')
            print(data)
            origin_status, created = OriginEmailStatus.objects.get_or_create(generatedLink=generated_link)
            origin_status.origin_url = origin_url
            origin_status.email = email
            origin_status.send_delay = sentime
            origin_status.save()

            return JsonResponse({'message': 'Data saved successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Admin(APIView):
    def post(self, request, format=None):
        try:
            data = request.data
            link = data.get('link')

            found = Meeting.objects.filter(origin=link)
             
            if found:
                for obj in found:
                    print(found)
                serialized_data = [{'Name': obj.name, 'Date': obj.date} for obj in found]
                print(serialized_data)
            else:
                print(f'No matches found for origin: {link}')
                serialized_data = []  # Empty list when no matches are found
            
            return JsonResponse({'data': serialized_data}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

