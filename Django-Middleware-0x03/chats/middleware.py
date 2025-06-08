# messaging_app/middleware.py

from datetime import datetime, time
import logging
from django.http import HttpResponseForbidden

# Set up a logger
logger = logging.getLogger(__name__)
handler = logging.FileHandler('user_requests.log')  # File to log to
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Middleware 1: Logs all requests
class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)

        response = self.get_response(request)
        return response


# Middleware 2: Restricts chat access based on time
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only restrict access for chat URLs
        if request.path.startswith("/chat/"):
            current_time = datetime.now().time()
            start_time = time(18, 0)  # 6:00 PM
            end_time = time(21, 0)    # 9:00 PM

            if not (start_time <= current_time <= end_time):
                return HttpResponseForbidden("Chat access is only allowed between 6 PM and 9 PM.")

        return self.get_response(request)
