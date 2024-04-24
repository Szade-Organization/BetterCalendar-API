from django.contrib.auth import login

from rest_framework.request import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer

from knox.views import LoginView as KnoxLoginView
from drf_yasg.utils import swagger_auto_schema

from .custom.generic_permission_view_set import GenericPermissionViewSet

from .models import *
from .serializers import *
from .filters import *


@swagger_auto_schema(method='get')
class APIInformationView(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

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


class CategoryViewSet(GenericPermissionViewSet):
    serializer_class = CategorySerializer
    filterset_class = CategoryFilter
    model_class = Category
    queryset = Category.objects.all()


class ActivityViewSet(GenericPermissionViewSet):
    serializer_class = ActivitySerializer
    filterset_class = ActivityFilter
    model_class = Activity
    queryset = Activity.objects.all()


class LoginView(KnoxLoginView):
    serializer_class = AuthSerializer
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()

    @swagger_auto_schema(request_body=AuthTokenSerializer)
    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)
    
from knox.models import AuthToken
from django.conf import settings


# TODO: Remove this function in production

class developmentUserCreate(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    serializer_class = UserSerializer
    
    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        if not settings.DEBUG:
            return Response({'error': 'This endpoint is only available in development mode'}, status=status.HTTP_403_FORBIDDEN)
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['email'] = serializer.validated_data.get('username') + '@example.com'
        serializer.validated_data['is_active'] = True
        user = serializer.save()
        _, token = AuthToken.objects.create(user)
        return Response({'token': 'Token ' + token}, status=status.HTTP_201_CREATED)
        
        
    
    
