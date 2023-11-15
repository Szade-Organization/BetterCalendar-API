from django.urls import path
from .views import APIInformationView


urlpatterns = [
    path("info", APIInformationView.as_view(), name="api-information"),
]
