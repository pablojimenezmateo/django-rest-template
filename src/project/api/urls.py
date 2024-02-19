from api import views
from django.urls import path
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

urlpatterns = [
    path("token/", views.GetToken.as_view()),
    path("demo/", views.DemoView.as_view()),
]

urlpatterns += router.urls
