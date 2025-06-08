# messaging_app/middleware.py

from datetime import datetime, time, timedelta
from django.http import HttpResponseForbidden, HttpResponseTooManyRequests
import logging

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
        if request.path.startswith("/chat/"):
            current_time = datetime.now().time()
            start_time = time(18, 0)  # 6:00 PM
            end_time = time(21, 0)    # 9:00 PM

            if not (start_time <= current_time <= end_time):
                return HttpResponseForbidden("Chat access is only allowed between 6 PM and 9 PM.")

        return self.get_response(request)


# Middleware 3: Limit chat messages by IP (rate limiting)
class OffensiveLanguageMiddleware:
    message_logs = {}  # Class-level storage for IP tracking

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'POST' and request.path.startswith('/chat/'):
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Initialize IP log if not present
            if ip not in self.message_logs:
                self.message_logs[ip] = []

            # Remove timestamps older than 1 minute
            self.message_logs[ip] = [
                timestamp for timestamp in self.message_logs[ip]
                if now - timestamp < timedelta(minutes=1)
            ]

            if len(self.message_logs[ip]) >= 5:
                return HttpResponseTooManyRequests("Rate limit exceeded: Max 5 messages per minute.")

            self.message_logs[ip].append(now)

        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
