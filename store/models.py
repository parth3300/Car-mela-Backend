from django.db import models
from django.conf import settings


class Company(models.Model):
    title = models.CharField(max_length=50)
    country = models.CharField(max_length=30)
    since = models.IntegerField()

    def __str__(self) -> str:
        return self.title


class Car(models.Model):
    FUEL_CHOICES = [('Petrol', 'Petrol'), ('Diesel', 'Diesel'),
                    ('Electric', 'Electric'), ('CNG', 'CNG')]
    YEAR_CHOICES = [(str(year), str(year)) for year in range(2013, 2024)]
    RATING_CHOICES = [('1', '1'), ('2', '2'), ('3', '3'),
                      ('4', '4'), ('5', '5')]

    title = models.CharField(max_length=20)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='cars'
    )
    dealerships = models.ManyToManyField(
        'DealerShip', related_name='cars_at_dealership'
    )
    carmodel = models.CharField(max_length=50)
    color = models.CharField(max_length=10)
    registration_year = models.CharField(max_length=10, choices=YEAR_CHOICES)
    fuel_type = models.CharField(max_length=10, choices=FUEL_CHOICES)
    mileage = models.IntegerField()
    description = models.TextField(null=True)
    price = models.BigIntegerField()
    ratings = models.CharField(max_length=5, choices=RATING_CHOICES)
    last_update = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

    @property
    def carowner(self):
        return (
            self.car_ownership.carowner.user.username
            if hasattr(self, 'car_ownership')
            else None
        )

    # Note: Removed the dealership property to avoid circular reference


class Customer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    phone = models.BigIntegerField()
    personal_address = models.TextField()

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name

    def __str__(self) -> str:
        return self.user.first_name


class CarOwner(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    phone = models.BigIntegerField()
    personal_address = models.TextField()

    def __str__(self) -> str:
        return self.user.first_name

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name


class CarOwnerShip(models.Model):
    car = models.OneToOneField(
        Car, on_delete=models.CASCADE, related_name='car_ownership'
    )
    carowner = models.ForeignKey(
        CarOwner, on_delete=models.CASCADE, related_name='cars_owned'
    )

    def __str__(self) -> str:
        return self.car.title


class DealerShip(models.Model):
    featured_car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name='featured_at_dealership', null=True, blank=True
    )
    RATING_CHOICES = [('1', '1'), ('2', '2'), ('3', '3'),
                      ('4', '4'), ('5', '5')]
    dealership_name = models.CharField(max_length=50)
    phone = models.BigIntegerField()
    address = models.TextField()
    ratings = models.CharField(max_length=5, choices=RATING_CHOICES)
    # Removed the extra cars field here

    def __str__(self) -> str:
        return self.dealership_name


class Dealer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    dealership = models.ForeignKey(
        DealerShip, on_delete=models.CASCADE, related_name='dealers'
    )
    phone = models.BigIntegerField()
    personal_address = models.TextField()

    def __str__(self) -> str:
        return self.user.first_name

    def first_name(self):
        return self.user.first_name

    def last_name(self):
        return self.user.last_name


class Review(models.Model):
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name='reviews'
    )
    name = models.CharField(max_length=20)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Review for {self.car.title} by {self.name}"
