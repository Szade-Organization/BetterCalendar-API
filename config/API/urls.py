from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import APIInformationView
from .views import APIDBTestView

schema_view = get_schema_view(
    openapi.Info(
        title="BetterCalendar-API",
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),
    path("info", APIInformationView.as_view(), name="api-information"),
    path("dbtest", APIDBTestView.as_view(), name="db-test")
]
