from .models import *
from rest_framework import serializers
from caruser.serializers import UserSerializer

# for all users


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ['title', 'country', 'since']

# for admin


class AdminCompanySerializer(serializers.ModelSerializer):
    cars = serializers.SerializerMethodField()

    def get_cars(self, company):
        return [car.title for car in company.cars.all()]

    class Meta:
        model = Company
        fields = '__all__'


# for dealer users
class DealerSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)

    def get_name(self, dealer):
        return f'{dealer.user.first_name} {dealer.user.last_name}'

    class Meta:
        model = Dealer
        fields = ['user_id', 'name', 'phone', 'personal_address']

# for admin


class AdminDealerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dealer
        fields = ['id', 'user_id', 'first_name', 'last_name',
                  'phone', 'personal_address']

# for annomous user


class CustomDealerSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)

    def get_name(self, dealer):
        return f'{dealer.user.first_name} {dealer.user.last_name}'

    class Meta:
        model = Dealer
        fields = ['name', 'phone']

# for all


class DealerShipSerializer(serializers.ModelSerializer):

    class Meta:
        model = DealerShip
        fields = "__all__"

# for all users


class CarWithDealerShipSerializer(serializers.ModelSerializer):
    dealership = DealerShipSerializer(read_only=True)

    class Meta:
        model = CarWithDealerShip
        fields = "__all__"

# for admin


class AdminCarWithDealerShipSerializer(serializers.ModelSerializer):
    dealership = DealerShipSerializer(many=True)

    class Meta:
        model = CarWithDealerShip
        fields = "__all__"

# for carowner users


class CarSerializer(serializers.ModelSerializer):
    owned_by = serializers.SerializerMethodField()
    company = CompanySerializer()

    def get_owned_by(self, car):
        user = self.context['request'].user
        return car.owned_by.user.username

    class Meta:
        model = CarWithOwnerShip
        fields = ['id', 'owned_by', 'title', 'company', 'registration_year', 'carmodel', 'color', 'mileage',
                  'description', 'fuel_type', 'ratings']

# custom mathod for creating car instance
# for carowner users


class CarCreateSerializer(serializers.ModelSerializer):
    company_title = serializers.SerializerMethodField()
    owned_by = serializers.SerializerMethodField(read_only=True)

    def get_company_title(self, car):
        return car.company.title

    def get_owned_by(self, car):
        user = self.context['request'].user

        return user.username

    class Meta:
        model = CarWithOwnerShip
        fields = ['id', 'owned_by', 'title',  'company', 'company_title', 'registration_year', 'carmodel', 'color', 'mileage',
                  'description', 'fuel_type', 'price', 'ratings']
        extra_kwargs = {
            'company': {'write_only': True},
        }

    def create(self, validated_data):
        user = self.context['request'].user
        owned_by, created = CarOwner.objects.get_or_create(user=user)
        validated_data.pop('owned_by', None)
        car = CarWithOwnerShip.objects.create(owned_by=owned_by, **validated_data)
        return car

# for admin


class AdminCarSerializer(serializers.ModelSerializer):

    carowner = serializers.SerializerMethodField()

    def get_carowner(self, car):

        return car.owned_by.user.username

    class Meta:
        model = CarWithOwnerShip
        fields = '__all__'

# created carowner details for annonymous user


class SimpleCarOwnerSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    def get_name(self, carowner):
        return f"{carowner.user.first_name} {carowner.user.last_name}"

    class Meta:
        model = CarOwner
        fields = ['name', 'phone', 'address']

# for annonymous user


class CustomeCarSerializer(serializers.ModelSerializer):

    company = CompanySerializer()
    owned_by = SimpleCarOwnerSerializer()

    class Meta:
        model = CarWithOwnerShip
        fields = ['id', 'owned_by', 'title', 'company', 'registration_year', 'carmodel', 'color', 'mileage',
                  'description', 'fuel_type', 'price', 'ratings']

# for all


class ReviewSerializer(serializers.ModelSerializer):
    car_title = serializers.SerializerMethodField(
        method_name='get_car_title', read_only=True)
    name = serializers.SerializerMethodField()

    def get_car_title(self, review):
        return review.car.title

    def get_name(self, review):
        car = review.car
        carowner = CarOwner.objects.only('user').get(car_owned=car)
        return carowner.user.username

    class Meta:
        model = Review
        fields = ['id', 'name', 'car_title', 'description']

    def create(self, validated_data):
        print(self.context)
        car_id = self.context.get('car_id')

        review = Review.objects.create(
            car_id=car_id,  **validated_data)
        return review

# for all


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'first_name', 'phone', 'address']

# for carowner users


class CarOwnerSerializer(serializers.ModelSerializer):
    my_cars = serializers.SerializerMethodField()
    car_count = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    def get_car_count(self, carowner):
        return carowner.car_owned.count()

    def get_my_cars(self, carowner):
        return [car.title for car in carowner.car_owned.all()]

    def get_name(self, carowner):
        return f"{carowner.user.first_name} {carowner.user.last_name}"

    class Meta:
        model = CarOwner
        fields = ['name',
                  'phone', 'address', 'car_count', 'my_cars']

# for admin


class AdminCarOwnerSerializer(serializers.ModelSerializer):
    car_owned = serializers.SerializerMethodField()

    def get_car_owned(self, carowner):
        return [car.title for car in carowner.car_owned.all()]

    class Meta:
        model = CarOwner
        fields = '__all__'
