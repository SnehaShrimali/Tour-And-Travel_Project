from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
from .api_views import (
    CountryViewSet, CityViewSet, TouristPlaceViewSet, VehicleViewSet,
    HotelViewSet, RestaurantViewSet, PackagePriceAPIView
)

router = DefaultRouter()
router.register(r'countries', CountryViewSet)
router.register(r'cities', CityViewSet)
router.register(r'destinations', TouristPlaceViewSet)
router.register(r'vehicles', VehicleViewSet)
router.register(r'hotels', HotelViewSet)
router.register(r'restaurants', RestaurantViewSet)

urlpatterns = [
    path('', views.splash, name='splash'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('change-password/', views.change_password, name='change_password'),
    path('logout/', views.user_logout, name='logout'),
    path('home/', views.home, name='home'),
    path('destination/', views.destination, name='destination'),
    path('vehicle/', views.vehicle_list, name='vehicle'),
    path('hotel/', views.hotel_list, name='hotel'),
    path('restaurant/', views.restaurant_list, name='restaurant'),
    path('planner/', views.tour_planner, name='planner'),
    path('package-summary/', views.package_summary, name='package_summary'),
    path('payment/', views.payment, name='payment'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('booking-success/', views.booking_success, name='booking_success'),
    path('profile/', views.profile, name='profile'),
    path('cancel-booking/<str:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('api/package-price/', PackagePriceAPIView.as_view(), name='api-package-price'),
    path('api/search-suggestions/', views.search_suggestions, name='search_suggestions'),
] + router.urls
