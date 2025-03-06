# utilis.py
import requests
from django.conf import settings

def get_paymob_auth_token():
    url = "https://accept.paymob.com/api/auth/tokens"
    payload = {
        "api_key": settings.PAYMOB_API_KEY
    }
    response = requests.post(url, json=payload)
    if response.status_code == 201:
        return response.json().get('token')
    else:
        raise Exception("Failed to get PayMob auth token")
    
    
def create_paymob_order(booking, auth_token):
    url = "https://accept.paymob.com/api/ecommerce/orders"
    payload = {
        "auth_token": auth_token,
        "delivery_needed": "false",
        "amount_cents": str(int(booking.total_price * 100)),  # تحويل المبلغ إلى سنتات
        "currency": "EGP",  # العملة (يمكن تغييرها)
        "items": []  # يمكن إضافة عناصر إذا لزم الأمر
    }
    response = requests.post(url, json=payload)
    if response.status_code == 201:
        return response.json().get('id')  # Order ID
    else:
        raise Exception("Failed to create PayMob order")
    
    
def get_payment_key(auth_token, order_id, booking):
    url = "https://accept.paymob.com/api/acceptance/payment_keys"
    payload = {
        "auth_token": auth_token,
        "amount_cents": str(int(booking.total_price * 100)),
        "expiration": 3600,  # صلاحية المفتاح بالثواني
        "order_id": order_id,
        "billing_data": {
            "first_name": booking.user.first_name,
            "last_name": booking.user.last_name,
            "email": booking.user.email,
            "phone_number": "01010101010",  # يمكن تغييرها
            "country": "EG",  # يمكن تغييرها
        },
        "currency": "EGP",
        "integration_id": settings.PAYMOB_INTEGRATION_ID
    }
    response = requests.post(url, json=payload)
    if response.status_code == 201:
        return response.json().get('token')  # Payment Key
    else:
        raise Exception("Failed to get payment key")