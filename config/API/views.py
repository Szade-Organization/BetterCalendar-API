from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import *

# Create your views here.
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
    def post(self, request):
        user = UserData()
        user.e_mail = "test@test.com"
        user.user_name = "testuser"
        user.save()
        return Response(status=status.HTTP_200_OK)

    def get(self, request):
        data = UserData.objects.all().values()
        return Response(data, status=status.HTTP_200_OK)