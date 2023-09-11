from django.core.wsgi import get_wsgi_application
from django.core.management import call_command
from http.server import BaseHTTPRequestHandler, HTTPServer

# Initialize Django application
application = get_wsgi_application()

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/vercel/api/emailcheck'):

        # Trigger your Django management command here
            call_command('emailcheck')

def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, RequestHandler)
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()