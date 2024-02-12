from rest_framework import serializers
from caruser.serializers import UserSerializer
from .models import *
from django.utils.html import format_html, urlencode


class CompanySerializer(serializers.ModelSerializer):
    cars_count = serializers.SerializerMethodField()
    listed_cars = serializers.SerializerMethodField()
    view_cars = serializers.SerializerMethodField()

    def get_cars_count(self, company):
        return company.cars.count()

    def get_listed_cars(self, company):
        return [{'title': car.title, 'id': car.id} for car in company.cars.all()]

    def get_view_cars(self, company):
        return self.context['request'].build_absolute_uri(f'/store/cars/?company_id={company.id}')

    class Meta:
        model = Company
        fields = ['id', 'logo', 'title', 'country',
                  'since', 'cars_count', 'listed_cars', 'view_cars']


class CarSerializer(serializers.ModelSerializer):
    dealerships = serializers.SerializerMethodField()
    carowner = serializers.SerializerMethodField()
    company = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    def get_dealerships(self, car):
        dealerships = car.dealerships.all()
        return [
            {
                'id': dealership.id,
                'name': dealership.dealership_name,
                'ratings': dealership.ratings,
                'view_details': self.context['request'].build_absolute_uri(dealership.get_absolute_info())
            }
            for dealership in dealerships
        ]

    def get_carowner(self, car):
        try:
            car_ownership = car.car_ownership
            return {
                'name': car_ownership.carowner.user.username,
                'view_detials': self.context['request'].build_absolute_uri(car_ownership.carowner.get_absolute_info())}
        except CarOwnerShip.DoesNotExist:
            return None

    def get_company(self, car):
        return car.company.title

    def get_reviews(self, car):
        return [{'name': review.name, 'ratings': review.ratings, 'description': review.description} for review in car.reviews.all()]

    class Meta:
        model = Car
        fields = ['id', 'title', 'company', 'image', 'dealerships', 'carmodel', 'color', 'registration_year',
                  'fuel_type', 'mileage', 'description', 'price', 'ratings', 'last_update', 'carowner','reviews']


class CustomerSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    def get_name(self, carowner):
        return f'{carowner.user.first_name} {carowner.user.last_name}'

    def get_email(self, carowner):
        return carowner.user.email

    class Meta:
        model = Customer
        fields = ['id', 'name', 'contact', 'personal_address']


class CarOwnerSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    cars_count = serializers.SerializerMethodField()
    cars = serializers.SerializerMethodField()
    view_cars = serializers.SerializerMethodField()

    def get_name(self, carowner):
        return f'{carowner.user.first_name} {carowner.user.last_name}'

    def get_email(self, carowner):
        return carowner.user.email

    def get_cars_count(self, carowner):
        return carowner.cars_owned.count()

    def get_cars(self, carowner):
        return [{'id': carownership.car.id, 'title': carownership.car.title} for carownership in carowner.cars_owned.all()]

    def get_view_cars(self, carowner):
        url = reverse('car-list')
        return self.context['request'].build_absolute_uri(f'{url}?car_ownership__carowner__id={carowner.id}')

    class Meta:
        model = CarOwner
        fields = ['id', 'name', 'profile_pic', 'cars_count', 'cars',
                  'view_cars', 'contact', 'email']


class AdminCarOwnerSerializer(CarOwnerSerializer):
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    cars_count = serializers.SerializerMethodField()
    cars = serializers.SerializerMethodField()
    view_cars = serializers.SerializerMethodField()

    def get_name(self, carowner):
        return f'{carowner.user.first_name} {carowner.user.last_name}'

    def get_email(self, carowner):
        return carowner.user.email

    def get_cars_count(self, carowner):
        return carowner.cars_owned.count()

    def get_cars(self, carowner):
        return [{'id': carownership.car.id, 'title': carownership.car.title} for carownership in carowner.cars_owned.all()]

    def get_view_cars(self, carowner):
        url = reverse('car-list')
        return self.context['request'].build_absolute_uri(f'{url}?car_ownership__carowner__id={carowner.id}')

    class Meta:
        model = CarOwner
        fields = ['id', 'name', 'profile_pic', 'cars', 'cars_count',
                  'view_cars', 'contact', 'email', 'personal_address']


class CarOwnerShipSerializer(serializers.ModelSerializer):
    car = serializers.SerializerMethodField()
    carowner = serializers.SerializerMethodField()

    def get_car(self, carownership):
        car = carownership.car
        return {
            'title': car.title,
            'price': car.price,
            'view_details': self.context['request'].build_absolute_uri(car.get_absolute_info())
        }

    def get_carowner(self, carownership):
        carowner = carownership.carowner
        return {
            'name': carowner.user.username,
            'cars': carowner.cars_owned.count(),
            'view_details': self.context['request'].build_absolute_uri(carowner.get_absolute_info())
        }

    class Meta:
        model = CarOwnerShip
        fields = ['id', 'car', 'carowner']


class DealerShipSerializer(serializers.ModelSerializer):
    featured_cars = serializers.SerializerMethodField()

    def get_featured_cars(self, dealership):
        featured_cars = dealership.featured_cars.all()
        
        return  ([

            {
                'title': featured_car.title,
                'price': featured_car.price,
                'view_details': self.context['request'].build_absolute_uri(featured_car.get_absolute_info())
            }
            for featured_car in featured_cars

        ])

    class Meta:
        model = DealerShip
        fields = ['id', 'dealership_name',
                  'featured_cars', 'contact', 'address', 'ratings']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id',  'name', 'ratings', 'description', 'date']
