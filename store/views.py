from django.shortcuts import render
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.mixins import RetrieveModelMixin
from .models import *
from store.permissions import IsAdminOrReadOnly
from django.contrib.auth.models import AnonymousUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from .filter import CarFilter, CarOwnerShipFilter
from rest_framework.filters import SearchFilter, OrderingFilter


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

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminCarOwnerSerializer
        return CarOwnerSerializer

    @action(detail=False, methods=['GET', 'PATCH'], permission_classes=[IsAuthenticated])
    def me(self, request):
        try:
            carowner = CarOwner.objects.get(user_id=request.user.id)

            if request.method == 'GET':
                serializer = CarOwnerSerializer(carowner)
                return Response(serializer.data)

            elif request.method == 'PUT':
                if carowner.user != request.user:
                    raise PermissionDenied(
                        "You don't have permission to perform this action.")

                serializer = CarOwnerSerializer(carowner, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)

        except CarOwner.DoesNotExist:
            raise PermissionDenied(
                'Authentication credentials were not provided or the user is not a CarOwner.')


class CarOwnerShipViewSet(ModelViewSet):
    queryset = CarOwnerShip.objects.all()
    serializer_class = CarOwnerShipSerializer
    filterset_class = CarOwnerShipFilter
    permission_classes = [IsAdminOrReadOnly]



class DealerShipViewSet(ModelViewSet):
    queryset = DealerShip.objects.all()
    serializer_class = DealerShipSerializer
    permission_classes = [IsAdminOrReadOnly]


class DealerViewset(ModelViewSet):
    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return AdminDealerSerializer
        return DealerSerializer


class ReviewViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(car_id=self.kwargs['car_pk'])

    def get_serializer_context(self):
        return {'car_id': self.kwargs['car_pk']}
