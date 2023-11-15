from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


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
