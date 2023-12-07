from django.contrib import admin
from .models import *
from django.contrib.contenttypes.admin import GenericStackedInline, GenericTabularInline


# Create your models here.


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'since', 'country']
    ordering = ['id']
    search_fields = ['title']


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'company', 'owned_by', 'carmodel', 'color', 'registration_year_display',
                    'mileage',  'fuel_type_display', 'price', 'last_update', 'ratings']
    list_per_page = 10
    ordering = ['id']
    search_fields = ['title']

    def registration_year_display(self, obj):
        return obj.get_registration_year_display()

    def fuel_type_display(self, obj):
        return obj.get_fuel_type_display()


class DealerShipForInline(GenericStackedInline):
    model = DealerShipFor
    extra = 1


@admin.register(CarWithDealerShip)
class CarWithDealerShipAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'company',  'carmodel', 'color', 'registration_year_display',
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
                    'last_name', 'phone', 'address']
    ordering = ['id']
    search_fields = ['user__first_name']


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


class CarInline(GenericStackedInline):
    model = Car


@admin.register(DealerShip)
class DealerShipAdmin(admin.ModelAdmin):
    list_display = ['id', 'dealership_name', 'address', 'phone', 'ratings']
    ordering = ['id']
    inlines = [CarInline]
