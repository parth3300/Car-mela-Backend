from django_filters.rest_framework import FilterSet
from .models import Car,CarOwnerShip


class CarFilter(FilterSet):
    class Meta:
        model = Car
        fields = {
            'company_id': ['exact'],
            'price': ['gt', 'lt']
        }
class CarOwnerShipFilter(FilterSet):
    class Meta:
        model = CarOwnerShip
        fields = {
            'carowner_id': ['exact'],
        }
