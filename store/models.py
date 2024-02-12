from django.db import models
from django.conf import settings
from django.urls import reverse


class Company(models.Model):
    logo = models.ImageField(upload_to='store/images')
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

    title = models.CharField(max_length=20, null=True)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='cars'
    )
    dealerships = models.ManyToManyField(
        'DealerShip', related_name='featured_cars'
    )
    image = models.ImageField(upload_to='store/images')

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

    def get_absolute_info(self):
        return reverse('car-detail', args=[str(self.id)])


class Customer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    contact = models.BigIntegerField()
    personal_address = models.TextField()

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    def __str__(self) -> str:
        return self.user.username


class CarOwner(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    profile_pic = models.ImageField(upload_to='store/images')
    contact = models.BigIntegerField()
    personal_address = models.TextField()

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name

    def __str__(self) -> str:
        return self.user.username

    def get_absolute_info(self):
        return reverse('carowner-detail', args=[str(self.id)])


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
    RATING_CHOICES = [('1', '1'), ('2', '2'), ('3', '3'),
                      ('4', '4'), ('5', '5')]
    dealership_name = models.CharField(max_length=50)
    contact = models.BigIntegerField()
    address = models.TextField()
    ratings = models.CharField(max_length=5, choices=RATING_CHOICES)

    def __str__(self) -> str:
        return self.dealership_name

    def get_absolute_info(self):
        return reverse('dealership-detail', args=[str(self.id)])


class Review(models.Model):
    RATING_CHOICES = [('1', '1'), ('2', '2'), ('3', '3'),
                      ('4', '4'), ('5', '5')]
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name='reviews'
    )
    name = models.CharField(max_length=20)
    ratings = models.CharField(max_length=5, choices=RATING_CHOICES)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Review for {self.car.title} by {self.name}"
