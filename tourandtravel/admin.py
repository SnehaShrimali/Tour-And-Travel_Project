from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, UserProfile, Country, City, TouristPlace, Vehicle, Hotel, Restaurant,
    TourPlan, Package, Payment, Booking
)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_customer', 'is_admin')
    list_filter = ('is_staff', 'is_customer', 'is_admin', 'is_superuser')
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone', 'is_customer', 'is_admin')}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('phone', 'is_customer', 'is_admin')}),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'mobile_number', 'email_verified')
    list_filter = ('email_verified',)
    search_fields = ('user__username', 'user__email', 'mobile_number')


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')
    list_filter = ('country',)
    search_fields = ('name', 'country__name')


@admin.register(TouristPlace)
class TouristPlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'entry_fee')
    list_filter = ('city',)
    search_fields = ('name', 'city__name')


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('name', 'vehicle_type', 'price_per_km', 'availability', 'capacity')
    list_filter = ('vehicle_type', 'availability')
    search_fields = ('name',)


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'hotel_type', 'price_per_night', 'rating', 'availability')
    list_filter = ('hotel_type', 'availability', 'city')
    search_fields = ('name', 'city__name')
    list_editable = ('availability',)


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'price_range', 'rating')
    list_filter = ('city',)
    search_fields = ('name', 'city__name')


@admin.register(TourPlan)
class TourPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'start_date', 'end_date', 'total_days', 'status', 'created_at')
    list_filter = ('status', 'city', 'created_at')
    search_fields = ('user__username', 'city__name')
    readonly_fields = ('created_at', 'updated_at', 'total_days')


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('tour_plan', 'min_price', 'max_price', 'calculated_at')
    readonly_fields = ('calculated_at',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'user', 'amount', 'payment_status', 'payment_date')
    list_filter = ('payment_status', 'payment_date')
    search_fields = ('payment_id', 'user__username')
    readonly_fields = ('payment_date',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'user', 'tour_plan', 'booking_status', 'booking_date')
    list_filter = ('booking_status', 'booking_date')
    search_fields = ('booking_id', 'user__username')
    readonly_fields = ('booking_date', 'booking_id')


admin.site.register(User, UserAdmin)

admin.site.site_header = 'Tour & Travel Admin'
admin.site.site_title = 'Tour & Travel Management'
admin.site.index_title = 'Dashboard'
