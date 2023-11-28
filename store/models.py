from django.db import models

# Create your models here.


class Company(models.Model):
    title = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    since = models.IntegerField()


class Car(models.Model):
    TRANSMISSION_CHOICE = [('Autometic', 'Autometic'), ('Menual', 'Menual')]
    FUAL_CHOICE = [(
        'Petrol', 'Petrol'), ('Diesel', 'Diesel'), ('Electric', 'Electric'), ('CNG', 'CNG')]
    YEAR_CHOICE = [('2013', '2013'), ('2014', '2014'), ('2015', '2015'), ('2016', '2016'), ('2017', '2017'),
                   ('2018', '2018'), ('2019', '2019'), ('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023')]
    title = models.CharField(max_length=255)
    carmodel = models.CharField(max_length=50)
    color = models.CharField(max_length=20)
    registration_year = models.IntegerField(choices=YEAR_CHOICE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    mileage = models.IntegerField()
    fuel_type = models.CharField(max_length=20, choices=FUAL_CHOICE)
    transmission = models.CharField(
        max_length=255, choices=TRANSMISSION_CHOICE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    descriptioin = models.TextField(null=True)
    ratings = models.IntegerField()
    last_update = models.DateTimeField(auto_now_add=True)


class CarOwner(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.IntegerField()
    address = models.TextField()


class Customer(models.Model):
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.IntegerField()
    address = models.TextField()


class Dealer(models.Model):
    dealership_name = models.CharField(max_length=50)
    firstname = models.CharField(max_length=40)

    lastname = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.IntegerField()
    address = models.TextField()


class Review(models.Model):
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=40)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
