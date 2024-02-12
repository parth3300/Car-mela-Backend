from django_filters.rest_framework import FilterSet
from .models import Car, CarOwnerShip


class CarFilter(FilterSet):
    class Meta:
        model = Car
        fields = {
            'car_ownership__carowner__id': {'exact'},
            'company_id': ['exact'],
            'price': ['gt', 'lt']
        }


class CarOwnerShipFilter(FilterSet):
    class Meta:
        model = CarOwnerShip
        fields = {
            'carowner_id': ['exact'],
        }
