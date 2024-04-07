from api import views
from django.urls import path
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

urlpatterns = [
    path("token/", views.GetToken.as_view()),
    path("demo/", views.DemoView.as_view()),
]

# It is safe to ignore the type error here
urlpatterns += router.urls  # type: ignore
