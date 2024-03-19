import django_filters
from rest_framework import serializers
from .models import *
from .validators import *

from .models import User
from django.contrib.auth import authenticate


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    
    class Meta:
        model = Category
        fields = '__all__' 


class ActivitySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = Activity
        fields = '__all__'

    def get_fields(self):
        fields = super().get_fields()
        fields['is_planned'] = serializers.BooleanField(read_only=True)
        return fields

    def validate(self, data):
        validate_date_period(data.get('date_start'), data.get('date_end'))
        return data


class UserSerializer(serializers.ModelSerializer):
    '''serializer for the user object'''
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class AuthSerializer(serializers.Serializer):
    '''serializer for the user authentication object'''
    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )

        if not user:
            msg = ('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user
        return
