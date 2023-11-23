from django.urls import path
from .views import APIInformationView
from .views import APIDBTestView


urlpatterns = [
    path("info", APIInformationView.as_view(), name="api-information"),
    path("dbtest", APIDBTestView.as_view(), name="db-test")
]
