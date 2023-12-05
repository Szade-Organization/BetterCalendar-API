from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser

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
            'version': 'v0.0.1',
            'description': 'An API for BetterCalendar project. Currently in development - this is the only view.',
        }
        return Response(data, status=status.HTTP_200_OK)
    
class APIDBTestView(APIView):
    @swagger_auto_schema(request_body=UserDataSerializer)
    def post(self, request):
        data = JSONParser().parse(request)
        serializer = UserDataSerializer(data=data)
        if serializer.is_valid():
            # for now we ignore the data and just create a test user
            user = UserData()
            user.e_mail = "test@test.com"
            user.user_name = "testuser"
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(status=status.HTTP_200_OK)

    def get(self, request):
        data = UserData.objects.get(user_name="testuser")
        serializer = UserDataSerializer(data, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)