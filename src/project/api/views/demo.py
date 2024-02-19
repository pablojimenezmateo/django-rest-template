from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
import logging

logger = logging.getLogger("django")


class DemoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        logger.info(request.META)
        data = {"message": "This is a test JSON response", "status": "success"}
        return Response(data)
