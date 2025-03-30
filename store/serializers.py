from rest_framework import serializers
from caruser.serializers import UserSerializer
from .models import *
from django.urls import reverse


class CompanySerializer(serializers.ModelSerializer):
    logo = serializers.ImageField(required=False)  # Handles uploads
    cars_count = serializers.SerializerMethodField()
    listed_cars = serializers.SerializerMethodField()
    view_cars = serializers.SerializerMethodField()

    def get_cars_count(self, company):
        return company.cars.count()

    def get_listed_cars(self, company):
        listed_cars = []
        for car in company.cars.all():
            car_data = {
                'title': car.title,
                'id': car.id,
                'carowner_user_id': None  # Default value if any related field is None
            }
            if hasattr(car, 'car_ownership') and hasattr(car.car_ownership, 'carowner') and hasattr(car.car_ownership.carowner, 'user'):
                car_data['carowner_user_id'] = car.car_ownership.carowner.user.id
            listed_cars.append(car_data)
        return listed_cars
    def get_view_cars(self, company):
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/store/cars/?company_id={company.id}')
        return f'/store/cars/?company_id={company.id}'

    class Meta:
        model = Company
        fields = [
            'id',
            'logo',
            'title',
            'country',
            'since',
            'cars_count',
            'listed_cars',
            'view_cars'
        ]


class CarSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)  # Handles uploads
    dealerships = serializers.SerializerMethodField()
    carowner = serializers.SerializerMethodField()
    company_title = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    
    def get_dealerships(self, car):
        dealerships = car.dealerships.all()
        request = self.context.get('request')
        return [
            {
                'id': dealership.id,
                'name': dealership.dealership_name,
                'ratings': dealership.ratings,
                'view_details': request.build_absolute_uri(dealership.get_absolute_info()) if request else dealership.get_absolute_info()
            }
            for dealership in dealerships
        ]

    def get_carowner(self, car):
        request = self.context.get('request')
        try:
            car_ownership = car.car_ownership
            return {
                'name': car_ownership.carowner.user.username,
                'user_id': car_ownership.carowner.user.id,
                'view_details': request.build_absolute_uri(car_ownership.carowner.get_absolute_info()) if request else car_ownership.carowner.get_absolute_info()
            }
        except CarOwnerShip.DoesNotExist:
            return None

    def get_company_title(self, car):
        return car.company.title if car.company else None

    def get_reviews(self, car):
        return [
            {
                'name': review.name,
                'ratings': review.ratings,
                'description': review.description
            }
            for review in car.reviews.all()
        ]

    def get_average_rating(self, car):
        reviews = car.reviews.all()
        
        if not reviews:
            avg_rating = float(car.ratings) if car.ratings else 0.0
        else:
            total_rating = sum(float(review.ratings) for review in reviews)
            car_rating = float(car.ratings) if car.ratings else 0.0
            
            avg_rating = (total_rating + car_rating) / (reviews.count() + 1)

        avg_rating = round(avg_rating)

        ratings_list = [float(review.ratings) for review in reviews]

        return avg_rating

        

    class Meta:
        model = Car
        fields = [
            'id',
            'title',
            'company',
            'company_title',
            'image',
            'dealerships',
            'carmodel',
            'color',
            'registration_year',
            'fuel_type',
            'mileage',
            'description',
            'price',
            'ratings',
            'last_update',
            'carowner',
            'reviews',
            'average_rating'
        ]


class CustomerSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    def get_name(self, customer):
        return f'{customer.user.first_name} {customer.user.last_name}'

    def get_email(self, customer):
        return customer.user.email

    class Meta:
        model = Customer
        fields = ['id', 'name', 'dial_code', 'phone_number', 'email']


class CarOwnerSerializer(serializers.ModelSerializer):
    profile_pic = serializers.ImageField(required=False)  # Handles uploads
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
        return [carownership.car.title
            for carownership in carowner.cars_owned.all()
        ]

    def get_view_cars(self, carowner):
        request = self.context.get('request')
        url = reverse('car-list')
        if request:
            return request.build_absolute_uri(f'{url}?car_ownership__carowner__id={carowner.id}')
        return f'{url}?car_ownership__carowner__id={carowner.id}'

    class Meta:
        model = CarOwner
        fields = [
            'id',
            'name',
            "user",
            'profile_pic',
            'balance',
            'cars_count',
            'cars',
            'view_cars',
            'dial_code', 'phone_number',
            'email'
        ]


class AdminCarOwnerSerializer(CarOwnerSerializer):
    class Meta(CarOwnerSerializer.Meta):
        fields = [
            'id',
            'name',
            'profile_pic',
            'cars',
            'cars_count',
            'view_cars',
            'dial_code', 'phone_number',
            'email'
        ]


class CarOwnerShipSerializer(serializers.ModelSerializer):
    car_detail = serializers.SerializerMethodField()
    carowner_detail = serializers.SerializerMethodField()


    def get_car_detail(self, carownership):
        car = carownership.car
        request = self.context.get('request')
        return {
            'title': car.title,
            'price': car.price,
            'view_details': request.build_absolute_uri(car.get_absolute_info()) if request else car.get_absolute_info()
        }

    def get_carowner_detail(self, carownership):
        carowner = carownership.carowner
        request = self.context.get('request')
        return {
            'name': carowner.user.username,
            'cars': carowner.cars_owned.count(),
            'view_details': request.build_absolute_uri(carowner.get_absolute_info()) if request else carowner.get_absolute_info()
        }

    class Meta:
        model = CarOwnerShip
        fields = ['id','car', 'carowner', 'car_detail', 'carowner_detail']


class DealerShipSerializer(serializers.ModelSerializer):
    featured_cars = serializers.SerializerMethodField()

    def get_featured_cars(self, dealership):
        featured_cars = dealership.featured_cars.all()
        request = self.context.get('request')
        return [
            {
                'title': featured_car.title,
                'price': featured_car.price,
                'view_details': request.build_absolute_uri(featured_car.get_absolute_info()) if request else featured_car.get_absolute_info()
            }
            for featured_car in featured_cars
        ]

    class Meta:
        model = DealerShip
        fields = [
            'id',
            'dealership_name',
            'featured_cars',
            'dial_code', 'phone_number',
            'address',
            'ratings'
        ]


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    
    def get_user_name(self, review):
        # If review.user exists and has a first name, use it. Otherwise, use review.name.
        full_name = f"{review.user.first_name} {review.user.last_name}" if review.user else ""
        return full_name.strip() or review.name
    class Meta:
        model = Review
        fields = ['id', 'car', 'user', 'user_name', 'name', 'ratings', 'description', 'date']



class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']