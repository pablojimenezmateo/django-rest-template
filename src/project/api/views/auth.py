from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import permissions
from api.serializers import AuthTokenSerializer
from rest_framework.response import Response


class GetToken(ObtainAuthToken):
    """
    Endpoint to get an Authorization token
    """

    permission_classes = [permissions.AllowAny]
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = AuthTokenSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "id": user.pk,
                "username": user.username,
                "email": user.email,
                "token": token.key,
            }
        )
