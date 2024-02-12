from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.core.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import *
from .serializers import *
from store.permissions import IsAdminOrReadOnly
from django.contrib.auth.models import AnonymousUser
from .filter import *


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAdminOrReadOnly]


class CarViewSet(ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CarFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'last_update']
    permission_classes = [IsAdminOrReadOnly]


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]


class CarOwnerViewset(ModelViewSet):
    queryset = CarOwner.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminCarOwnerSerializer
        return CarOwnerSerializer

    @action(detail=False, methods=['GET', 'PATCH'], permission_classes=[IsAuthenticated])
    def me(self, request):
        carowner = get_object_or_404(CarOwner, user=request.user)
        
        if request.method == 'GET':
            serializer = CarOwnerSerializer(carowner)
            return Response(serializer.data)

        elif request.method == 'PATCH':
            if carowner.user != request.user:
                raise PermissionDenied(
                    "You don't have permission to perform this action.")

            serializer = CarOwnerSerializer(
                carowner, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class CarOwnerShipViewSet(ModelViewSet):
    queryset = CarOwnerShip.objects.all()
    serializer_class = CarOwnerShipSerializer
    filterset_class = CarOwnerShipFilter
    permission_classes = [IsAdminOrReadOnly]


class DealerShipViewSet(ModelViewSet):
    queryset = DealerShip.objects.all()
    serializer_class = DealerShipSerializer
    permission_classes = [IsAdminOrReadOnly]


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_create(self, serializer):
        car_id = self.kwargs['car_pk']
        serializer.save(car_id=car_id)
