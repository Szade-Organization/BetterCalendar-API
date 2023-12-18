import django_filters
from .models import *

class ActivityFilter(django_filters.FilterSet):
    class Meta:
        model = Activity
        fields = '__all__'
        
    name = django_filters.CharFilter(lookup_expr='icontains')
    user = django_filters.CharFilter(lookup_expr='exact')
    category = django_filters.CharFilter(lookup_expr='exact')
    category__name = django_filters.CharFilter(lookup_expr='icontains')
    category__description = django_filters.CharFilter(lookup_expr='icontains')
    description = django_filters.CharFilter(lookup_expr='icontains')
    date_start = django_filters.DateTimeFilter(lookup_expr='gte')
    date_end = django_filters.DateTimeFilter(lookup_expr='lte')
    length = django_filters.DurationFilter()
    importance_level = django_filters.CharFilter(lookup_expr='exact')
    date_created = django_filters.DateTimeFilter(lookup_expr='gte')
    date_modified = django_filters.DateTimeFilter(lookup_expr='gte')
    is_planned = django_filters.BooleanFilter(method='filter_is_planned')
    
            
    def filter_is_planned(self, queryset, name, value):
        if value:
            return queryset.filter(date_start__isnull=False, date_end__isnull=False)
        else:
            return queryset.filter(date_start__isnull=True, date_end__isnull=True)

class CategoryFilter(django_filters.FilterSet):
    class Meta:
        model = Category
        fields = '__all__'
        
    name = django_filters.CharFilter(lookup_expr='icontains')
    user = django_filters.CharFilter(lookup_expr='exact')
    description = django_filters.CharFilter(lookup_expr='icontains')
    color = django_filters.CharFilter(lookup_expr='exact')
    icon = django_filters.CharFilter(lookup_expr='exact')
    importance_level = django_filters.CharFilter(lookup_expr='exact')
    date_created = django_filters.DateTimeFilter(lookup_expr='gte')
    date_modified = django_filters.DateTimeFilter(lookup_expr='gte')
    
    
    