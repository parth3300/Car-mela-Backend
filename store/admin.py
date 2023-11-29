from django.contrib import admin
from . import models


# Create your models here.


@admin.register(models.Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'since', 'country']
    ordering = ['id']
    search_fields = ['title']


@admin.register(models.Car)
# class CarAdmin(admin.ModelAdmin):
#     list_display = ['id', 'title', 'company', 'carmodel', 'color', 'registration_year',
#                     'mileage', 'transmission', 'ratings', 'price', 'fuel_type', 'last_update']
#     list_per_page = 10
#     ordering = ['id']
#     search_fields = ['title']
class CarAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'company', 'carmodel', 'color', 'registration_year_display',
                    'mileage', 'transmission_display', 'ratings', 'price', 'fuel_type_display', 'last_update']
    list_per_page = 10
    ordering = ['id']
    search_fields = ['title']

    def registration_year_display(self, obj):
        return obj.get_registration_year_display()

    def transmission_display(self, obj):
        return obj.get_transmission_display()

    def fuel_type_display(self, obj):
        return obj.get_fuel_type_display()


@admin.register(models.CarOwner)
class CarOwnerAdmin(admin.ModelAdmin):

    list_display = ['id', 'user', 'first_name',
                    'last_name', 'phone', 'address']
    search_fields = ['user__first_name']


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name',
                    'last_name', 'phone', 'address']
    search_fields = ['user_first_name']


@admin.register(models.Dealer)
class DealerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name',
                    'last_name', 'dealership_name', 'phone', 'address']
    search_fields = ['user_first_name']

# @admin.register(models.review)
# class ReviewAdmin(admin.ModelAdmin):
