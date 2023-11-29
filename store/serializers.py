from .models import *
from rest_framework import serializers


class CompanySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Company
        fields = ['id', 'title', 'country', 'since']


class CarSerializer(serializers.ModelSerializer):
    company_url = serializers.HyperlinkedRelatedField(
        view_name='company-detail', read_only=True, source='company')
    company_title = serializers.CharField(
        source='company.title', read_only=True)

    class Meta:
        model = Car
        fields = ['id', 'title', 'company_title', 'company_url', 'carmodel', 'color', 'mileage',
                  'description', 'transmission', 'fuel_type', 'price', 'ratings']


class ReviewSerializer(serializers.ModelSerializer):
    car_title = serializers.SerializerMethodField(
        method_name='get_car_title', read_only=True)

    def get_car_title(self, request):
        return request.car.title

    class Meta:
        model = Review
        fields = ['id', 'name', 'description', 'car_title']

    def create(self, validated_data):
        car_id = self.context['car_id']
        return Review.objects.create(car_id=car_id, **validated_data)
