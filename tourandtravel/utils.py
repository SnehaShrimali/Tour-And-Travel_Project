from decimal import Decimal
from .models import TouristPlace


def calculate_package_price(tour_plan):
    total_days = tour_plan.total_days if tour_plan.total_days > 0 else 1
    num_people = tour_plan.number_of_people if tour_plan.number_of_people > 0 else 1
    
    vehicle_cost = Decimal('0')
    if tour_plan.vehicle:
        vehicle_cost = tour_plan.vehicle.price_per_km * 500
    
    hotel_cost = Decimal('0')
    if tour_plan.hotel:
        hotel_cost = tour_plan.hotel.price_per_night * total_days
    
    restaurant_cost_per_meal = Decimal('500')
    restaurant_cost = restaurant_cost_per_meal * total_days * 3
    
    tourist_place_fees = Decimal('0')
    places = TouristPlace.objects.filter(city=tour_plan.city)[:5]
    for place in places:
        tourist_place_fees += place.entry_fee
    
    tourist_place_fees = tourist_place_fees * num_people
    
    base_cost = vehicle_cost + hotel_cost + restaurant_cost + tourist_place_fees
    
    min_price = base_cost * Decimal('0.85')
    max_price = base_cost * Decimal('1.15')
    
    return {
        'min_price': round(min_price, 2),
        'max_price': round(max_price, 2),
        'vehicle_cost': vehicle_cost,
        'hotel_cost': hotel_cost,
        'restaurant_cost': restaurant_cost,
        'tourist_place_fees': tourist_place_fees,
        'total_days': total_days,
        'num_people': num_people
    }


def calculate_total_distance(city):
    distance_map = {
        'Delhi': 0,
        'Mumbai': 1400,
        'Bangalore': 2150,
        'Chennai': 2200,
        'Kolkata': 1500,
        'Jaipur': 280,
        'Goa': 1500,
        'Kerala': 2500,
        'Shimla': 350,
        'Manali': 550,
    }
    return distance_map.get(city.name, 500)
