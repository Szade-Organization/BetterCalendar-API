from django.urls import path, include
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from knox import views as knox_views
from rest_registration.api import urls as rest_registration

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
router.register('get-activity', UserActivityViewSet, basename='get-activity')

urlpatterns = [
    path('swagger', schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),
    path('info', APIInformationView.as_view(), name='api-information'),
    path('', include(router.urls)),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('auth/logoutall/', knox_views.LogoutAllView.as_view(), name='logout-all'),
    path('auth/register/', rest_registration.register, name='register'),
    path('auth/verify-registration/', rest_registration.verify_registration, name='verify-registration'),
    path('auth/send-reset-password-link/', rest_registration.send_reset_password_link, name='send-reset-password-link'),
    path('auth/reset-password/', rest_registration.reset_password, name='reset-password'),
    path('auth/profile/', rest_registration.profile, name='profile'),
    path('auth/change-password/', rest_registration.change_password, name='change-password'),
    path('auth/change-email/', rest_registration.register_email, name='change-email'),
    path('auth/verify-email/', rest_registration.verify_email, name='verify-email'),
]

from django.conf import settings
if settings.DEBUG:
    urlpatterns += [
        path('auth/create_test_user/', developmentUserCreate.as_view(), name='create-test-user'),
    ]
