from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from .models import *
from django.contrib.contenttypes.admin import GenericStackedInline, GenericTabularInline
from django.urls import reverse
from django.utils.html import format_html, urlencode
from django.db.models.aggregates import Count
from . import models


# Create your models here.

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'since', 'country', 'listed_cars']
    ordering = ['id']
    search_fields = ['title']

    def listed_cars(self, company):
        cars = company.cars.all()
        car_titles = ', '.join(str(car) for car in cars)
        return car_titles


class PriceFilter(admin.SimpleListFilter):
    title = 'Price'
    parameter_name = 'price'

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return [
            ('<500000', 'less than 500000'),
            ('>500000', 'more than 500000'),
        ]

    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == '<500000':
            return queryset.filter(price__lt=500000)
        elif self.value() == '>500000':
            return queryset.filter(price__gt=500000)


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'company', 'carmodel', 'color', 'registration_year',
                    'fuel_type', 'mileage',  'price', 'last_update', 'ratings', 'carowner']
    ordering = ['id']
    search_fields = ['title']
    list_per_page = 10
    list_filter = [PriceFilter, 'car_ownership__carowner']


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name',
                    'last_name', 'phone', 'personal_address']
    ordering = ['id']
    search_fields = ['user_first_name', 'phone', 'personal_address']


@admin.register(models.CarOwner)
class CarOwnerAdmin(admin.ModelAdmin):

    list_display = ['id', 'user', 'user_details', 'first_name',
                    'last_name', 'cars_count', 'phone', 'personal_address',]
    ordering = ['id']
    search_fields = ['user__first_name', 'phone', 'personal_address']
    list_filter = ['user']

    @admin.display(ordering='cars_count')
    def cars_count(self, carowner):
        url = reverse('admin:store_carownership_changelist')
        return format_html('<a href="{}?carowner__id__exact={}">{} - View all</a>', url, carowner.id, carowner.cars_count)

    def user_details(self, carowner):
        url = reverse('admin:caruser_user_changelist')
        return format_html('<a href="{}?id__exact={}">View details</a>', url, carowner.user.id)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            cars_count=Count('cars_owned')
        )


@admin.register(CarOwnerShip)
class CarOwnerShipAdmin(admin.ModelAdmin):
    list_display = ['id', 'car', 'car_details', 'carowner', 'carowner_details']
    ordering = ['id']
    list_filter = ['carowner']

    def car_details(self, car_ownership):
        url = reverse('admin:store_car_changelist')
        return format_html('<a href="{}?car_ownership__carowner__id__exact={}">View details</a>', url, car_ownership.carowner.id)

    def carowner_details(self, car_ownership):
        url = reverse('admin:store_carowner_changelist')
        return format_html('<a href="{}?id__exact={}">View details</a>', url, car_ownership.carowner.id)


@admin.register(DealerShip)
class DealerShipAdmin(admin.ModelAdmin):
    list_display = ['id', 'dealership_name',
                    'display_cars', 'address', 'phone', 'ratings']
    ordering = ['id']
    search_fields = ['dealership_name']

    def display_cars(self, dealership):
        return ', '.join([car.title for car in dealership.cars.all()])
    display_cars.short_description = 'Cars'

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            cars_count=Count('cars_at_dealership')
        )


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name',
                    'last_name', 'dealership', 'phone', 'personal_address']
    ordering = ['id']
    search_fields = ['user_first_name', 'phone', 'personal_address']
