from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from .models import *
from django.contrib.contenttypes.admin import GenericStackedInline, GenericTabularInline
from django.urls import reverse
from django.utils.html import format_html, urlencode
from django.db.models.aggregates import Count


# Create your models here.


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'since', 'country']
    ordering = ['id']
    search_fields = ['title']


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


@admin.register(CarWithOwnerShip)
class CarWithOwneshipAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'company', 'owned_by', 'carmodel', 'color', 'registration_year_display',
                    'mileage',  'fuel_type_display', 'price', 'last_update', 'ratings']
    ordering = ['id']
    search_fields = ['title']
    list_filter = ['owned_by', PriceFilter]

    def registration_year_display(self, obj):
        return obj.get_registration_year_display()

    def fuel_type_display(self, obj):
        return obj.get_fuel_type_display()


class DealerShipForInline(GenericStackedInline):
    model = DealerShipFor
    extra = 1


@admin.register(CarWithDealerShip)
class CarWithDealerShipAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'company', 'carmodel', 'color', 'registration_year_display',
                    'mileage', 'fuel_type_display', 'price', 'last_update', 'ratings']
    list_per_page = 10
    ordering = ['id']
    search_fields = ['title']
    inlines = [DealerShipForInline]

    def registration_year_display(self, obj):
        return obj.get_registration_year_display()

    def fuel_type_display(self, obj):
        return obj.get_fuel_type_display()


@admin.register(CarOwner)
class CarOwnerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name',
                    'last_name', 'phone', 'address', 'cars_count']
    ordering = ['id']
    search_fields = ['user__first_name']

    @admin.display(ordering='cars_count')
    def cars_count(self, carowner):
        url = reverse('admin:store_carwithownership_changelist')
        return format_html('<a href="{}?owned_by__id__exact={}">{}</a>', url, carowner.id, carowner.cars_count)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            cars_count=Count('car_owned')
        )


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name',
                    'last_name', 'phone', 'address']
    ordering = ['id']
    search_fields = ['user_first_name']


@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'dealership', 'first_name',
                    'last_name', 'phone',  'personal_address']
    ordering = ['id']
    search_fields = ['user_first_name']

# @admin.register(review)
# class ReviewAdmin(admin.ModelAdmin):


@admin.register(DealerShip)
class DealerShipAdmin(admin.ModelAdmin):
    list_display = ['id', 'dealership_name', 'address', 'phone', 'ratings']
    ordering = ['id']
