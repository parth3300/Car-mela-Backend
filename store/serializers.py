from rest_framework import serializers
from caruser.serializers import UserSerializer
from .models import Company, Car, Customer, CarOwner, CarOwnerShip, DealerShip, Dealer, Review
from django.urls import reverse


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'title', 'country', 'since']


class AdminCompanySerializer(serializers.ModelSerializer):
    cars_count = serializers.SerializerMethodField()
    cars = serializers.SerializerMethodField()

    def get_cars_count(self, company):
        return company.cars.count()

    def get_cars(self, company):
        return [car.title for car in company.cars.all()]

    class Meta:
        model = Company
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    carowner = serializers.SerializerMethodField(read_only=True)
    dealership = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Car
        fields = ['id', 'title', 'company', 'carmodel', 'color', 'registration_year', 'fuel_type',
                  'mileage', 'description', 'price', 'ratings', 'dealership', 'carowner']

    def get_carowner(self, car):
        try:
            car_ownership = car.car_ownership
            return car_ownership.carowner.user.username if car_ownership else None
        except CarOwnerShip.DoesNotExist:
            return 'Not Owned'


class CustomerSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)

    def get_name(self, customer):
        return f'{customer.user.username} {customer.user.last_name}'

    class Meta:
        model = Customer
        fields = ['id', 'name', 'phone', 'personal_address']


class CarOwnerSerializer(serializers.ModelSerializer):
    my_cars = serializers.SerializerMethodField()
    cars_count = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField(read_only=True)

    def get_cars_count(self, carowner):
        return carowner.cars_owned.count()

    def get_my_cars(self, carowner):
        return [carownership.car.title for carownership in carowner.cars_owned.all()]

    def get_name(self, carowner):
        return f'{carowner.user.username}'

    class Meta:
        model = CarOwner
        fields = ['id', 'name', 'cars_count', 'my_cars', 'phone']


class AdminCarOwnerSerializer(serializers.ModelSerializer):
    cars_owned = serializers.SerializerMethodField()
    cars_count = serializers.SerializerMethodField()

    def get_cars_count(self, carowner):
        return carowner.cars_owned.count()

    def get_cars_owned(self, carowner):
        return [carownership.car.title for carownership in carowner.cars_owned.all()]

    class Meta:
        model = CarOwner
        fields = '__all__'


class CarOwnerShipSerializer(serializers.ModelSerializer):
    car_details = serializers.HyperlinkedRelatedField(
        view_name='car-detail', source='car', read_only=True)
    carowner_details = serializers.HyperlinkedRelatedField(
        view_name='carowner-detail', source='carowner', read_only=True)

    class Meta:
        model = CarOwnerShip
        fields = ['id', 'car', 'car_details', 'carowner', 'carowner_details']



class SimpleCarSerializer(serializers.Serializer):
    class Meta:
        model = Car
        fields = ['title']


class DealerShipSerializer(serializers.ModelSerializer):
    cars_count = serializers.SerializerMethodField(read_only=True)
    cars_info = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = DealerShip
        fields = ['id', 'dealership_name', 'cars_count',
                  'cars_info', 'address', 'ratings', 'phone']

    def get_cars_count(self, dealership):
        return dealership.cars.count()

    def get_cars_info(self, dealership):
        # Combine car title and details into a single string
        return [{'title': car.title, 'details': self.context['request'].build_absolute_uri(reverse('car-detail', args=[car.pk]))} for car in dealership.cars.all()]


class DealerSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)

    def get_name(self, dealer):
        return f'{dealer.user.username}'

    class Meta:
        model = Dealer
        fields = ['id', 'name', 'dealership', 'phone']


class AdminDealerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealer
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    car_title = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    def get_car_title(self, review):
        return review.car.title

    def get_name(self, review):
        car = review.car
        carowner = CarOwner.objects.only('user').get(cars_owned=car)
        return carowner.user.username

    class Meta:
        model = Review
        fields = ['id', 'name', 'car_title', 'description']

    def create(self, validated_data):
        car_id = self.context.get('car_id')
        review = Review.objects.create(car_id=car_id, **validated_data)
        return review
