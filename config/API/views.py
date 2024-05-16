from django.contrib.auth import login
from django.utils import timezone

from rest_framework.request import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework import viewsets

from knox.views import LoginView as KnoxLoginView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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
    queryset = Category.objects.all()


class ActivityViewSet(GenericPermissionViewSet):
    serializer_class = ActivitySerializer
    filterset_class = ActivityFilter
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
        
        
    
class UserActivityViewSet(viewsets.ViewSet):
    serializer_class = UserActivitySerializer
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'state', 
                in_=openapi.IN_QUERY, 
                description="List of states to query (e.g., 'recent', 'next', 'current')", 
                type=openapi.TYPE_ARRAY,
                items = openapi.Items(type=openapi.TYPE_STRING),
                required=True, 
                collectionFormat='multi'
            ),
            openapi.Parameter(
                'count', 
                in_=openapi.IN_QUERY, 
                description="List of counts corresponding to each state, must be integers. Pass 0 to get all activities for a given state.", 
                type=openapi.TYPE_ARRAY,
                items = openapi.Items(type=openapi.TYPE_INTEGER), 
                required=True, 
                collectionFormat='multi'
            )
        ]
    )
    def list(self, request):
        def _checkEmpty(state, count):
            if not state:
                return Response({'error': 'State is empty'}, status=status.HTTP_400_BAD_REQUEST)
            if not count:
                return Response({'error': 'Count is empty'}, status=status.HTTP_400_BAD_REQUEST)
            return None
        
        user = request.user
        state = request.query_params.getlist('state')
        count = request.query_params.getlist('count')
        
        check_empty = _checkEmpty(state, count)
        if check_empty:
            return check_empty
        allowed_states = ['recent', 'next', 'current']
        if any(t not in allowed_states for t in state):
            invalid_states = [t for t in state if t not in allowed_states]
            return Response({'error': 'Invalid states: ' + ', '.join(invalid_states)}, status=status.HTTP_400_BAD_REQUEST)
            
        count = [int(c) for c in count]
        activities = {t: [] for t in state}
        
        if len(state) != len(count):
            return Response({'error': 'State and count must have the same length (you need to pass a count for every given state)'}, status=status.HTTP_400_BAD_REQUEST)

        for t, n in zip(state, count):
            activity = self._getActivity(user, t, n)
            if activity:
                activities[t].extend(activity)

        serializer = self.serializer_class(activities)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def _getCurrentActivity(self, user, n):
        """ Retrieves the current activity if it exists """
        a = Activity.objects.filter(user=user, date_start__lte=timezone.now(), date_end__gte=timezone.now()).order_by('date_start')
        if n:
            return a[:n]
        return a
    
    def _getRecentActivities(self, user, n):
        a = Activity.objects.filter(
            user=user, 
            date_end__lt=timezone.now()
        ).order_by('-date_end')
        if n:
            return a[:n]
        return a
    
    def _getNextActivities(self, user, n):
        a = Activity.objects.filter(
            user=user,
            date_start__gt=timezone.now()
        ).order_by('date_start')
        if n:
            return a[:n]
        return a

    def _getActivity(self, user, t, n):
        """ Retrieves activities based on type (recent, next, current) """
        if t == 'recent':
            return self._getRecentActivities(user, n)
        elif t == 'next':
            return self._getNextActivities(user, n)
        elif t == 'current':
            return self._getCurrentActivity(user, n)
            
