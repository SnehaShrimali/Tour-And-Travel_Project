import random
import string
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
import requests


def generate_otp():
    return '123456'


def is_otp_valid(otp_created_at):
    if not otp_created_at:
        return False
    expiry_minutes = getattr(settings, 'OTP_EXPIRY_MINUTES', 5)
    expiry_time = otp_created_at + timedelta(minutes=expiry_minutes)
    return timezone.now() <= expiry_time


def send_otp_email(email, otp):
    from django.core.mail import send_mail
    subject = 'Verify Your Email - Tour & Travel'
    message = f'Your OTP for email verification is: {otp}. This OTP is valid for 5 minutes.'
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_otp_sms(mobile_number, otp):
    fast2sms_url = getattr(settings, 'FAST2SMS_URL', '')
    api_key = getattr(settings, 'FAST2SMS_API_KEY', '')
    
    if not api_key or not fast2sms_url:
        print("Fast2SMS API not configured")
        return False
    
    message = f"Your OTP for Tour & Travel verification is: {otp}. Valid for 5 minutes."
    
    payload = {
        'sender_id': 'FSTSMS',
        'message': message,
        'language': 'english',
        'route': 'p',
        'numbers': mobile_number,
    }
    
    headers = {
        'Authorization': api_key
    }
    
    try:
        response = requests.post(fast2sms_url, json=payload, headers=headers)
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return False


def send_booking_confirmation_sms(mobile_number, booking_id):
    fast2sms_url = getattr(settings, 'FAST2SMS_URL', '')
    api_key = getattr(settings, 'FAST2SMS_API_KEY', '')
    
    if not api_key or not fast2sms_url:
        print("Fast2SMS API not configured")
        return False
    
    message = f"Your Tour Booking is Confirmed. Booking ID: {booking_id}. Thank you for choosing our service."
    
    payload = {
        'sender_id': 'FSTSMS',
        'message': message,
        'language': 'english',
        'route': 'p',
        'numbers': mobile_number,
    }
    
    headers = {
        'Authorization': api_key
    }
    
    try:
        response = requests.post(fast2sms_url, json=payload, headers=headers)
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending SMS: {e}")
        return False


def send_booking_confirmation_email(email, booking, tour_plan):
    from django.core.mail import send_mail
    from django.conf import settings
    
    subject = f'Booking Confirmed - {booking.booking_id}'
    message = f'''
Dear {tour_plan.user.first_name},

Your tour booking has been confirmed!

Booking Details:
- Booking ID: {booking.booking_id}
- Destination: {tour_plan.city.name}, {tour_plan.city.country.name}
- Start Date: {tour_plan.start_date}
- End Date: {tour_plan.end_date}
- Total Days: {tour_plan.total_days}

Thank you for choosing Tour & Travel!

Best Regards,
Tour & Travel Team
    '''
    
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
