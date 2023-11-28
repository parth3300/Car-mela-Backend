from django.shortcuts import render
from .serializers import *
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.mixins import RetrieveModelMixin
from .models import *


class CarViewSet(ModelViewSet, RetrieveModelMixin):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class ReviewViewSet(ModelViewSet):

    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(car_id=self.kwargs['car_pk'])

    def get_serializer_context(self):
        return {'car_id': self.kwargs['car_pk']}


# Create your views here.
