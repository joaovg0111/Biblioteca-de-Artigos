from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
    """
    Custom authentication backend.
    Allows users to log in using their email address.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            # Try to find a user matching the given email
            user = UserModel.objects.get(email__iexact=username)
        except UserModel.DoesNotExist:
            # If no user is found, return None -- Django will then try the next backend.
            return None
        
        # Check if the password is correct for that user
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
