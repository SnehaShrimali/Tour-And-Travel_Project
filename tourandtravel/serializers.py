from rest_framework import serializers
from .models import User, UserProfile, Country, City, TouristPlace, Vehicle, Hotel, Restaurant, TourPlan, Package, Payment, Booking


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone')
        read_only_fields = ('id', 'username')


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source='country.name', read_only=True)
    
    class Meta:
        model = City
        fields = '__all__'


class TouristPlaceSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)
    
    class Meta:
        model = TouristPlace
        fields = '__all__'


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'


class HotelSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)
    
    class Meta:
        model = Hotel
        fields = '__all__'


class RestaurantSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)
    
    class Meta:
        model = Restaurant
        fields = '__all__'


class TourPlanSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)
    vehicle_name = serializers.CharField(source='vehicle.name', read_only=True)
    hotel_name = serializers.CharField(source='hotel.name', read_only=True)
    restaurant_name = serializers.CharField(source='restaurant.name', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = TourPlan
        fields = '__all__'


class PackageSerializer(serializers.ModelSerializer):
    tour_plan_detail = TourPlanSerializer(source='tour_plan', read_only=True)
    
    class Meta:
        model = Package
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Payment
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    tour_plan_detail = TourPlanSerializer(source='tour_plan', read_only=True)
    payment_detail = PaymentSerializer(source='payment', read_only=True)
    
    class Meta:
        model = Booking
        fields = '__all__'


class PackagePriceSerializer(serializers.Serializer):
    tour_plan_id = serializers.IntegerField()
    city_id = serializers.IntegerField()
    vehicle_id = serializers.IntegerField(required=False, allow_null=True)
    hotel_id = serializers.IntegerField(required=False, allow_null=True)
    restaurant_id = serializers.IntegerField(required=False, allow_null=True)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    number_of_people = serializers.IntegerField(default=1)
