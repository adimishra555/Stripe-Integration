from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import stripe
from .models import Payment
stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def create_checkout(request):
    try:
        if request.method == 'POST':
            name = request.POST['name']
            email = request.POST.get('email', 'raj@gmail.com')  
            phone = request.POST.get('phone', '3182771171') 
            amount = int(request.POST['amount']) * 100  
            customer = stripe.Customer.create(
                name=name,
                email=email,
                phone=phone,
                address={
                    "line1": "510 Townsend St",
                    "postal_code": "10008",
                    "city": "New York",
                    "state": "New York",
                    "country": "United State",
                }
            )
            print(f"New customer created: {customer.id}")
            
            session = stripe.checkout.Session.create(
                customer=customer.id, 
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Premium Membership',  
                            'description': 'Access to all premium features',              
                        },
                        'unit_amount': amount,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url="http://127.0.0.1:8000/success",
                cancel_url="http://127.0.0.1:8000/cancel",
            )

            payment = Payment.objects.create(
                name=name,
                amount=amount / 100, 
                payment_id=session.id,
            )
            return redirect(session.url, code=201)

    except Exception as e:
        return render(request, 'error.html', {'error': str(e)})


def home(request):
    return render(request, 'home.html')

def success(request):
    return render(request, 'success.html')

def success(request):
    return render(request, 'success.html')

def cancel(request):
    return render(request, 'cancel.html')
