from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class User(AbstractUser):
    is_customer = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    phone = models.CharField(max_length=15, blank=True)
    
    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    mobile_number = models.CharField(max_length=15)
    email_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_created_at = models.DateTimeField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - Profile"


class Country(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='cities')
    
    def __str__(self):
        return f"{self.name}, {self.country.name}"


class TouristPlace(models.Model):
    name = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='tourist_places')
    description = models.TextField()
    image = models.ImageField(upload_to='tourist_places/', blank=True, null=True)
    entry_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    def __str__(self):
        return self.name


class VehicleType(models.TextChoices):
    TRAIN = 'Train', 'Train'
    CAR = 'Car', 'Car'
    BUS = 'Bus', 'Bus'
    FLIGHT = 'Flight', 'Flight'


class Vehicle(models.Model):
    vehicle_type = models.CharField(max_length=20, choices=VehicleType.choices)
    name = models.CharField(max_length=100)
    price_per_km = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)
    image = models.ImageField(upload_to='vehicles/', blank=True, null=True)
    capacity = models.IntegerField(default=4)
    
    def __str__(self):
        return f"{self.name} ({self.vehicle_type})"


class HotelType(models.TextChoices):
    HOTEL = 'Hotel', 'Hotel'
    LODGE = 'Lodge', 'Lodge'
    RESORT = 'Resort', 'Resort'


class Hotel(models.Model):
    name = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='hotels')
    hotel_type = models.CharField(max_length=20, choices=HotelType.choices)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    image = models.ImageField(upload_to='hotels/', blank=True, null=True)
    description = models.TextField(blank=True)
    amenities = models.TextField(blank=True)
    availability = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - {self.city.name}"


class Restaurant(models.Model):
    name = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='restaurants')
    price_range = models.CharField(max_length=50)
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    image = models.ImageField(upload_to='restaurants/', blank=True, null=True)
    description = models.TextField(blank=True)
    cuisine_type = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return f"{self.name} - {self.city.name}"


class TourPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tour_plans')
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    total_days = models.IntegerField(default=0)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.SET_NULL, null=True, blank=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.SET_NULL, null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, blank=True)
    number_of_people = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='pending')
    
    def save(self, *args, **kwargs):
        if self.start_date and self.end_date:
            self.total_days = (self.end_date - self.start_date).days
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.username} - {self.city.name}"


class Package(models.Model):
    tour_plan = models.OneToOneField(TourPlan, on_delete=models.CASCADE, related_name='package')
    min_price = models.DecimalField(max_digits=12, decimal_places=2)
    max_price = models.DecimalField(max_digits=12, decimal_places=2)
    calculated_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Package for {self.tour_plan}"


class PaymentStatus(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    SUCCESS = 'Success', 'Success'
    FAILED = 'Failed', 'Failed'
    REFUNDED = 'Refunded', 'Refunded'


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_id = models.CharField(max_length=100, unique=True)
    razorpay_order_id = models.CharField(max_length=100, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    payment_status = models.CharField(max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    payment_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.payment_id} - {self.amount}"


class BookingStatus(models.TextChoices):
    PENDING = 'Pending', 'Pending'
    CONFIRMED = 'Confirmed', 'Confirmed'
    CANCELLED = 'Cancelled', 'Cancelled'
    COMPLETED = 'Completed', 'Completed'


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    tour_plan = models.OneToOneField(TourPlan, on_delete=models.CASCADE, related_name='booking')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='booking')
    booking_status = models.CharField(max_length=20, choices=BookingStatus.choices, default=BookingStatus.PENDING)
    booking_date = models.DateTimeField(auto_now_add=True)
    booking_id = models.CharField(max_length=20, unique=True)
    
    def save(self, *args, **kwargs):
        if not self.booking_id:
            self.booking_id = f"BK{timezone.now().strftime('%Y%m%d%H%M%S')}{self.id or ''}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.booking_id} - {self.user.username}"
