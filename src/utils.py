from .models import Meeting

def get_dates_from_origin_url(origin_url):
    # Query the database to get all meetings with the given origin URL
    meetings = Meeting.objects.filter(origin=origin_url)

    # Create a list to store the date and meeting name dictionaries
    dates_list = []

    for meeting in meetings:
        # Convert the date to a string for the dictionary
        date_str = meeting.date.strftime('%B %d, %Y at %I:%M %p')
        
        # Add the date and meeting name to the dictionary
        date_info = {
            'date': date_str,
            'name': meeting.name
        }

        dates_list.append(date_info)

    return dates_list