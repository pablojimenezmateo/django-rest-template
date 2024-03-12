from django.db import models
from django.conf import settings
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# Use TimedRotatingFileHandler for daily log file rotation
handler = logging.handlers.TimedRotatingFileHandler(
    settings.MODELS_LOG_FILE, when="midnight", interval=1, backupCount=0
)
formatter = logging.Formatter("%(asctime)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class LogCreateUpdateDeleteMixin(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):

        action = "Created" if self.pk is None else "Updated"
        log_message = (
            f"{action} {self.__class__.__name__} "
            f"- Data: {get_model_fields(self)}"
        )

        # Get the previous state of the object
        if self.pk is not None:
            try:
                previous_state = self.__class__.objects.get(pk=self.pk)
                log_message += (
                    f" - Previous data: {get_model_fields(previous_state)}"
                )
            except self.__class__.DoesNotExist:
                pass

        logger.info(log_message)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # This is a delete operation
        log_message = (
            f"Deleted {self.__class__.__name__} "
            f"- Data: {get_model_fields(self)}"
        )
        logger.info(log_message)
        super().delete(*args, **kwargs)


def get_model_fields(object: models.Model) -> dict:
    fields = {}
    for field in object._meta.fields:
        if field.name == "password":
            fields["password"] = "REDACTED"
        else:
            fields[field.name] = field.value_from_object(object)
    return fields
