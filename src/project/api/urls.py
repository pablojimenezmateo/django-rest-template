from api import views
from django.urls import path
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
# router.register(
#     r"postal",
#     views.PostalViewSet,
#     basename="postal",
# )

urlpatterns = [
    path("token/", views.GetToken.as_view()),
]

urlpatterns += router.urls
