from django.conf import settings
import logging
from logging.handlers import TimedRotatingFileHandler
from api.models import ExpiringToken
import json
from django.http import QueryDict
from typing import Callable, Any, Optional
from django.http import HttpRequest, HttpResponse

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# Use TimedRotatingFileHandler for daily log file rotation
handler = TimedRotatingFileHandler(
    settings.API_LOG_FILE, when="midnight", interval=1, backupCount=0
)
formatter = logging.Formatter("%(asctime)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class LoggerMiddleware:
    def __init__(
        self, get_response: Callable[[HttpRequest], HttpResponse]
    ) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        # Code to be executed for each request before
        # the view (and later middleware) are called

        # Log the request details
        user = self.get_user(request)
        logger.info(
            (
                f"[0] User: {user} - Request: {request.method} {request.path} "
                f"Request params: {self.get_request_params(request)}"
            )
        )

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.
        # You can also log response details here if needed

        # Log the response details
        logger.info(
            (
                f"[2] User: {user} - Request: {request.method} {request.path} "
                f"Request params: {self.get_request_params(request)} "
                f"- Response: [{response.status_code}] "
                f"({response.reason_phrase})"
            )
        )

        return response

    def process_exception(
        self, request: HttpRequest, exception: Exception
    ) -> Optional[Any]:
        # Code to be executed for each request after
        # an exception is raised
        logger.info(
            (
                f"[E] User: {self.get_user(request)} "
                f"- Request: {request.method} {request.path} "
                f"Request params: {self.get_request_params(request)} "
                f"- Exception: {str(exception)}"
            )
        )

        return None

    def process_view(
        self,
        request: HttpRequest,
        view_func: Callable,
        view_args: tuple,
        view_kwargs: dict,
    ) -> Optional[Any]:
        # This method is optional for additional logging
        # before the view is called.
        # Example: logging the view name
        logger.info(
            (
                f"[1] User: {self.get_user(request)} "
                f"- Request: {request.method} {request.path} "
                f"Request params: {self.get_request_params(request)} "
                f"- View: {view_func.__name__} "
                f"View params: {view_args} {view_kwargs}"
            )
        )

        return None

    def get_user(self, request: HttpRequest) -> str:
        user = None
        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Token "):
            token = auth_header.split(" ")[1]
            # Get the User object from the token
            try:
                user = ExpiringToken.objects.get(key=token).user
            except ExpiringToken.DoesNotExist:
                user = None

        if not user:
            return "Anonymous"
        else:
            return f"{user.id} ({user.email})"

    def get_request_params(self, request: HttpRequest) -> dict:
        if request.method in ["GET", "DELETE"]:
            # Parameters are in the URL for GET and DELETE
            return request.GET.dict()
        elif request.method in ["POST", "PUT", "PATCH"]:
            # For POST, PUT, PATCH, handle form data or JSON
            if request.content_type == "application/json":
                # Handle JSON body
                try:
                    data = json.loads(request.body)
                    # Remove sensitive data from the request
                    if "password" in data:
                        data["password"] = "REDACTED"
                    return data
                except json.JSONDecodeError:
                    return {}
            else:
                # Handle form data
                if (
                    isinstance(request.body, (bytes, bytearray))
                    and request.body
                ):
                    request_body = request.body.decode("utf-8")
                    return QueryDict(request_body).dict()
                return request.POST.dict()
        else:
            # Default empty dict for other types
            return {}
