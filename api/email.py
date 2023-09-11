from django.core.management import call_command
from http import HTTPStatus

def trigger_emailcheck(request):
    # Call your custom management command
    call_command('emailcheck')
    
    # Return an HTTP response indicating success
    return {
        'statusCode': HTTPStatus.OK,
        'body': 'Email check triggered successfully',
    }





