import razorpay
from django.conf import settings
import uuid
import time


def get_razorpay_client():
    return razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )


def create_razorpay_order(amount, currency='INR'):
    if getattr(settings, 'USE_TEST_PAYMENT', True):
        return {
            'id': f'order_test_{int(time.time())}',
            'amount': int(amount * 100),
            'currency': currency,
            'status': 'created'
        }
    
    client = get_razorpay_client()
    
    order_data = {
        'amount': int(amount * 100),
        'currency': currency,
        'payment_capture': 1,
    }
    
    try:
        order = client.order.create(data=order_data)
        return order
    except Exception as e:
        print(f"Error creating Razorpay order: {e}")
        return None


def verify_razorpay_payment(razorpay_order_id, razorpay_payment_id):
    if getattr(settings, 'USE_TEST_PAYMENT', True):
        return True
    
    client = get_razorpay_client()
    
    try:
        payment = client.payment.fetch(razorpay_payment_id)
        if payment.get('order_id') == razorpay_order_id and payment.get('status') == 'captured':
            return True
        return False
    except Exception as e:
        print(f"Error verifying payment: {e}")
        return False


def generate_payment_id():
    if getattr(settings, 'USE_TEST_PAYMENT', True):
        return f"PAY{uuid.uuid4().hex[:12].upper()}"
    return f"PAY{uuid.uuid4().hex[:12].upper()}"
