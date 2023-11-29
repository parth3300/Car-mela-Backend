from django.db import models
from django.conf import settings

# Create your models here.


class Company(models.Model):
    title = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    since = models.IntegerField()


class Car(models.Model):
    TRANSMISSION_CHOICE = [('Automatic', 'Automatic'), ('Manual', 'Manual')]
    FUEL_CHOICE = [('Petrol', 'Petrol'), ('Diesel', 'Diesel'),
                   ('Electric', 'Electric'), ('CNG', 'CNG')]
    YEAR_CHOICES = [(str(year), str(year)) for year in range(2013, 2024)]

    title = models.CharField(max_length=255)
    carmodel = models.CharField(max_length=50)
    color = models.CharField(max_length=20)
    registration_year = models.CharField(max_length=50, choices=YEAR_CHOICES)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    mileage = models.IntegerField()
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICE)
    transmission = models.CharField(
        max_length=255, choices=TRANSMISSION_CHOICE, default='Automatic')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True)
    ratings = models.IntegerField()
    last_update = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class CarOwner(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    phone = models.IntegerField()
    address = models.TextField()

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name


class Customer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    phone = models.IntegerField()
    address = models.TextField()

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name


class Dealer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    dealership_name = models.CharField(max_length=50)
    address = models.TextField()
    phone = models.DecimalField(max_digits=12, decimal_places=0)

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name


class Review(models.Model):
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=40)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
