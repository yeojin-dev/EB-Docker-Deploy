from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import check_password

User = get_user_model()


class SettingsBackend:

    def authenticate(self, request, username=None, password=None):
        login_valid = (settings.ADMIN_LOGIN == username)
        pwd_valid = check_password(password, settings.ADMIN_PASSWORD)
        if login_valid and pwd_valid:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Create a new user. There's no need to set a password
                # because only the password from settings.py is checked.
                user = User.objects.create_superuser(
                    username=username,
                    email='a@a.com',
                    password='pbkdf2_sha256$100000$kbjAfbjjSOdA$WeU1/+gnYYIOqDDPmE0bJIIYmr15m7U4sEEJuDhuWx0=',
                )
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
