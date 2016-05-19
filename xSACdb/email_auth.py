from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class BasicBackend:
    def get_user(self, user_id):
        U = get_user_model()
        try:
            return U.objects.get(pk=user_id)
        except U.DoesNotExist:
            return None

class EmailBackend(BasicBackend):
    def authenticate(self, username=None, password=None):
        U = get_user_model()
        #If username is an email address, then try to pull it up
        try:
            validate_email(username)
            try:
                user = U.objects.get(email=username)
            except U.DoesNotExist:
                return None
        except ValidationError:
            return None
        if user.check_password(password):
            return user
        else:
            return None
