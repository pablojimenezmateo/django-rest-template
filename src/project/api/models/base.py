from api.mixins import LogCreateUpdateDeleteMixin
from django.db import models


class Base(LogCreateUpdateDeleteMixin):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
