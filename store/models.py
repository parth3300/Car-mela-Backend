from django.db import models
from django.conf import settings
from django.urls import reverse
from cloudinary.models import CloudinaryField
from django.utils import timezone


class Company(models.Model):
    logo = CloudinaryField('image', null=True, blank=True)
    title = models.CharField(max_length=50)
    country = models.CharField(max_length=30)
    since = models.IntegerField()


    class Meta:
        ordering = ['-id'] 

    def __str__(self):
        return self.title


class Car(models.Model):
    FUEL_CHOICES = [('Petrol', 'Petrol'), ('Diesel', 'Diesel'),
                    ('Electric', 'Electric'), ('CNG', 'CNG')]
    YEAR_CHOICES = [(str(year), str(year)) for year in range(2000, 2030)]
    RATING_CHOICES = [('1', '1'), ('2', '2'), ('3', '3'),
                      ('4', '4'), ('5', '5')]

    title = models.CharField(max_length=20, null=True)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='cars', null=True, blank=True  
    )
    dealerships = models.ManyToManyField(
        'DealerShip', related_name='featured_cars'
    )

    # ✅ Replaced ImageField with CloudinaryField
    image = CloudinaryField('image', null=True, blank=True)

    carmodel = models.CharField(max_length=50)
    color = models.CharField(max_length=10)
    registration_year = models.CharField(max_length=10, choices=YEAR_CHOICES)
    fuel_type = models.CharField(max_length=10, choices=FUEL_CHOICES)
    mileage = models.IntegerField()
    description = models.TextField(null=True)
    price = models.BigIntegerField()
    ratings = models.CharField(max_length=5, choices=RATING_CHOICES)
    last_update = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-id'] 

    def __str__(self):
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
    dial_code = models.IntegerField(default= 91)
    phone_number = models.BigIntegerField()

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name


    class Meta:
        ordering = ['-id'] 

    def __str__(self):
        return self.user.username


class CarOwner(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    # ✅ Replaced ImageField with CloudinaryField
    profile_pic = CloudinaryField('image', null=True, blank=True)
    balance = models.BigIntegerField(default= 1000000)
    dial_code = models.IntegerField(default= 91)
    phone_number = models.BigIntegerField()

    @property
    def first_name(self):
        return self.user.first_name

    @property
    def last_name(self):
        return self.user.last_name


    class Meta:
        ordering = ['-id'] 

    def __str__(self):
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

    class Meta:
        ordering = ['-id'] 

    def __str__(self):
        return self.car.title


class DealerShip(models.Model):
    RATING_CHOICES = [('1', '1'), ('2', '2'), ('3', '3'),
                      ('4', '4'), ('5', '5')]
    dealership_name = models.CharField(max_length=50)
    dial_code = models.IntegerField(default= 91)
    phone_number = models.BigIntegerField()
    address = models.TextField()
    ratings = models.CharField(max_length=5, choices=RATING_CHOICES)


    class Meta:
        ordering = ['-id'] 

    def __str__(self):
        return self.dealership_name

    def get_absolute_info(self):
        return reverse('dealership-detail', args=[str(self.id)])


class Review(models.Model):
    RATING_CHOICES = [('1', '1'), ('2', '2'), ('3', '3'),
                      ('4', '4'), ('5', '5')]
    car = models.ForeignKey(
        Car, on_delete=models.CASCADE, related_name='reviews', null=True, blank=True
    )
    name = models.CharField(max_length=20, null=True, blank=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True
    )
    ratings = models.CharField(max_length=5, choices=RATING_CHOICES)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-id'] 

    def __str__(self):
        return f"Review for {self.car.title} by {self.name}"

from django.db import models
from django.conf import settings
from django.utils import timezone

class ChatSession(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    session_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Session {self.session_id} ({self.user or 'Anonymous'})"

class ChatMessage(models.Model):
    session = models.ForeignKey(
        ChatSession, 
        on_delete=models.CASCADE,
        related_name='messages'
    )
    message = models.TextField()
    is_bot = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
        verbose_name = 'Chat Message'
        verbose_name_plural = 'Chat Messages'

    def __str__(self):
        return f"{'Bot' if self.is_bot else 'User'}: {self.message[:50]}..."

class FAQ(models.Model):
    question = models.TextField(unique=True)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
        ordering = ['-created_at']

    def __str__(self):
        return f"FAQ: {self.question[:50]}..."
    
    question = models.TextField()
    answer = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"
        ordering = ['-created_at']

    def __str__(self):
        return self.question[:50] + "..." if len(self.question) > 50 else self.question