from django.contrib import admin
from api.models import ExpiringToken
from api.mixins import LogAdminMixin


# Register your models here.
class ExpiringTokenAdmin(LogAdminMixin, admin.ModelAdmin):
    list_display = (
        "key",
        "user",
        "created",
        "expiry_date",
        "is_used",
        "permanent",
    )
    search_fields = (
        "user__username",
        "key",
    )
    list_filter = ("is_used", "permanent", "created", "expiry_date")
    ordering = ("-created",)


admin.site.register(ExpiringToken, ExpiringTokenAdmin)
