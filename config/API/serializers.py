import django_filters
from rest_framework import serializers
from .models import *
from .validators import *


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ActivitySerializer(serializers.ModelSerializer):    
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