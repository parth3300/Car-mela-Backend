from django_filters.rest_framework import FilterSet
from .models import CarWithOwnerShip


class CarFilter(FilterSet):
    class Meta:
        model = CarWithOwnerShip
        fields = {
            'company_id': ['exact'],
            'owned_by_id': ['exact'],
            'price': ['gt', 'lt']
        }
