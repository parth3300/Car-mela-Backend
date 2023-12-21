from django.shortcuts import render
from .serializers import *
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import *
from rest_framework.mixins import RetrieveModelMixin
from .models import *
from rest_framework import permissions
from store.permissions import *
from django.contrib.auth.models import AnonymousUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from .filter import CarFilter
from rest_framework.filters import SearchFilter, OrderingFilter


class CarWithOwnerShipViewSet(ModelViewSet):

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = CarFilter
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'last_update']

    def get_permissions(self):
        if self.action == 'retrieve' and self.request.method == 'GET':
            return [IsAuthenticated()]
        return [IsAdminOrCarOwnerOrReadOnly()]

    def get_queryset(self):
        user = self.request.user

        if CarOwner.objects.filter(user_id=user.id).exists():
            carowner = CarOwner.objects.get(user=user)
            return CarWithOwnerShip.objects.filter(owned_by=carowner)
        return CarWithOwnerShip.objects.all()

    def get_serializer_class(self):
        user = self.request.user
        if user.is_staff:
            return AdminCarSerializer
        if CarOwner.objects.filter(user_id=user.id).exists():
            if self.request.method in ['POST', 'PUT', 'PATCH']:
                return CarCreateSerializer
            return CarSerializer

        return CustomeCarSerializer

    def create(self, request, *args, **kwargs):
        car_data = request.data.get('car', {})
        dealership_data_list = request.data.get('dealership', [])
        car_serializer = self.get_serializer(data=car_data)
        if car_serializer.is_valid():
            car_instance = car_serializer.save()
            for index, dealership_data in enumerate(dealership_data_list, start=1):
                dealership_data['content_type'] = 'car'
                dealership_data['object_id'] = car_instance.id

        return super().create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        car_data = request.data.get('car', {})
        dealership_data_list = request.data.getlist('dealership', [])

        car_serializer = self.get_serializer(data=car_data)
        if car_serializer.is_valid():
            car_instance = car_serializer.save()

            for index, dealership_data in enumerate(dealership_data_list, start=1):
                dealership_data['content_type'] = 'car'
                dealership_data['object_id'] = car_instance.id

                dealership_serializer = DealerShipSerializer(
                    data=dealership_data)
                if dealership_serializer.is_valid():
                    dealership_serializer.save()
                else:
                    # Rollback the created Car instance if DealerShip data is not valid
                    car_instance.delete()
                    return Response(dealership_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            car_serializer_data = car_serializer.data
            car_serializer_data['dealerships'] = DealerShipSerializer(
                car_instance.dealerships.all(), many=True).data

            return Response(car_serializer_data, status=status.HTTP_201_CREATED)

        return Response(car_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CarWithDealerShipViewSet(ModelViewSet):
    queryset = CarWithDealerShip.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):

        if self.request.user.is_staff:
            return AdminCarWithDealerShipSerializer

        return CarWithDealerShipSerializer


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAdminUser]


class ReviewViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(car_id=self.kwargs['car_pk'])

    def get_serializer_context(self):
        return {'car_id': self.kwargs['car_pk']}


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]


class DealerViewset(ModelViewSet):
    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer

    def get_view_name(self):
        return "Dealer List"

    def get_permissions(self):
        if self.action == 'retrieve':
            return [IsAdminUser()]
        return [IsAdminOrReadOnly()]

    def get_serializer_class(self):
        user = self.request.user

        if Dealer.objects.filter(user_id=user.id).exists():
            return DealerSerializer
        elif self.request.user.is_staff:
            return AdminDealerSerializer

        return CustomDealerSerializer

    # @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    # def me(self, request):
    #     dealer = Dealer.objects.get(user_id=request.user.id)

    #     if request.method == 'GET':
    #         serializer = CarOwnerSerializer(dealer)
    #         return Response(serializer.data)
    #     elif request.method == 'PUT':
    #         serializer = CarOwnerSerializer(dealer, data=request.data)
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(serializer.data)


class CarOwnerViewset(ModelViewSet):
    queryset = CarOwner.objects.all()

    def get_view_name(self):
        return "Car Owner  List"

    def get_permissions(self):

        if self.action == 'retrieve':
            return [IsAdminUser()]
        elif self.request.method == 'GET':
            return [AllowAny()]
        return [IsAdminOrReadOnly()]

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
