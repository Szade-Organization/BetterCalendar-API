from rest_framework.request import *
from rest_framework.response import Response
from rest_framework import status, viewsets
from django_filters.rest_framework import DjangoFilterBackend

class GenericPermissionViewSet(viewsets.ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = '__all__'

    def list(self, request: Request):
        if request.user.id is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        user = request.user.id
        query_user = request.query_params.get("user")
        if request.user.is_staff and query_user != None:
            user = query_user
        self.remove_user_from_query(request)

        queryset = self.model_class.objects.filter(user_id = user)
        
        filterset = self.filterset_class(request.query_params, queryset=queryset)
        serializer = self.serializer_class(filterset.qs, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request: Request, *args, **kwargs):
        object = self.try_get_object(kwargs.get('pk'))
        if object is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if not request.user.is_staff and request.user.id != object.user_id:
            return Response(status=status.HTTP_403_FORBIDDEN)
        serializer = self.serializer_class(object)
        return Response(serializer.data)
    
    def create(self, request: Request, *args, **kwargs):
        if request.user.id is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        if not request.user.is_staff or request.data.get('user') is None:
            self.update_user(request)
        
        return super().create(request, *args, **kwargs)
    
    def update(self, request: Request, *args, **kwargs):
        object = self.try_get_object(kwargs.get('pk'))
        if object is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if not request.user.is_staff:
            if request.user.id != object.user_id:
                return Response(status=status.HTTP_403_FORBIDDEN)
            self.update_user(request)

        return super().update(request, *args, **kwargs)

    def patrial_update(self, request: Request, *args, **kwargs):
        object = self.try_get_object(kwargs.get('pk'))
        if object is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if not request.user.is_staff:
            if request.user.id != object.user_id:
                return Response(status=status.HTTP_403_FORBIDDEN)
            if (request.data.get("user") is not None):
                self.update_user(request)
        
        return super().patrial_update(request, *args, **kwargs)
    
    def destroy(self, request: Request, *args, **kwargs):
        object = self.try_get_object(kwargs.get('pk'))
        if object is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if not request.user.is_staff and request.user.id != object.user_id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        return super().destroy(request, *args, **kwargs)
    
    def try_get_object(self, id):
        try:
            return self.model_class.objects.get(id = id)
        except:
            return None
        
    def update_user(self, request):
        try:
            request.data['user'] = request.user.id
        except AttributeError:
            request.data._mutable = True
            request.data['user'] = request.user.id
            request.data._mutable = False
    
    def remove_user_from_query(self, request : Request):
        if request.query_params.get("user") is not None:
            try:
                request.query_params.pop("user")
            except AttributeError:
                request.query_params._mutable = True
                request.query_params.pop("user")
                request.query_params._mutable = False