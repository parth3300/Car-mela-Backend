from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

# Create your models here.


class Company(models.Model):
    title = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    since = models.IntegerField()

    def __str__(self) -> str:
        return self.title


class CarOwner(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    phone = models.BigIntegerField()
    address = models.TextField()

    def __str__(self) -> str:
        return self.user.username

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name


class Customer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    phone = models.BigIntegerField()
    address = models.TextField()

    def __str__(self) -> str:
        return self.user.username

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name


#  for reloading queries/ to  user manage item in database


class DealerShipManager(models.Manager):
    def get_dealerships_for(self, obj_type, obj_id):
        return self.objects.select_related('dealers').filter(
            content_type=obj_type, object_id=obj_id)


class DealerShip(models.Model):
    RATING_CHOICES = [('1', '1'), ('2', '2'), ('3', '3'),
                      ('4', '4'), ('5', '5')]
    dealership_name = models.CharField(max_length=50)
    address = models.TextField()
    ratings = models.CharField(max_length=5, choices=RATING_CHOICES)
    phone = models.BigIntegerField()

    def __str__(self) -> str:
        return self.dealership_name


class Dealer(models.Model):
    dealership = models.ForeignKey(
        DealerShip, on_delete=models.CASCADE, related_name='dealers')

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    personal_address = models.TextField()
    phone = models.BigIntegerField()

    def __str__(self) -> str:
        return self.user.username

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name


class DealerShipFor(models.Model):
    objects = DealerShipManager()
    dealership = models.ForeignKey(DealerShip, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


class Car(models.Model):
    FUEL_CHOICE = [('Petrol', 'Petrol'), ('Diesel', 'Diesel'),
                   ('Electric', 'Electric'), ('CNG', 'CNG')]
    YEAR_CHOICES = [(str(year), str(year)) for year in range(2013, 2024)]
    RATING_CHOICES = [('1', '1'), ('2', '2'), ('3', '3'),
                      ('4', '4'), ('5', '5')]

    title = models.CharField(max_length=255)
    # this forignkey access  to carowner table, carowned access to Car table
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='cars')
    owned_by = models.ForeignKey(
        CarOwner, on_delete=models.CASCADE, related_name='car_owned')
    # many to many relationship eg in showroom many cars and one car in many show room
    carmodel = models.CharField(max_length=50)
    color = models.CharField(max_length=20)
    registration_year = models.CharField(max_length=50, choices=YEAR_CHOICES)
    mileage = models.IntegerField()
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICE)

    description = models.TextField(null=True)
    ratings = models.CharField(max_length=5, choices=RATING_CHOICES)
    last_update = models.DateTimeField(auto_now_add=True)
    price = models.BigIntegerField()

    def __str__(self) -> str:
        return self.title


class CarWithDealerShip(models.Model):
    FUEL_CHOICE = [('Petrol', 'Petrol'), ('Diesel', 'Diesel'),
                   ('Electric', 'Electric'), ('CNG', 'CNG')]
    YEAR_CHOICES = [(str(year), str(year)) for year in range(2013, 2024)]
    RATING_CHOICES = [('1', '1'), ('2', '2'), ('3', '3'),
                      ('4', '4'), ('5', '5')]

    title = models.CharField(max_length=255)
    # this forignkey access  to carowner table, carowned access to Car table
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='carswithdealership')

    carmodel = models.CharField(max_length=50)
    color = models.CharField(max_length=20)
    registration_year = models.CharField(max_length=50, choices=YEAR_CHOICES)
    mileage = models.IntegerField()
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICE)

    description = models.TextField(null=True)
    ratings = models.CharField(max_length=5, choices=RATING_CHOICES)
    last_update = models.DateTimeField(auto_now_add=True)
    price = models.BigIntegerField()

    def __str__(self) -> str:
        return self.title


class Review(models.Model):
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=40)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
