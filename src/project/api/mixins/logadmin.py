from typing import Any
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.http import HttpRequest
from django.conf import settings

import logging
from logging.handlers import TimedRotatingFileHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# Use TimedRotatingFileHandler for daily log file rotation
handler = TimedRotatingFileHandler(
    settings.ADMIN_LOG_FILE, when="midnight", interval=1, backupCount=0
)
formatter = logging.Formatter("%(asctime)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def get_object_fields(object):
    fields = {}
    for field in object._meta.fields:
        if field.name == "password":
            fields["password"] = "REDACTED"
        else:
            fields[field.name] = field.value_from_object(object)
    return fields


class LogAdminMixin(admin.ModelAdmin):
    class Meta:
        abstract = True

    def log_addition(
        self, request: HttpRequest, object: Any, message: Any
    ) -> LogEntry:
        logger.info(
            (
                f"Add: {get_object_fields(object)} - "
                f"Message: {message} - Request: {request}"
            )
        )

        return super().log_addition(request, object, message)

    def log_change(
        self, request: HttpRequest, object: Any, message: Any
    ) -> LogEntry:
        logger.info(
            (
                f"Change: {get_object_fields(object)} - "
                f"Message: {message} - Request: {request}"
            )
        )
        return super().log_change(request, object, message)

    def log_deletion(
        self, request: HttpRequest, object: Any, object_repr: str
    ) -> LogEntry:
        logger.info(
            f"Delete: {get_object_fields(object)} - Request: {request}"
        )
        return super().log_deletion(request, object, object_repr)
