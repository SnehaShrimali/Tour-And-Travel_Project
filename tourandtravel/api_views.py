from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from decimal import Decimal
from .models import Country, City, TouristPlace, Vehicle, Hotel, Restaurant, TourPlan
from .serializers import (
    CountrySerializer, CitySerializer, TouristPlaceSerializer,
    VehicleSerializer, HotelSerializer, RestaurantSerializer
)
from .utils import calculate_package_price


class CountryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class CityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    
    def get_queryset(self):
        queryset = City.objects.all()
        country_id = self.request.query_params.get('country', None)
        if country_id:
            queryset = queryset.filter(country_id=country_id)
        return queryset


class TouristPlaceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TouristPlace.objects.all()
    serializer_class = TouristPlaceSerializer
    
    def get_queryset(self):
        queryset = TouristPlace.objects.all()
        city_id = self.request.query_params.get('city', None)
        if city_id:
            queryset = queryset.filter(city_id=city_id)
        return queryset


class VehicleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Vehicle.objects.filter(availability=True)
    serializer_class = VehicleSerializer


class HotelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Hotel.objects.filter(availability=True)
    serializer_class = HotelSerializer
    
    def get_queryset(self):
        queryset = Hotel.objects.filter(availability=True)
        city_id = self.request.query_params.get('city', None)
        hotel_type = self.request.query_params.get('type', None)
        min_rating = self.request.query_params.get('rating', None)
        
        if city_id:
            queryset = queryset.filter(city_id=city_id)
        if hotel_type:
            queryset = queryset.filter(hotel_type=hotel_type)
        if min_rating:
            queryset = queryset.filter(rating__gte=float(min_rating))
        
        return queryset


class RestaurantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    
    def get_queryset(self):
        queryset = Restaurant.objects.all()
        city_id = self.request.query_params.get('city', None)
        if city_id:
            queryset = queryset.filter(city_id=city_id)
        return queryset


class PackagePriceAPIView(APIView):
    def post(self, request):
        try:
            city_id = request.data.get('city_id')
            vehicle_id = request.data.get('vehicle_id')
            hotel_id = request.data.get('hotel_id')
            restaurant_id = request.data.get('restaurant_id')
            start_date = request.data.get('start_date')
            end_date = request.data.get('end_date')
            number_of_people = int(request.data.get('number_of_people', 1))
            
            from datetime import datetime
            start = datetime.strptime(start_date, '%Y-%m-%d').date()
            end = datetime.strptime(end_date, '%Y-%m-%d').date()
            total_days = (end - start).days
            
            tour_plan_data = {
                'city': City.objects.get(id=city_id),
                'start_date': start,
                'end_date': end,
                'total_days': total_days,
                'number_of_people': number_of_people,
                'vehicle': Vehicle.objects.get(id=vehicle_id) if vehicle_id else None,
                'hotel': Hotel.objects.get(id=hotel_id) if hotel_id else None,
                'restaurant': Restaurant.objects.get(id=restaurant_id) if restaurant_id else None,
            }
            
            price_details = calculate_package_price(tour_plan_data)
            
            return Response({
                'success': True,
                'min_price': float(price_details['min_price']),
                'max_price': float(price_details['max_price']),
                'vehicle_cost': float(price_details['vehicle_cost']),
                'hotel_cost': float(price_details['hotel_cost']),
                'restaurant_cost': float(price_details['restaurant_cost']),
                'tourist_place_fees': float(price_details['tourist_place_fees']),
                'total_days': total_days,
                'num_people': number_of_people
            })
        except Exception as e:
            return Response({
                'success': False,
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
