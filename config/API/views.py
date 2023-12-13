from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets

from drf_yasg.utils import swagger_auto_schema

from .models import *
from .serializers import *

# Create your views here.

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
    

class ActivityViewSet(viewsets.ModelViewSet):
    """
    This viewset provides list, create, retrieve, update, partial_update and destroy actions for Activity model.
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer