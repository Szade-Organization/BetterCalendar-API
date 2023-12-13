from django.urls import path, include
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .views import *

schema_view = get_schema_view(
    openapi.Info(
        title='BetterCalendar-API',
        default_version='v1',
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register('category', CategoryViewSet, basename='category')
router.register('activity', ActivityViewSet, basename='activity')

urlpatterns = [
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),
    path('info', APIInformationView.as_view(), name='api-information'),
    path('', include(router.urls)),
]
