from django.contrib.auth import login

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer

from knox.views import LoginView as KnoxLoginView
from drf_yasg.utils import swagger_auto_schema

from .models import *
from .serializers import *
from .filters import *


@swagger_auto_schema(method='get')
class APIInformationView(APIView):
    def get(self, request):
        """
        List basic information about the API.
        """
        data = {
            'api_name': 'BetterCalendar-API',
            'version': 'v0.0.4',
            'description': 'An API for BetterCalendar project. Currently in development.',
        }
        return Response(data, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    This viewset provides list, create, retrieve, update, partial_update and destroy actions for Category model.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'
    filterset_class = CategoryFilter


class ActivityViewSet(viewsets.ModelViewSet):
    """
    This viewset provides list, create, retrieve, update, partial_update and destroy actions for Activity model.
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'
    filterset_class = ActivityFilter


class LoginView(KnoxLoginView):
    serializer_class = AuthSerializer
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(request_body=AuthTokenSerializer)
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)
