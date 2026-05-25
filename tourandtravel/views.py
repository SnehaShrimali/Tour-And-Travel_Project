from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from decimal import Decimal

from .models import (
    User, UserProfile, Country, City, TouristPlace, Vehicle, Hotel, Restaurant,
    TourPlan, Package, Payment, Booking, BookingStatus
)
from .forms import (
    RegistrationForm, LoginForm, OTPVerificationForm, ForgotPasswordForm,
    ChangePasswordForm, TourPlanForm, ProfileUpdateForm
)
from .otp_service import generate_otp, is_otp_valid, send_otp_email, send_otp_sms, send_booking_confirmation_sms, send_booking_confirmation_email
from .payment_gateway import create_razorpay_order, verify_razorpay_payment, generate_payment_id
from .utils import calculate_package_price


def splash(request):
    return render(request, 'splash.html')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})


def user_register(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            otp = generate_otp()
            profile = user.profile
            profile.otp = otp
            profile.otp_created_at = timezone.now()
            profile.save()
            
            send_otp_email(user.email, otp)
            send_otp_sms(profile.mobile_number, otp)
            
            request.session['registration_user_id'] = user.id
            messages.success(request, 'Registration successful! Please verify your OTP.')
            return redirect('verify_otp')
    else:
        form = RegistrationForm()
    
    return render(request, 'register.html', {'form': form})


def verify_otp(request):
    user_id = request.session.get('registration_user_id')
    if not user_id:
        messages.error(request, 'Session expired. Please register again.')
        return redirect('register')
    
    user = User.objects.get(id=user_id)
    profile = user.profile
    
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            
            if profile.otp == entered_otp and is_otp_valid(profile.otp_created_at):
                profile.email_verified = True
                profile.otp = None
                profile.otp_created_at = None
                profile.save()
                
                login(request, user)
                messages.success(request, 'Email verified successfully!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid or expired OTP')
    else:
        form = OTPVerificationForm()
    
    return render(request, 'verify_otp.html', {'form': form, 'email': user.email})


def resend_otp(request):
    user_id = request.session.get('registration_user_id')
    if not user_id:
        return JsonResponse({'success': False, 'message': 'Session expired'})
    
    user = User.objects.get(id=user_id)
    profile = user.profile
    
    otp = generate_otp()
    profile.otp = otp
    profile.otp_created_at = timezone.now()
    profile.save()
    
    send_otp_email(user.email, otp)
    send_otp_sms(profile.mobile_number, otp)
    
    return JsonResponse({'success': True, 'message': 'OTP resent successfully'})


def forgot_password(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            try:
                user = User.objects.get(email=email)
                profile = user.profile
                
                otp = generate_otp()
                profile.otp = otp
                profile.otp_created_at = timezone.now()
                profile.save()
                
                send_otp_email(email, otp)
                
                request.session['forgot_password_user_id'] = user.id
                messages.success(request, 'OTP sent to your email. Please verify.')
                return redirect('change_password')
            except User.DoesNotExist:
                messages.error(request, 'No user found with this email')
    else:
        form = ForgotPasswordForm()
    
    return render(request, 'forgot_password.html', {'form': form})


def change_password(request):
    user_id = request.session.get('forgot_password_user_id')
    if not user_id:
        messages.error(request, 'Session expired. Please try again.')
        return redirect('forgot_password')
    
    user = User.objects.get(id=user_id)
    profile = user.profile
    
    if request.method == 'POST':
        form = OTPVerificationForm(request.POST)
        if form.is_valid():
            entered_otp = form.cleaned_data['otp']
            
            if profile.otp == entered_otp and is_otp_valid(profile.otp_created_at):
                new_password_form = ChangePasswordForm(request.POST)
                if new_password_form.is_valid():
                    password = new_password_form.cleaned_data['new_password']
                    user.set_password(password)
                    user.save()
                    
                    profile.otp = None
                    profile.otp_created_at = None
                    profile.save()
                    
                    del request.session['forgot_password_user_id']
                    messages.success(request, 'Password changed successfully! Please login.')
                    return redirect('login')
            else:
                messages.error(request, 'Invalid or expired OTP')
    else:
        form = OTPVerificationForm()
        new_password_form = ChangePasswordForm()
    
    return render(request, 'change_password.html', {'form': form, 'email': user.email})


def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('splash')


@login_required
def home(request):
    countries = Country.objects.all()
    cities = City.objects.all()[:10]
    vehicles = Vehicle.objects.filter(availability=True)
    
    recent_destinations = City.objects.all()[:6]
    
    return render(request, 'home.html', {
        'countries': countries,
        'cities': cities,
        'vehicles': vehicles,
        'recent_destinations': recent_destinations
    })


@login_required
def destination(request):
    countries = Country.objects.all()
    cities = City.objects.all()
    search_query = request.GET.get('q', '')
    
    if search_query:
        cities = cities.filter(name__icontains=search_query) | cities.filter(country__name__icontains=search_query)
    
    return render(request, 'destination.html', {
        'countries': countries,
        'cities': cities.distinct(),
        'search_query': search_query
    })


@login_required
def vehicle_list(request):
    vehicles = Vehicle.objects.filter(availability=True)
    vehicle_type = request.GET.get('type', '')
    
    if vehicle_type:
        vehicles = vehicles.filter(vehicle_type=vehicle_type)
    
    return render(request, 'vehicle.html', {
        'vehicles': vehicles,
        'selected_type': vehicle_type
    })


@login_required
def hotel_list(request):
    hotels = Hotel.objects.filter(availability=True)
    city_id = request.GET.get('city', '')
    hotel_type = request.GET.get('type', '')
    min_rating = request.GET.get('rating', '')
    
    if city_id:
        hotels = hotels.filter(city_id=city_id)
    if hotel_type:
        hotels = hotels.filter(hotel_type=hotel_type)
    if min_rating:
        hotels = hotels.filter(rating__gte=float(min_rating))
    
    cities = City.objects.all()
    
    return render(request, 'hotel.html', {
        'hotels': hotels,
        'cities': cities,
        'selected_city': city_id,
        'selected_type': hotel_type,
        'selected_rating': min_rating
    })


@login_required
def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    city_id = request.GET.get('city', '')
    
    if city_id:
        restaurants = restaurants.filter(city_id=city_id)
    
    cities = City.objects.all()
    
    return render(request, 'restaurant.html', {
        'restaurants': restaurants,
        'cities': cities,
        'selected_city': city_id
    })


@login_required
def tour_planner(request):
    if request.method == 'POST':
        form = TourPlanForm(request.POST)
        if form.is_valid():
            tour_plan = form.save(commit=False)
            tour_plan.user = request.user
            tour_plan.save()
            
            request.session['tour_plan_id'] = tour_plan.id
            return redirect('package_summary')
    else:
        form = TourPlanForm()
    
    cities = City.objects.all()
    vehicles = Vehicle.objects.filter(availability=True)
    hotels = Hotel.objects.filter(availability=True)
    restaurants = Restaurant.objects.all()
    
    return render(request, 'planner.html', {
        'form': form,
        'cities': cities,
        'vehicles': vehicles,
        'hotels': hotels,
        'restaurants': restaurants
    })


@login_required
def package_summary(request):
    tour_plan_id = request.session.get('tour_plan_id')
    if not tour_plan_id:
        messages.error(request, 'Please create a tour plan first')
        return redirect('planner')
    
    try:
        tour_plan = TourPlan.objects.get(id=tour_plan_id, user=request.user)
    except TourPlan.DoesNotExist:
        messages.error(request, 'Tour plan not found')
        return redirect('planner')
    
    price_details = calculate_package_price(tour_plan)
    
    if request.method == 'POST':
        package, created = Package.objects.update_or_create(
            tour_plan=tour_plan,
            defaults={
                'min_price': price_details['min_price'],
                'max_price': price_details['max_price']
            }
        )
        
        request.session['package_min_price'] = str(price_details['min_price'])
        return redirect('payment')
    
    return render(request, 'package_summary.html', {
        'tour_plan': tour_plan,
        'price_details': price_details
    })


@login_required
def payment(request):
    tour_plan_id = request.session.get('tour_plan_id')
    if not tour_plan_id:
        messages.error(request, 'Please create a tour plan first')
        return redirect('planner')
    
    try:
        tour_plan = TourPlan.objects.get(id=tour_plan_id, user=request.user)
    except TourPlan.DoesNotExist:
        messages.error(request, 'Tour plan not found')
        return redirect('planner')
    
    package = Package.objects.filter(tour_plan=tour_plan).first()
    
    if not package:
        price_details = calculate_package_price(tour_plan)
        package, _ = Package.objects.update_or_create(
            tour_plan=tour_plan,
            defaults={
                'min_price': price_details['min_price'],
                'max_price': price_details['max_price']
            }
        )
    
    amount = float(package.min_price)
    
    razorpay_order = create_razorpay_order(amount)
    
    if not razorpay_order:
        messages.error(request, 'Payment gateway error. Please try again.')
        return redirect('package_summary')
    
    request.session['razorpay_order_id'] = razorpay_order.get('id')
    request.session['payment_amount'] = amount
    
    return render(request, 'payment.html', {
        'tour_plan': tour_plan,
        'package': package,
        'razorpay_order_id': razorpay_order.get('id'),
        'amount': amount,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID
    })


@login_required
@csrf_exempt
def payment_success(request):
    razorpay_order_id = request.session.get('razorpay_order_id')
    razorpay_payment_id = request.POST.get('razorpay_payment_id', '')
    amount = request.session.get('payment_amount', 0)
    tour_plan_id = request.session.get('tour_plan_id')
    
    if verify_razorpay_payment(razorpay_order_id, razorpay_payment_id):
        try:
            tour_plan = TourPlan.objects.get(id=tour_plan_id)
            
            payment = Payment.objects.create(
                user=request.user,
                amount=Decimal(str(amount)),
                payment_id=generate_payment_id(),
                razorpay_order_id=razorpay_order_id,
                razorpay_payment_id=razorpay_payment_id,
                payment_status='Success'
            )
            
            booking = Booking.objects.create(
                user=request.user,
                tour_plan=tour_plan,
                payment=payment,
                booking_status='Confirmed'
            )
            
            tour_plan.status = 'confirmed'
            tour_plan.save()
            
            profile = request.user.profile
            send_booking_confirmation_sms(profile.mobile_number, booking.booking_id)
            send_booking_confirmation_email(request.user.email, booking, tour_plan)
            
            request.session.pop('tour_plan_id', None)
            request.session.pop('razorpay_order_id', None)
            request.session.pop('payment_amount', None)
            request.session.pop('package_min_price', None)
            
            return render(request, 'booking_success.html', {'booking': booking})
        except Exception as e:
            messages.error(request, f'Error processing booking: {str(e)}')
            return redirect('home')
    else:
        Payment.objects.create(
            user=request.user,
            amount=Decimal(str(amount)),
            payment_id=generate_payment_id(),
            razorpay_order_id=razorpay_order_id,
            razorpay_payment_id=razorpay_payment_id,
            payment_status='Failed'
        )
        messages.error(request, 'Payment verification failed')
        return redirect('payment')


@login_required
def booking_success(request):
    booking_id = request.GET.get('id', '')
    booking = None
    
    if booking_id:
        try:
            booking = Booking.objects.get(booking_id=booking_id, user=request.user)
        except Booking.DoesNotExist:
            pass
    
    if not booking:
        booking = Booking.objects.filter(user=request.user, booking_status='Confirmed').first()
    
    return render(request, 'booking_success.html', {'booking': booking})


@login_required
def profile(request):
    user = request.user
    bookings = Booking.objects.filter(user=user).order_by('-booking_date')
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user_profile = user.profile
            if 'profile_image' in request.FILES:
                user_profile.profile_image = request.FILES['profile_image']
                user_profile.save()
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=user)
    
    return render(request, 'profile.html', {
        'form': form,
        'bookings': bookings,
        'user': user
    })


@login_required
def cancel_booking(request, booking_id):
    try:
        booking = Booking.objects.get(booking_id=booking_id, user=request.user)
        if booking.booking_status == 'Confirmed':
            booking.booking_status = 'Cancelled'
            booking.save()
            
            tour_plan = booking.tour_plan
            tour_plan.status = 'cancelled'
            tour_plan.save()
            
            messages.success(request, 'Booking cancelled successfully')
        else:
            messages.error(request, 'This booking cannot be cancelled')
    except Booking.DoesNotExist:
        messages.error(request, 'Booking not found')
    
    return redirect('profile')


def search_suggestions(request):
    query = request.GET.get('q', '')
    suggestions = []
    
    if query:
        cities = City.objects.filter(name__icontains=query)[:5]
        countries = Country.objects.filter(name__icontains=query)[:5]
        
        for city in cities:
            suggestions.append({
                'type': 'city',
                'name': city.name,
                'country': city.country.name
            })
        
        for country in countries:
            suggestions.append({
                'type': 'country',
                'name': country.name
            })
    
    return JsonResponse(suggestions, safe=False)
