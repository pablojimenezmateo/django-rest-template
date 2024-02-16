from django.http import JsonResponse
from api.models import ExpiringToken
from django.utils import timezone
import logging
from django.conf import settings
from datetime import timedelta

logger = logging.getLogger("django")


class CheckTokenExpiryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before the view is called
        auth_header = request.headers.get("Authorization")
        if auth_header and "Token" in auth_header:
            token_key = auth_header.split(" ")[1]
            try:
                token = ExpiringToken.objects.get(key=token_key)
                if not token.permanent and token.expiry_date <= timezone.now():
                    token.delete()  # Deleting expired token
                    return JsonResponse(
                        {"error": "Token has expired"}, status=401
                    )
                # If the token only has 1 hour left, we extend the expiry date
                elif token.expiry_date <= timezone.now() + timedelta(hours=1):
                    token.expiry_date = timezone.now() + timedelta(
                        hours=settings.TOKEN_EXPIRY_HOURS
                    )
                    token.save()

            except ExpiringToken.DoesNotExist:
                return JsonResponse({"error": "No token found"}, status=403)

        response = self.get_response(request)

        return response
