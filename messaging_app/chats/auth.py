#week 5 assignment task 0
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User

class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication to ensure user is active and authenticated.
    """

    def authenticate(self, request):
        """
        Override to perform custom validation.
        """
        raw_token = self.get_raw_token(self.get_header(request))

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        user = self.get_user(validated_token)

        if not user.is_active:
            raise AuthenticationFailed('User is inactive or deleted.', code='user_inactive')

        return (user, validated_token)

