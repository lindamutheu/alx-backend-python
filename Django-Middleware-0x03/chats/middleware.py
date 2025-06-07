# messaging_app/middleware.py

from datetime import datetime
import logging

# Set up a logger
logger = logging.getLogger(__name__)
handler = logging.FileHandler('user_requests.log')  # File to log to
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)
        
        response = self.get_response(request)
        return response
