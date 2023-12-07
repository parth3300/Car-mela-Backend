from django_filters.rest_framework import FilterSet
from .models import Car


class CarFilter(FilterSet):
    class Meta:
        model = Car
        fields = {
            'company_id': ['exact'],
            'owned_by_id': ['exact'],
            'price': ['gt', 'lt']
        }
