from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db import models
from rest_framework.authtoken.models import Token
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from api.mixins import LogCreateUpdateDeleteMixin


class UsernameOrEmailBackend(ModelBackend):
    def authenticate(
        self, request, username=None, email=None, password=None, **kwargs
    ):
        UserModel = get_user_model()

        if not (username or email):
            return None

        if username:
            try:
                # try to fetch user by username
                user = UserModel.objects.get(username=username)
            except UserModel.DoesNotExist:
                return None
        if email:
            try:
                # if username does not exist, try with email
                user = UserModel.objects.get(email=email)
            except UserModel.DoesNotExist:
                return None

        if user.check_password(password):
            return user

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None


def default_expiry():
    return timezone.now() + timedelta(hours=settings.TOKEN_EXPIRY_HOURS)


class ExpiringTokenManager(models.Manager):
    """
    A custom manager that always returns a token that is not expired
    """

    def get_updated(self, **kwargs):
        now = timezone.now()
        token, created = super().get_or_create(**kwargs)

        # Check if token is expired or used, and not permanent
        if (now >= token.expiry_date) and not token.permanent:
            # Delete the old token
            token.delete()

            # Create a new token
            token = self.model.objects.create(**kwargs)

        return (
            token,
            created or not token.permanent,
        )  # created will be False if a new token is generated


class ExpiringToken(LogCreateUpdateDeleteMixin, Token):
    expiry_date = models.DateTimeField(default=default_expiry)
    is_used = models.BooleanField(default=False)
    permanent = models.BooleanField(default=False)
    objects = ExpiringTokenManager()  # type: ignore
